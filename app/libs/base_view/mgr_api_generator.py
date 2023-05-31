from inspect import isclass

from fastapi import APIRouter

from app.libs.base_view.base_manager import BaseManager
from app.libs.base_view.base_view import BaseView


class ManagerApiGenerator(object):

    def __init__(self, manager: BaseManager):
        self.manager = manager

    async def bind_entry(self, manager_api_entry):
        """
        初始化manager对应的router
        """
        router = APIRouter()
        for api_view in self.manager.exposed_apis():
            if isclass(api_view) and issubclass(api_view, BaseView):
                api_view(self.manager).bind_router(router)
        manager_api_entry.include_router(
            router,
            prefix=f"/{self.manager.model_name}",
            tags=[f"{self.manager.model_name}模型API"]
        )
