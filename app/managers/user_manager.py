# _*_ coding: utf-8 _*_
# @创建时间：2023/05/31 14:18
# @作者：dengqihua
# @名称 : user_manager.py
# @描述 : 用户表Manager类

from app.libs.base_view.base_manager import BaseManager
from app.models import User


class UserManagerCls(BaseManager):

    def __init__(self):
        super().__init__(model_cls=User)


UserManager = UserManagerCls()
