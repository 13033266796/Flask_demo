from functools import wraps, partial

from flask import request, g

from monarch.corelibs.mcredis import mc
from monarch.exc.consts import CACHE_USER_TOKEN
from monarch.models.user import User
from monarch.utils.api import biz_success
from monarch.exc import codes


def check_admin_login(view):
    """验证登录状态"""

    @wraps(view)
    def wrapper(*args, **kwargs):
        token = request.headers.get("token")
        biz_forbidden = partial(biz_success, code=codes.CODE_FORBIDDEN, http_code=codes.HTTP_FORBIDDEN)
        if not token:
            return biz_forbidden(msg="用户无权限")
        cache_admin_user_token = CACHE_USER_TOKEN.format(token)
        admin_user_id = mc.get(cache_admin_user_token)
        if not admin_user_id:
            return biz_forbidden(msg="token已过期")

        admin_user = User.get(admin_user_id)
        if not admin_user:
            return biz_forbidden(msg="用户不存在")

        g.admin_user = admin_user
        return view(*args, **kwargs)

    return wrapper
