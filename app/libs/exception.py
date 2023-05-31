import logging


class HTTPException(Exception):
    def __init__(self, code: str, message: str, service_name: str = None):
        self.code = str(code)
        self.message = message
        self.service_name = service_name


class BizException(Exception):
    def __init__(self, code: str, message: str):
        self.code = str(code)
        self.message = message


class RespCodeException(Exception):

    def __init__(self, err_node):
        # 备注：err_node类型为ErrorNode。因为循环导包问题这里不增加入参类型标注
        self.code = str(err_node.code)
        self.message = err_node.message

    def __str__(self):
        return f"{self.code}: {self.message}"


class RetryError(Exception):
    """重试异常"""


class NeedRetryError(RetryError):
    """需要重试的时候，抛出的异常"""

    def __init__(self, message, level=logging.ERROR):
        self.level = level
        RetryError.__init__(self, message)


class FailRetryError(RetryError):
    """重试全部失败之后，抛出的异常"""

