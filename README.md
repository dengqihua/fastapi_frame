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

### 设置当前项目的路径
```shell
    export PYTHONPATH="D:\python\fastapi_frame"
```
     
### 执行脚本
```shell
    python ./app/script/脚本名称.py
```


# 自动生成的交互式 API 文档
http://127.0.0.1:9001/docs


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