import hashlib
import re
import socket
import time
import uuid
import bcrypt
from datetime import datetime
from typing import Callable, Iterator

from app.libs.time_helper import str_to_timestamp, to_datetime_str


class GetSetTer(object):
    def __init__(self):
        self._x = None

    @property
    def x(self):
        """I'm the 'x' property."""
        print("getter of x called")
        return self._x

    @x.setter
    def x(self, value):
        print("setter of x called")
        self._x = value

    @x.deleter
    def x(self):
        print("deleter of x called")
        del self._x


def get_host():
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('114.114.114.114', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def to_int(num_str, default_num=0):
    try:
        return int(num_str)
    except:
        return default_num


def to_float(num_str, default_num=0):
    try:
        return float(num_str)
    except:
        return default_num


def verify_phone(phone):
    """校验是否手机号码"""
    return bool(re.match(re.compile(r'^1[3-9]\d{9}$'), phone))


def add_param_if_true(params, key, value, only_check_none=False):
    """
    不为空则添加到参数中
    :param params 要加入元素的字典
    :param key 要加入字典的key值
    :param value 要加入字典的value值
    :param only_check_none 是否只检查空值 [0、false等是有意义的]
    """
    if value or (only_check_none and value is not None):
        params[key] = value


def get_params_str(params: dict, sort: bool = False) -> str:
    """
    用于拼接 param query string
    :param params: 字典参数
    :param sort: 是否需要对字典进行按键升序排序, 这通常用于加密相关
    :return: k1=v1&k2=v2
    """
    if sort:
        return "&".join([f"{key}={params[key]}" for key in sorted(params.keys())])
    else:
        return "&".join([f"{key}={value}" for key, value in params.items()])


def get_md5_str(sign_dict: dict, salt: str = "", sort: bool = True) -> str:
    """
    根据盐加密对应的字典, 返回对应的md5字符串
    参与加密的参数字典默认会按照键升序排序
    :param sign_dict: 加密字典参数
    :param salt: 加密盐, 默认为空串
    :param sort: 通常需要对字典进行按键升序排序, 默认为真
    :return: 32位的md5加密字符串
    """
    sign_str = get_params_str(sign_dict, sort=sort)
    md5_obj = hashlib.md5()
    md5_obj.update((sign_str + salt).encode())
    return md5_obj.hexdigest()


def handle_datetime(_obj):
    """
    正则匹配时间，获取format_str
    2020-11-20 15:49:38.000

    """
    try:
        # 兼容db_server
        if isinstance(_obj, str):
            _obj = _obj.replace("T", " ")
            return to_datetime_str(str_to_timestamp(_obj))
        elif isinstance(_obj, int):
            return _obj
        elif isinstance(_obj, datetime):
            return to_datetime_str(_obj.timestamp())
        elif _obj is None:
            return
        else:
            raise Exception(f"意外的时间格式: {_obj},{type(_obj)}")
    except:
        raise Exception(f"意外的时间格式: {_obj},{type(_obj)}")


def format_response(_obj, _key=None):
    _new_obj = None
    if isinstance(_obj, dict):
        _new_obj = {}
        for k, v in _obj.items():
            key, info = format_response(v, k)
            _new_obj[key] = info

    elif isinstance(_obj, list):
        _new_obj = []
        for i in _obj:
            _, info = format_response(i)
            _new_obj.append(info)
    elif _key and _key.endswith("_time"):
        _new_obj = handle_datetime(_obj)
        _key = f"{_key[:-5]}_time"
    else:
        _new_obj = _obj
    return _key, _new_obj


def set_response(content, do_format=True):
    """
    在model检查前处理数据
    用于统一响应数据
    此时拿到的数据已经是未经过model检查的
    """
    content["now_time"] = int(time.time())
    if content.get("data") and do_format:
        _, content["data"] = format_response(content["data"])
    return content


def format_success_response(data=None, do_format=True):
    """成功的响应"""
    data = data or {}
    content = {
        'code': 200,
        'message': 'SUCCESS',
        'data': data
    }
    return set_response(content, do_format)


def format_fail_response(message, data=None, code=500, do_format=True):
    """失败的响应【格式化时间：将 _time 结尾的字段全部转化为 _ts】"""
    if data is None:
        data = {}
    content = {
        'code': code,
        'message': str(message),
        'data': data
    }
    return set_response(content, do_format)


def success_response(data=None, do_format=False):
    """成功的响应"""
    return format_success_response(data, do_format=do_format)


def fail_response(message, data=None, code=500):
    """失败的响应【不格式化时间】"""
    return format_fail_response(message, data, code, do_format=False)


def generate_trade_no(length=32) -> str:
    """生成订单号"""
    # 获取当前时间，格式化为 %Y%m%d%H%M%S
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    # 生成 UUID，并去掉短横线
    unique_id = str(uuid.uuid4()).replace('-', '')
    # 拼接前缀和唯一标识符，返回订单号
    trade_no = current_time + unique_id
    return trade_no[:length]


def url_params_to_dict(url_params) -> dict:
    """url参数转换成字典格式"""
    return dict(item.split('=') for item in url_params.split('&'))


def groupby(iterable: Iterator, keyfunc: Callable):
    """
    按照keyfunc返回的值分组
    """
    ret = {}

    if not iterable:
        return {}

    if not keyfunc:
        keyfunc = lambda x: x

    for item in iterable:
        key = keyfunc(item)
        ret.setdefault(key, []).append(item)

    return ret


def hash_password(password):
    """ 对密码进行哈希 """
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode()


def check_password(hashed_password, user_password):
    """ 检查用户提供的密码是否与哈希密码匹配 """
    return bcrypt.checkpw(user_password.encode(), hashed_password.encode())
