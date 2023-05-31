from fastapi import Query

from app.libs.base_view.base_view import BaseView, ResponseView
from app.libs.base_view.errors import ManagerApiError
from app.libs.const import Method


class GetModelView(BaseView):
    def __init__(self, manager):
        self.manager = manager
        super().__init__(
            path=".get",
            methods=[Method.get],
            summary=f"查询单个{self.manager.model_name}"
        )

    @ResponseView()
    async def as_view(
            self,
            model_id: int = Query(...)
    ):
        model = await self.manager.get(model_id)
        if not model:
            return ManagerApiError.get_not_found.apply(model_id=model_id, model_name=self.manager.model_name)
        return {self.manager.model_name: model.to_dict()}
