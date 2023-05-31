# _*_ coding: utf-8 _*_
# @创建时间：2023/4/25 01:58
# @作者：dengqihua
# @名称 : __init__.py
# @描述 :

from fastapi import APIRouter

from app.libs.response import SuccessBaseModel
from app.routers.user.api import user_api
from app.routers.user.response_model import user_out

router = APIRouter()

router.add_api_route(
    '.info.get',
    user_api.get_user_info,
    methods=['get'],
    summary='获取用户信息',
    response_model=user_out.GetUserInfoOut,
)

router.add_api_route(
    '.info.edit',
    user_api.update_user,
    methods=['post'],
    summary='更新用户信息',
    response_model=SuccessBaseModel
)
