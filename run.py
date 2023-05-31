import os

import uvicorn
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()

    # 是否启用代码自动刷新
    reload = True
    if os.environ.get('APP_FASTAPI_FRAME_RELOAD', '').lower() == 'false':
        reload = False

    # 指定端口
    port = int(os.environ.get('APP_FASTAPI_FRAME_PORT', 9002))

    # 指定运行的进程数量，通用公式：2 * CPU核心数 + 1，非正式环境默认为1
    workers_num = 1
    if os.getenv('env') == 'pro':
        workers_num = 2 * int(os.cpu_count()) + 1
    workers_num = int(os.environ.get('APP_FASTAPI_FRAME_WORKERS', workers_num))
    print(f'启动的进程数量：{workers_num}')

    print(f"是否开启 reload={reload}")
    uvicorn.run('app:app', host='0.0.0.0', port=port, reload=reload, workers=workers_num)
