# _*_ coding: utf-8 _*_
# @创建时间：2023/4/25 01:43
# @作者：dengqihua
# @名称 : auth_api.py
# @描述 : 登录验证相关

from app.constants.enums import LoginType
from app.libs.utils import success_response, set_response
from app.logic.user_logic import UserLogic
from app.routers.auth.request_model import auth_in


async def register(item: auth_in.RegisterIn):
    """用户注册"""
    result = await UserLogic.register(item.username, item.password, item.platform)
    return success_response()


async def login(item: auth_in.LoginIn):
    """ 用户登录 """
    # 用户账号密码登录
    result = await UserLogic.login_account(username=item.username, password=item.password)

    return success_response(result)
