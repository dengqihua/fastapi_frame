# _*_ coding: utf-8 _*_
# @创建时间：2023/04/27 21:58
# @作者：dengqihua
# @名称 : setting.py
# @描述 : 配置文件
import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool = False
    env: str

    # mysql 配置
    mysql_host: str = '127.0.0.1'
    mysql_port: int = 3306
    mysql_user: str = 'root'
    mysql_password: str = '123456'
    mysql_database: str = 'test'
    mysql_maxsize: int = 5

    # redis 配置
    redis_host: str = '127.0.0.1'
    redis_port: int = 6379
    redis_user: str = 'default'
    redis_password: str = '123456'
    redis_db: int = 0
    redis_max_connections: int = 10
    redis_timeout: int = 3

    # mysql 多库配置
    mysql: dict

    # redis 多库配置
    redis: dict

    version: str = '1.0'
    service_name: str = 'app'
    project_name: str = 'fastapi_frame'
    base_dir: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    request_timeout: int = 5
    request_limit_per_host: int = 300
    limit: int = 20
    keepalive_timeout: int = 15
    default_lock_time: int = 10

    # jwt
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


settings = Settings()
