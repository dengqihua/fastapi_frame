# _*_ coding: utf-8 _*_
# @创建时间：2023/4/25 01:58
# @作者：dengqihua
# @名称 : __init__.py
# @描述 :

from fastapi import APIRouter

from app.routers.auth.api import auth_api
from app.routers.auth.response_model import auth_out
from app.libs.response import SuccessBaseModel

router = APIRouter()

router.add_api_route(
    '.register.get',
    auth_api.register,
    methods=['post'],
    summary='用户注册',
    response_model=SuccessBaseModel,
)

router.add_api_route(
    '.login.get',
    auth_api.login,
    methods=['post'],
    summary='用户登录',
    response_model=auth_out.LoginOut,
)
