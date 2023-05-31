import enum
from copy import deepcopy

from app.config.setting import settings
from app.libs.exception import HTTPException


class ErrorNode:
    def __init__(self, code, msg):
        self.code = code
        self.message = msg

    @property
    def service_name(self):
        return settings.service_name

    def unpack(self):
        return self.code, self.message

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message
        }

    def apply(self, *args, **kwargs):
        _node = deepcopy(self)
        _node.message = _node.message.format(*args, **kwargs)
        return _node

    def to_exception(self):
        return HTTPException(self.code, self.message)


class Error:
    success = ErrorNode(200, "success")
    no_auth = ErrorNode(401, "您没有操作权限")
    login_fail = ErrorNode(403, "用户名或密码错误")
    timeout_error = ErrorNode(504, "timeout")


class CommonEnum(enum.Enum):
    @classmethod
    def get_members_values(cls):
        """ 获取所有的成员values """
        return [item.value for item in cls.__members__.values()]

    @classmethod
    def get_members_keys(cls):
        """ 获取所有的成员key """
        return [item for item in cls.__members__.keys()]

    @classmethod
    def get_value_by_key(cls, key):
        """根据key值获取value值，value不存时返回key值"""
        return cls.__members__.get(key).value if cls.__members__.get(key) else key

    @classmethod
    def get_members_items(cls):
        """
        获取所有的成员 items
        :return dict
        """
        return {item: getattr(cls, item).value for item in cls.__members__.keys()}


class IntEnum(int, CommonEnum):
    pass


class StringEnum(str, CommonEnum):
    pass


class Method(StringEnum):
    get = "get"
    post = "post"
