# _*_ coding: utf-8 _*_
# @创建时间：2023/4/25 01:43
# @作者：dengqihua
# @名称 : auth_in.py
# @描述 :

from typing import Optional

from pydantic import BaseModel, Field


class UpdateUserIn(BaseModel):
    nickname: Optional[str] = Field(description='用户昵称')
    real_name: Optional[str] = Field(description='真实姓名')
