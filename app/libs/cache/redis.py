# _*_ coding: utf-8 _*_
# @创建时间：2022/12/14 00:10
# @作者：dengqihua
# @名称 : redis.py
# @描述 : redis
import aioredis
from icecream import ic

from app.config.setting import settings

redis_pool = type('RedisPool', (), {})


async def init_redis():
    """初始化redis连接池"""
    pool = aioredis.ConnectionPool.from_url(
        f'redis://{settings.redis_host}:{settings.redis_port}',
        username=settings.redis_user,
        password=settings.redis_password,
        max_connections=settings.redis_max_connections,
        db=settings.redis_db,
        encoding='utf-8',
        decode_responses=True
    )
    setattr(redis_pool, 'default', pool)

    if settings.redis:
        for name, conf in settings.redis.items():
            pool = aioredis.ConnectionPool.from_url(
                f'redis://{conf.get("host")}:{conf.get("port")}',
                username=conf.get('user', 'default'),
                password=conf.get('password'),
                max_connections=int(conf.get('max_connections')),
                db=conf.get('db'),
                encoding='utf-8',
                decode_responses=True
            )

    ic('初始化redis连接池成功！')
    return pool


async def get_redis_conn(name=None):
    """获取redis链接"""
    name = name or 'default'

    if hasattr(redis_pool, name):
        connection_pool = getattr(redis_pool, name)
    else:
        connection_pool = await init_redis()

    redis_conn = await aioredis.Redis(connection_pool=connection_pool)
    return redis_conn
