"""
@Time: 2026/3/4
@Author: chyu.wissfi@gmail.com
@Description: HTTP code
"""
from enum import Enum

class HttpCode(str, Enum):
    """
    HTTP 基础业务状态码
    """
    SUCCESS = "success" # 成功
    FAIL = "fail" # 失败
    NOT_FOUND = "not_found" # 未找到
    UNAUTHORIZED = "unauthorized" # 未授权
    FORBIDDEN = "forbidden" # 无权限，禁止访问
    VALIDATE_ERROR = "validate_error" # 数据校验错误