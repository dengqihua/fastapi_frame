# _*_ coding: utf-8 _*_
# @创建时间：2023/4/25 01:43
# @作者：dengqihua
# @名称 : auth_api.py
# @描述 : 用户相关
from fastapi import Request

from app.libs.utils import success_response
from app.logic.user_logic import UserLogic
from app.routers.user.request_model import user_in


async def get_user_info(request: Request = Request):
    """获取用户信息"""
    user_id = request.state.user.get('id')
    result = await UserLogic.get_user_info(user_id)
    return success_response(result, do_format=True)


async def update_user(item: user_in.UpdateUserIn, request: Request = Request):
    """更新用户信息"""
    to_update = {}
    user_id = request.state.user['id']
    if item.nickname:
        to_update['nickname'] = item.nickname
    if item.real_name:
        to_update['real_name'] = item.real_name
    if to_update:
        await UserLogic.update_user(user_id=user_id, to_update=to_update)
    return success_response()
