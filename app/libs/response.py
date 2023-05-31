from typing import List

from pydantic import BaseModel, Field


class ResponseBaseModel(BaseModel):
    code: int = Field(default=200, description='状态码')
    message: str = Field(default='提示信息')


class SuccessBaseModel(ResponseBaseModel):
    """请求成功统一返回"""
    data: dict


class ListResponseDataModel(BaseModel):
    """分页列表响应data模型"""
    total: int
    has_more: bool
    next_offset: int
    data_list: List


class ListResponseModel(ResponseBaseModel):
    """分页列表响应统一返回"""
    data: ListResponseDataModel
