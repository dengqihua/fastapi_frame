# _*_ coding: utf-8 _*_
# @创建时间：2023/4/25 01:43
# @作者：dengqihua
# @名称 : auth_in.py
# @描述 :

from typing import Optional

from pydantic import BaseModel, Field

from app.constants.enums import Platform


class LoginIn(BaseModel):
    """登录入参"""
    username: Optional[str] = Field(None, description='用户名，登录方式为account时必传')
    password: Optional[str] = Field(None, description='密码， 登录方式为account时必传')


class RegisterIn(BaseModel):
    """用户注册入参"""
    platform: Optional[Platform] = Field(..., description='注册平台，ios：ios客户端；android：安卓客户端；pc：PC端；h5：h5端')
    username: Optional[str] = Field(..., description='用户名')
    password: Optional[str] = Field(..., description='密码')
