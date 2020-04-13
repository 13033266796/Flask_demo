from monarch.exc.codes import (
    # 系统状态码
    CODE_BAD_REQUEST,
    CODE_FORBIDDEN,
    CODE_NOT_FOUND,
    CODE_SERVER_ERROR,
    CODE_UNAUTHORIZED,
    # 业务状态码
    BIZ_CODE_OK,
    BIZ_CODE_FAIL,
    BIZ_REMOTE_SERVICE_TIMEOUT,
    BIZ_REMOTE_SERVICE_NOT_VALID,
    BIZ_REMOTE_DATA_NOT_VALID,
    BIZ_REMOTE_SERIALIZE_NOT_VALID,
)

# 状态码与提示映射
errmsg = {
    CODE_BAD_REQUEST: "参数错误",
    CODE_UNAUTHORIZED: "权限不足",
    CODE_FORBIDDEN: "拒绝访问",
    CODE_NOT_FOUND: "无法找到资源",
    CODE_SERVER_ERROR: "服务端错误",
    BIZ_CODE_OK: "成功",
    BIZ_CODE_FAIL: "失败",
    BIZ_REMOTE_SERVICE_TIMEOUT: "远程服务超时",
    BIZ_REMOTE_SERVICE_NOT_VALID: "远程服务不可用",
    BIZ_REMOTE_DATA_NOT_VALID: "远程服务数据无法解析",
    BIZ_REMOTE_SERIALIZE_NOT_VALID: "远程服务数据无法序列化",
}
