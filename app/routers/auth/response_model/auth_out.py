# _*_ coding: utf-8 _*_
# @创建时间：2023/4/25 01:51
# @作者：dengqihua
# @名称 : auth_out.py
# @描述 :

from typing import Optional

from pydantic import Field

from app.libs.response import ResponseBaseModel
from app.routers.user.response_model.user_out import UserBaseInfo


class LoginInfo(UserBaseInfo):
    user_token: Optional[str] = Field(description='用户登录token')


class LoginOut(ResponseBaseModel):
    data: Optional[LoginInfo] = Field(description='用户信息')
