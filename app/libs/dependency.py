# _*_ coding: utf-8 _*_
# @创建时间：2022/12/12 22:52
# @作者：dengqihua
# @名称 : dependency.py
# @描述 : 依赖

from typing import List

from fastapi import Body, Query

from .utils import success_response


class Paginator:
    """分页器"""

    def __init__(
            self,
            offset: int = Query(0, description='分页参数offset', ge=0),
            limit: int = Query(20, description='分页参数limit', le=1000),
            need_total: bool = Body(True, description='是否需要总数', embed=True)
    ):
        self.offset = offset
        self.limit = limit
        self.need_total = need_total

    def get_list_response(self, data_list: List, total=None):
        data = self.get_page_data(data_list, total)
        return success_response(data)

    def get_page_data(self, data_list: list, total=None):
        next_offset = self.offset + self.limit
        if self.need_total:
            assert isinstance(total, int)
            next_offset = next_offset if next_offset < total else total
            has_more = total > next_offset
        else:
            total = 0
            has_more = len(data_list) >= self.limit

        data = {
            'data_list': data_list,
            'total': total,
            'has_more': has_more,
            'next_offset': next_offset
        }
        return data
