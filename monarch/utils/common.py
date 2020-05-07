import uuid
from functools import wraps, partial
from flask import request, g
from marshmallow import ValidationError, EXCLUDE
import hashlib

from monarch.corelibs.mcredis import mc
from monarch.exc.consts import CACHE_USER_INFO
from monarch.models.user import User
from monarch.models.robot import Robot
from monarch.utils.api import Bizs, biz_success
from monarch.exc import codes
from monarch.exc import message
from monarch.external.sso_admin_client import operating


def _check_user_login(access_token):
    if not access_token:
        return False, Bizs.forbidden(msg=message.FORBIDDEN_TOKEN_ERROR)

    cache_admin_user_token = CACHE_USER_INFO.format(access_token=access_token)
    user_info = mc.get(cache_admin_user_token)
    if not user_info:
        return False, Bizs.forbidden(msg=message.FORBIDDEN_TOKEN_INVALIDATE)

    admin_user_id = user_info.get("id")
    admin_user = User.get(admin_user_id)
    if not admin_user:
        return False, Bizs.forbidden(msg=message.FORBIDDEN_USER_NOT_EXISTS)

    return True, admin_user


def check_admin_login(view):
    """验证登录状态"""

    @wraps(view)
    def wrapper(*args, **kwargs):
        token = request.headers.get("token")
        is_ok, resp = _check_user_login(token)
        if not is_ok:
            return resp

        g.admin_user = resp
        return view(*args, **kwargs)

    return wrapper


def _check_user_robot_id(user_obj, robot_id):
    """检查用户的robot_id是否合规"""
    robot = Robot.get(robot_id)
    if not robot:
        return False, Bizs.forbidden(message.FORBIDDEN_ROBOT_ID_NOT_EXISTS)

    if robot.company_id != user_obj.company_id:
        return False, Bizs.forbidden(message.FORBIDDEN_ROBOT_ID_ERROR)

    return True, "ok"


def check_user_robot_id(view):
    """验证用户robot_id"""
    @wraps(view)
    def wrapper(*args, **kwargs):
        is_ok, resp = _check_user_robot_id(g.admin_user, g.data["robot_id"])
        if not is_ok:
            return resp

        return view(*args, **kwargs)

    return wrapper


def get_schema_doc_params(schema):
    """将 marshmallow 的 schema 转换成 flask-restful 能识别的doc

    额外定义shema参数
        doc_type: 文档中要展示的数据类型, string, bool, integer, 默认为schema的类型
        doc_location: 文档中的http数据来源 query, header, formData, body, cookie, 默认为query
    示例:
        class TestSchema(Schema):
            name = fields.Str(required=True, allow_none=False, doc_location="query")
            age = fields.Int(required=True, allow_none=False, doc_location="body")

    Args:
        schema: marshmallow 的 schema 实例
    """
    params = {}
    for field_name in schema.declared_fields:
        field = schema.fields[field_name]
        doc_type = field.metadata.get("doc_type", field.__class__.__name__.lower())
        doc_location = field.metadata.get("doc_location", "query")
        params[field.name] = {"type": doc_type,
                              "in": doc_location,
                              "required": field.required,
                              "description": field.metadata.get("description")}
    return params


def doc_schema(namespace, schema):
    """添加schema到doc """
    params = get_schema_doc_params(schema)
    return namespace.doc(params=params)


def expect_schema(namespace, schema):
    """类似flask-restful的expect"""

    def wrapper(view):
        view = doc_schema(namespace, schema)(view)
        return form_validate(schema)(view)

    return wrapper


def form_validate(schema):
    """接口请求参数验证"""

    def wrapper(view):
        @wraps(view)
        def view_wrapper(*args, **kw):
            r_params = request.args if request.method == "GET" else (request.json or {})
            try:
                data = schema.load(r_params, unknown=EXCLUDE)  # 忽略未知字段

            except ValidationError as error_info:
                return Bizs.bad_query(data=error_info.messages)

            g.data = data
            return view(*args, **kw)

        return view_wrapper

    return wrapper


def gen_random_key():
    """生成32位随机数"""
    return hashlib.md5(str(uuid.uuid4()).encode("utf-8")).hexdigest()


def check_conf_center_token(view):
    """验证运营页面权限"""
    @wraps(view)
    def wrapper(*args, **kwargs):
        biz_forbidden = partial(biz_success, code=codes.CODE_UNAUTHORIZED, http_code=codes.HTTP_OK)
        data = request.get_json()
        token = request.values.get("token") or data.get("token")
        code = request.values.get("code") or data.get("code")
        is_ok, _ = operating.check_token(code, token)
        if is_ok != codes.BIZ_CODE_OK:
            return biz_forbidden(msg="绑定失败，请重新绑定")
        return view(*args, **kwargs)

    return wrapper
