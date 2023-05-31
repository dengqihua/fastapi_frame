# _*_ coding: utf-8 _*_
# @创建时间：2023/05/31 14:18
# @作者：dengqihua
# @名称 : user_model.py
# @描述 : 用户表模型类

from tortoise import fields
from app.libs.base_view.base_model import CheckingModel


class User(CheckingModel):
    username = fields.CharField(max_length=64, description="用户名")
    password = fields.CharField(max_length=64, null=True, description="密码")
    mobile = fields.CharField(max_length=15, null=True, description="手机号码")
    nickname = fields.CharField(max_length=128, null=True, description="用户昵称")
    real_name = fields.CharField(max_length=250, null=True, description="真实姓名")
    device = fields.CharField(max_length=32, null=True, description="设备类型，Android安卓系统；IOS苹果系统；PC桌面系统")
    platform = fields.CharField(max_length=32, null=True, description="用户注册平台，，wx_miniprogram：微信小程序，wx_public：微信公众号，ios：ios客户端；android：安卓客户端；pc：PC端；h5：h5端")
    last_login_time = fields.DatetimeField(null=True, description="最后一次登录时间")

    class Meta:
        table = 'user'
