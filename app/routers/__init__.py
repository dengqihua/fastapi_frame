# 所有路由入口

from fastapi import APIRouter, Depends

from app.dependencies import auth_token_header
from app.routers import auth, user

api_router = APIRouter()

api_router.include_router(auth.router, prefix='/auth', tags=['验证相关'])
api_router.include_router(user.router, prefix='/user', dependencies=[Depends(auth_token_header)], tags=['用户相关'])


@api_router.get("/health_check", description="容器心跳检测", tags=['其它'])
async def _():
    return 'alive'
