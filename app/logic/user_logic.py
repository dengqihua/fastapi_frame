# _*_ coding: utf-8 _*_
# @创建时间：2023/4/25 02:07
# @作者：dengqihua
# @名称 : user_logic.py
# @描述 :

import hashlib
import json
from datetime import datetime, timedelta
from typing import Union

from fastapi import HTTPException, status
from icecream import ic
from jose import jwt

from app.config.setting import settings
from app.constants.redis_key import RedisKey
from app.libs.cache.redis import get_redis_conn
from app.libs.time_helper import DATETIME_FORMAT_NORMAL
from app.libs.utils import hash_password, check_password
from app.managers.user_manager import UserManager


class UserLogic:
    """用户相关"""

    @classmethod
    async def register(cls, username, password, platform):
        """用户注册"""
        # 判断该用户名是否被注册
        if await UserManager.filter_existed(filter_params={'username': username}):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={'code': 40900, 'message': '该用户名已被注册！'}
            )
        user_info = await UserManager.create(to_create={
            'username': username,
            'password': hash_password(password),
            'platform': platform
        })
        return user_info

    @classmethod
    async def login_account(cls, username, password):
        """用户账号密码方式登录"""
        # 根据用户名获取用户信息
        user_info = await UserManager.filter_first(filter_params={'username': username})
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={'code': 40400, 'message': '该用户未注册，请先注册！'}
            )
        # 验证密码是否正确
        if not check_password(user_info.password, password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={'code': 40100, 'message': '用户名或密码错误！'}
            )

        # 更新最后一次登录时间
        await UserManager.update(user_info.id, to_update={'last_login_time': datetime.now()})

        user_info = user_info.to_dict()

        # 将 用户信息 保存在 token 中
        user_token_expires = timedelta(minutes=settings.jwt_access_token_expire_minutes)
        token_data = {
            'id': user_info.get('id'),
            'username': user_info.get('username'),
            'nickname': user_info.get('nickname'),
            'avatar_url': user_info.get('avatar_url'),
            'create_time': user_info.get('create_time').strftime(DATETIME_FORMAT_NORMAL),
        }
        user_token = await cls.create_user_token(
            data=token_data,
            expires_delta=user_token_expires
        )

        # 将token保存到redis
        redis_conn = await get_redis_conn('default')
        pipe = await redis_conn.pipeline()

        user_token_md5 = hashlib.md5(user_token.encode()).hexdigest()
        redis_key = RedisKey.user_token_key(user_token_md5)
        token_data['mobile'] = user_info.get('mobile')
        token_data['user_token_jwt'] = user_token
        pipe.setex(redis_key, user_token_expires, json.dumps(token_data))

        # 保存user_id和user_token映射关系
        redis_key = RedisKey.mapping_user_id_token(user_id=user_info.get('id'))
        pipe.setex(redis_key, user_token_expires, user_token_md5)

        await pipe.execute()

        result = token_data.copy()
        result['user_token'] = user_token
        return result

    @classmethod
    async def create_user_token(cls, data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"expire": expire.isoformat()})
        ic(to_encode)
        encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
        return encoded_jwt

    @classmethod
    async def get_user_info(cls, user_id):
        """获取用户信息"""
        user_info = await UserManager.filter_first(filter_params={'id': user_id})
        return user_info.to_dict()

    @classmethod
    async def update_user(cls, user_id, to_update):
        """更新用户信息"""
        result = await UserManager.update(user_id, to_update=to_update)
        return {}
