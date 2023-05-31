# _*_ coding: utf-8 _*_
# @创建时间：2023/5/15 22:19
# @作者：dengqihua
# @名称 : test.py
# @描述 : 测试脚本

import asyncio
import sys
import os

from app import app
from app.ctx.app_ctx import app_context


class TaskHandle(object):
    async def run(self):
        """"""
        print('执行成功！')


async def work():
    async with app_context(app):
        await TaskHandle().run()


if __name__ == '__main__':
    asyncio.run(work())
