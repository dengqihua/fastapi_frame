# _*_ coding: utf-8 _*_
# @创建时间：2023/4/29 23:18
# @作者：dengqihua
# @名称 : dependencies.py
# @描述 :

import hashlib
import json
from typing import List

from fastapi import HTTPException, Header, Query, Request, status
from jose import JWTError, jwt

from app.config.setting import settings
from app.libs.cache.redis import get_redis_conn
from app.libs.utils import success_response
from app.constants.redis_key import RedisKey


async def auth_token_header(user_token: str = Header(..., description='用户token'), request: Request = Request):
    try:
        payload = jwt.decode(user_token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_token_md5 = hashlib.md5(user_token.encode()).hexdigest()
        # redis获取
        redis_conn = await get_redis_conn('default')
        redis_key = RedisKey.user_token_key(user_token_md5)
        redis_value = await redis_conn.get(redis_key)
        if not redis_value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={'code': 40100, 'message': "用户登录token验证失败！"}
            )
        user_info = json.loads(redis_value)
        user_info['user_token_jwt'] = user_token
        user_info['user_token'] = user_token_md5
        request.state.user = user_info
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'code': 40100, 'message': "用户登录token验证失败！"}
        )


class Paginator:
    """分页器"""

    def __init__(
            self,
            offset: int = Query(0, description="分页参数offset", ge=0),
            limit: int = Query(20, description="分页参数limit", le=1000),
    ):
        self.offset = offset
        self.limit = limit

    def get_list_response(self, data_list: List, total=None, do_format=False):
        """获取分页响应"""
        data = self.get_page_data(data_list, total)
        return success_response(data, do_format=do_format)

    def get_page_data(self, data_list: List, total=None):
        next_offset = self.offset + self.limit

        assert isinstance(total, int)
        next_offset = next_offset if next_offset < total else total
        has_more = total > next_offset
        data = {
            "data_list": data_list,
            "total": total,
            "has_more": has_more,
            "next_offset": next_offset
        }
        return data
