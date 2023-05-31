# _*_ coding: utf-8 _*_
# @创建时间：2023/4/25 01:51
# @作者：dengqihua
# @名称 : auth_out.py
# @描述 :

from typing import Optional

from pydantic import BaseModel, Field

from app.libs.response import ResponseBaseModel


class UserBaseInfo(BaseModel):
    """用户基本信息"""
    id: Optional[int] = Field(description='用户id')
    username: Optional[str] = Field(description='用户名')
    mobile: Optional[str] = Field(description='手机号码，如果为空，则未授权手机号')
    nickname: Optional[str] = Field(description='用户昵称')
    real_name: Optional[str] = Field(description='真实姓名')
    avatar_url: Optional[str] = Field(description='头像地址')


class GetUserInfoOut(ResponseBaseModel):
    data: Optional[UserBaseInfo] = Field(description='用户信息')
