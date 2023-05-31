# fastapi_frame

# 依赖
    Python 3.10 及更高版本

# 安装

### 创建虚拟环境
通过执行 venv 指令来创建一个 虚拟环境
```shell
    python -m venv ./venv
```

### 激活虚拟环境
    不同系统激活方式不一样，参考文档：https://docs.python.org/zh-cn/3.10/library/venv.html#how-venvs-work

### 安装依赖
```shell
    pip install -r requirements.txt
```

# 运行

### 设置环境变量

- `APP_FASTAPI_FRAME_RELOAD` 是否启用代码自动更新，默认为启用，生产环境需要设置为false
```shell
    #开发环境
    export APP_FASTAPI_FRAME_RELOAD="True"
    
    #生产环境
    export APP_FASTAPI_FRAME_RELOAD="False"
```

- `APP_FASTAPI_FRAME_WORKERS` 指定运行的进程数量，非生产环境默认为：1，生产环境根据公式计算：2 * CPU核数 + 1，如果PM2工具启动需要设置具体的进程数量，
```shell
    export APP_FASTAPI_FRAME_WORKERS=5
```

### 创建.env文件
```shell
    cp .env_dev .env
```
 根据自己信息，修改相关配置

### 执行命令
```shell
    python run.py
```
    

# 运行脚本

### 设置环境变量
```shell
    # 当前项目根路径加入到模块的搜索路径
    export PYTHONPATH="D:\python\fastapi_frame"
    # 指定.env文件的路径
    export ENV_ABSOLUTE_PATH="D:\python\fastapi_frame"
```
     
### 执行脚本
```shell
    python ./app/script/脚本名称.py
```


# 交互式API文档
http://127.0.0.1:9002/docs


# 实战
- 框架已包含注册、登录、获取用户信息、修改用户信息接口，运行前请先创建你的数据库，然后导入如下SQL语句
```sql
CREATE TABLE `user` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL COMMENT '用户名',
  `password` varchar(64) DEFAULT NULL COMMENT '密码',
  `mobile` varchar(15) DEFAULT NULL COMMENT '手机号码',
  `nickname` varchar(128) DEFAULT NULL COMMENT '用户昵称',
  `real_name` varchar(250) DEFAULT NULL COMMENT '真实姓名',
  `device` varchar(32) DEFAULT NULL COMMENT '设备类型，Android安卓系统；IOS苹果系统；PC桌面系统',
  `platform` varchar(32) DEFAULT NULL COMMENT '用户注册平台，ios：ios客户端；android：安卓客户端；pc：PC端；h5：h5端',
  `status` tinyint(3) unsigned NOT NULL DEFAULT '1' COMMENT '状态，0冻结，1正常',
  `last_login_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '最后一次登录时间',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username_unique` (`username`) USING BTREE,
  UNIQUE KEY `mobile_unique` (`mobile`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='用户表';
```

- 登录采用JWT方式，token保存到redis，请修改redis相关配置

### 实用脚本

- 根据数据库表结构，自动生成model、manager文件
```shell
    
    python app/script/auto_create_model.py -h 
    
    # usage: auto_create_model.py [-h] [--table TABLE] [--databse DATABSE] [--force FORCE]
    # 根据数据库表结构，自动生成model、manager文件
    # options:
    #   -h, --help         show this help message and exit
    #   --table TABLE      表名，默认值：*，代表全部表, 举例：--table=user
    #   --databse DATABSE  数据库名称，默认值：test，如：--databse=test
    #   --force FORCE      是否强制覆盖已存在的文件，默认值：0，参数解释：0 不覆盖，1 强制覆盖

```


### 目录结构说明
```shell

app 应用目录
  |-- config  配置目录
    |-- setting.py  读取.env文件的全局配置文件
  |-- constants   常量目录
    |-- enums.py    枚举常量文件
    |-- redis_key.py  redis的key文件
  |-- ctx 上下文目录
    |-- app_ctx.py   app上下文
  |-- dependencies.py   
  |-- libs    类库目录
    |-- base_view  框架基础类库
    |-- cache   缓存目录
      |-- redis.py    redis缓存文件
    |-- common.py   公共文件
    |-- const.py    常量文件
    |-- decorators.py   装饰器文件
    |-- dependency.py   依赖性文件
    |-- exception.py    自定义异常处理类文件
    |-- response.py     响应文件
    |-- time_helper.py  时间工具函数
    |-- utils.py        工具类文件
  |-- logic  逻辑处理层
    |-- user_logic.py
  |-- managers  业务处理层
    |-- user_manager.py
  |-- models  模型层
    |-- user_model.py
  |-- routers  路由层
    |-- auth  认证路由
      |-- api
        |-- auth_api.py
      |-- request_model
        |-- auth_in.py
      |-- response_model
        |-- auth_out.py
  |-- script 脚本目录
    |-- auto_create_model.py
    |-- test.py
    |-- tpl
      |-- manager_template.tpl
      |-- model_template.tpl
run.py    启动文件
requirements.txt
.env_dev  开发环境环境变量文件
.env_pro  生产环境环境变量文件
```
