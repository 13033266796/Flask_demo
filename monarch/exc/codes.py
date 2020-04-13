"""
正常http状态码 200 302 400 401 403 404 500

1. 当http请求失败，返回失败的http状态码
2. 当http请求验证数据失败，返回http状态码400
3. 当http请求成功，业务处理失败，返回http状态码200

当http状态码是302/400/401/403/404/500 前端这边直接处理了http请求 不往下走业务逻辑
当http状态码是200 业务状态码是自定义时 前端先处理http请求 然后处理业务逻辑 比如说表单提交 参数错误时 返回400业务状态码 前端会根据返回的错误处理逻辑 给予提示
   - 因此http状态码是200 仅仅代表网络请求正常 具体业务处理还需要根据数据包的code来判断
   - http code 200 返回数据：
        {'code': 200, msg: '操作成功', 'data': {} }
   - http code 200 返回数据：
        {
            "code": 400,
            "msg": "参数错误",
            "data": {
                "status": [
                    "Missing data for required field."
                ],
                "department_id": [
                    "Missing data for required field."
                ],
                "name": [
                    "Not a valid string."
                ],
                "type": [
                    "Missing data for required field."
                ]
            }
        }
"""

HTTP_OK = 200
HTTP_FOUND = 302
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_SERVER_ERROR = 500

CODE_OK = 200
CODE_FOUND = 302
CODE_BAD_REQUEST = 400
CODE_UNAUTHORIZED = 401
CODE_FORBIDDEN = 403
CODE_NOT_FOUND = 404
CODE_SERVER_ERROR = 500

# 业务状态码
BIZ_CODE_OK = 0
BIZ_CODE_FAIL = 1

BIZ_REMOTE_SERVICE_TIMEOUT = 20001
BIZ_REMOTE_SERVICE_NOT_VALID = 20002
BIZ_REMOTE_DATA_NOT_VALID = 20003
BIZ_REMOTE_SERIALIZE_NOT_VALID = 20004

# 内部业务代码
BIZ_CODE_NOT_EXISTS = 100404
