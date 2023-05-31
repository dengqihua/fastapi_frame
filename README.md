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

### 执行命令
```shell
    python run.py
```
    

# 运行脚本
### 设置.env文件绝对路径的环境变量
```shell
    export ENV_ABSOLUTE_PATH="D:\python\fastapi_frame" 
```

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

