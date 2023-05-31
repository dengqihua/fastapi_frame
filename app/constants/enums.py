# _*_ coding: utf-8 _*_
# @创建时间：2023/4/29 17:05
# @作者：dengqihua
# @名称 : enums.py
# @描述 : 枚举类

from app.libs.const import StringEnum


class Env(StringEnum):
    """环境"""
    local = 'local'
    test = 'test'
    pro = 'pro'


class LoginType(StringEnum):
    """登录方式"""
    account = 'account'  # 用户账号密码方式登录
    mobile = 'mobile'  # 手机验证码方式登录


class Platform(StringEnum):
    """平台"""
    ios = 'ios'  # ios客户端
    android = 'android'  # android客户端
    pc = 'pc'  # pc
    h5 = 'h5'  # h5
