import json
from math import ceil

from flask import Response, abort, jsonify, request

from monarch.exc import codes
from monarch.exc.consts import DEFAULT_PAGE, DEFAULT_PER_PAGE
from monarch.exc.message import errmsg
from functools import partial


def http_fail(data=None, code=None, http_code=None, msg=None):
    """系统失败统一处理
    """
    if data is None:
        data = {}
    if code is None:
        code = codes.CODE_BAD_REQUEST
    if http_code is None:
        http_code = code
    if msg is None:
        msg = errmsg.get(code, "")

    success = True if code == codes.BIZ_CODE_OK else False
    data = json.dumps(dict(code=code, msg=msg, data=data, success=success))
    return Response(data, status=http_code, mimetype="application/json")


def biz_success(
    data=None,
    code=codes.BIZ_CODE_OK,
    http_code=codes.HTTP_OK,
    msg=None,
    mimetype="application/json",
):
    """系统成功 业务逻辑处理返回
    """
    if data is None:
        data = {}
    if code is None:
        code = codes.BIZ_CODE_OK
    if msg is None:
        msg = errmsg.get(code, "")

    success = True if code == codes.BIZ_CODE_OK else False
    data = json.dumps(dict(code=code, msg=msg, data=data, success=success))
    return Response(data, status=http_code, mimetype=mimetype)


class Bizs:
    success = biz_success

    bad_query = partial(biz_success, code=codes.CODE_BAD_REQUEST,
                        http_code=codes.HTTP_BAD_REQUEST)

    not_found = partial(biz_success, code=codes.BIZ_CODE_NOT_EXISTS)

    forbidden = partial(biz_success, code=codes.CODE_FORBIDDEN,
                        http_code=codes.HTTP_FORBIDDEN)

    fail = partial(biz_success, code=codes.BIZ_CODE_FAIL, http_code=codes.HTTP_OK)


def parse_pagination(query):
    page = request.args.get("page", type=int, default=DEFAULT_PAGE)
    per_page = min(
        request.args.get("per_page", type=int, default=DEFAULT_PER_PAGE), 1000
    )

    count = query.count()
    total_page = int(ceil(float(count) / per_page))
    pagination = {
        "total_count": count,
        "per_page": per_page,
        "page": page,
        "total_pages": total_page,
    }
    if count != 0:
        if page > total_page:
            # todo: 此处有待斟酌
            return {"pagination": pagination, "result": []}
    else:
        return {"pagination": pagination, "result": []}
    query = query.offset(per_page * (page - 1)).limit(per_page)
    return {"pagination": pagination, "result": query.all()}


def schema_pagination(page_result, schema_cls):
    """利用shema解析结果列表
        page_result: 通过parse_pagination返回的result
        schema_cls: schema的类
    """
    data = schema_cls().dump(page_result["result"], many=True).data
    return {"pagination": page_result["pagination"], "list": data}


def _abort(http_code=400, data=None, message="", business_code=None):
    if not business_code:
        business_code = http_code
    data = {"code": business_code, "msg": message, "data": data or {}, "success": False}
    abort(Response(jsonify(data), mimetype="application/json", status=http_code))
