import shortuuid
from flask import request
from monarch.corelibs.mcredis import mc
from monarch.exc import codes
from monarch.exc.consts import CACHE_USER_TOKEN, CACHE_TWELVE_HOUR, CACHE_CAPTCHA_IMAGE_KEY
from monarch.forms.admin.user import UserSchema
from monarch.models.user import User
from monarch.utils.api import Bizs, parse_pagination


def get_user_list(data):
    query_field = data.get("query_field")
    keyword = data.get("keyword")

    pagi_data = parse_pagination(User.paginate_user(query_field, keyword))

    _result, _pagination = pagi_data.get("result"), pagi_data.get("pagination")

    admin_user_data = UserSchema().dump(_result, many=True)
    return Bizs.success({"result": admin_user_data, "pagination": _pagination})


def login(data):
    account = data.get("account")
    password = data.get("password")
    captcha_value = data.get("captcha_value")
    captcha_id = data.get("captcha_id")

    cache_captcha_image_key = CACHE_CAPTCHA_IMAGE_KEY.format(captcha_id)
    captcha_code = mc.get(cache_captcha_image_key)
    if not captcha_code:
        return Bizs.bad_query(code=codes.CODE_BAD_REQUEST, http_code=codes.HTTP_BAD_REQUEST, msg="验证码不存在")

    if captcha_code != captcha_value:
        return Bizs.bad_query(code=codes.CODE_BAD_REQUEST, http_code=codes.HTTP_BAD_REQUEST, msg="验证码错误")

    user = User.get_by_account(account)
    if not user:
        return Bizs.bad_query(code=codes.CODE_BAD_REQUEST, http_code=codes.HTTP_BAD_REQUEST, msg="账号密码错误")
    if not user.check_password(password):
        return Bizs.bad_query(code=codes.CODE_BAD_REQUEST, http_code=codes.HTTP_BAD_REQUEST, msg="账号密码错误")

    token = shortuuid.uuid()
    mc.set(CACHE_USER_TOKEN.format(token), user.id, CACHE_TWELVE_HOUR)

    result = {
        'token': token,
        'expired_at': CACHE_TWELVE_HOUR,
        'account': user.account,
        'id': user.id
    }
    return Bizs.success(result)


def logout():
    token = request.headers.get("token")
    mc.delete(CACHE_USER_TOKEN.format(token))
    return Bizs.success()
