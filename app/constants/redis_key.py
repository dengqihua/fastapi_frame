# _*_ coding: utf-8 _*_
# @创建时间：2023/5/6 12:55
# @作者：dengqihua
# @名称 : redis_keys.py
# @描述 :
from app.config.setting import settings


class RedisKey:

    @staticmethod
    def user_token_key(token, is_prefix=True):
        """用户user_token"""
        prefix = f'{settings.project_name}:' if is_prefix else None
        return f'{prefix}user_token:{token}'

    @staticmethod
    def mapping_user_id_token(user_id, is_prefix=True):
        """用户user_id和user_token 映射关系"""
        prefix = f'{settings.project_name}:' if is_prefix else None
        return f'{prefix}user_id_token:{user_id}'
