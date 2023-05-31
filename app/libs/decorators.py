# _*_ coding: utf-8 _*_
# @创建时间：2022/12/12 21:59
# @作者：dengqihua
# @名称 : decorators.py
# @描述 : 装饰器
import hashlib
import threading
from functools import wraps


def synchronized(func):
    """锁装饰器"""
    func.__lock__ = threading.Lock()

    @wraps(func)
    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return lock_func


def singleton(cls_):
    """单例类装饰器"""

    class wrap_cls(cls_):
        __instance = None

        @synchronized
        def __new__(cls, *args, **kwargs):
            if cls.__instance is None:
                cls.__instance = super().__new__(cls, *args, **kwargs)
                cls.__instance.__init = False
            return cls.__instance

        @synchronized
        def __init__(self, *args, **kwargs):
            if self.__init:
                return
            super().__init__(*args, **kwargs)

    wrap_cls.__name__ = cls_.__name__
    wrap_cls.__doc__ = cls_.__doc__
    wrap_cls.__qualname__ = cls_.__qualname__
    return wrap_cls


def cache_method(prefix=None, cache_time=60):
    """
    方法缓存装饰器
    要缓存的方法返回值必须是可json.dumps
    :param prefix string 缓存key的前缀
    :param cache_time int 缓存过期时间，单位秒
    """

    def cache_decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache = None
            r_prefix = prefix or ''
            # 可以转换为字符串的类型
            to_str_types = (int, str, float, list, tuple, dict)
            param_args = f'{",".join([str(item) for item in args if type(item) in to_str_types])}'
            param_kwargs = ','.join(sorted([f'{k}={v}' for k, v in kwargs.items() if type(v) in to_str_types]))
            param_md5 = hashlib.md5(f'{func.__qualname__}{param_args}{param_kwargs}'.encode()).hexdigest()
            cache_key = f'{r_prefix}:{func.__name__}:{param_md5}'
            result = await cache.get(cache_key)
            if not result:
                result = await func(*args, **kwargs)
                await cache.set(cache_key, result, timeout=cache_time)
            return result

        return wrapper

    return cache_decorator
