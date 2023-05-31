from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse
from icecream import ic
from starlette.exceptions import HTTPException as StarletteHTTPException
from tortoise.contrib.fastapi import register_tortoise

from app.config.setting import settings
from app.libs.base_view.base_manager import BaseManager, Managers
from app.libs.base_view.base_model import BaseOrmModel, CheckingModel
from app.libs.base_view.mgr_api_generator import ManagerApiGenerator
from app.libs.base_view.utils import get_classes_from_package
from app.libs.cache.redis import init_redis
from app.libs.utils import GetSetTer
from app.routers import api_router

docs_url = redoc_url = openapi_url = None

# 只有调试模式才开启文档
if settings.debug:
    docs_url = "/docs"
    redoc_url = "/redoc"
    openapi_url = "/openapi.json"

app = FastAPI(
    title='fastapi',
    openapi_url=openapi_url,
    docs_url=docs_url,
    redoc_url=redoc_url,
    description='''
测试环境：https://www.test.com \n
生产环境：https://www.pro.com
    '''
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    """重写 HTTPException 错误处理器"""

    async def get_content(exc):
        if isinstance(exc.detail, dict):
            content = {'code': exc.detail.get('code', exc.status_code), 'message': exc.detail.get('message')}
        else:
            content = {'code': exc.status_code, 'message': exc.detail}
        return content

    return JSONResponse(
        status_code=exc.status_code,
        content=await get_content(exc)
    )


@app.on_event('startup')
async def startup_event():
    # 导入路由
    app.include_router(api_router, prefix='')

    # 使用ic包替换print打印数据
    await ic_init()

    # 初始化数据库链接
    await db_init(app)

    # 初始化数据库表CURD操作路由
    await manager_api_init(
        app,
        f'{settings.base_dir}/{settings.service_name}/models',
        f'{settings.service_name}.models'
    )

    # 初始化redis连接池
    await init_redis()


async def ic_init():
    ic.configureOutput(prefix=f'{settings.service_name}|')
    if not settings.debug:
        ic.disable()


async def db_init(_app: FastAPI):
    """初始化数据库"""
    db_config = {
        'timezone': 'Asia/Shanghai',
        'connections': {
            'scdm_ai': {
                'engine': 'tortoise.backends.mysql',
                'credentials': {
                    'host': settings.mysql_host,
                    'port': settings.mysql_port,
                    'user': settings.mysql_user,
                    'password': settings.mysql_password,
                    'database': settings.mysql_database,
                    'maxsize': settings.mysql_maxsize
                }
            }
        },
        'apps': {
            'scdm_ai': {
                'models': ['app.models'],
                'default_connection': 'scdm_ai'
            }
        }
    }
    register_tortoise(
        app,
        config=db_config,
        generate_schemas=False,
        add_exception_handlers=False
    )
    ic('初始化数据库连接成功！')


async def manager_api_init(_app: FastAPI, model_pkg_path, model_pkg_name):
    """manager_api 初始化"""
    orm_models = await get_classes_from_package(
        model_pkg_path,
        model_pkg_name,
        parent_cls=BaseOrmModel,
        exclude_cls=[CheckingModel]
    )

    manager_api_entry = APIRouter()
    _app.state.managers = Managers()
    for _model in orm_models:
        if hasattr(_model, "manager") and isinstance(_model.manager, BaseManager):
            manager = _model.manager
        else:
            manager = BaseManager(model_cls=_model)
        manager_apis = ManagerApiGenerator(manager)
        await manager_apis.bind_entry(manager_api_entry)
        setattr(_app.state.managers, manager.model_name, manager)
    _app.include_router(manager_api_entry, prefix="/manager_api")
    ic('初始化manager_api路由成功！')
