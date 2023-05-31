from typing import Dict

from fastapi import Body

from app.libs.base_view.base_view import BaseView, ResponseView
from app.libs.base_view.errors import ManagerApiError
from app.libs.const import Method


class CreateModelView(BaseView):
    def __init__(self, manager):
        self.manager = manager
        super().__init__(
            path=".add",
            methods=[Method.post],
            summary=f"创建{self.manager.model_name}"
        )

    @ResponseView()
    async def as_view(
            self,
            info: Dict = Body(..., embed=True)
    ):
        unknow_fields = set(info.keys()).difference(self.manager.model_cls._meta.fields)
        if unknow_fields:
            return ManagerApiError.field_not_found.apply(
                model_name=self.manager.model_name,
                unknow_fields=unknow_fields
            )
        model = await self.manager.create(info)
        if not model:
            return ManagerApiError.create_fail.apply(
                model_name=self.manager.model_name
            )
        return {self.manager.model_cls._meta.db_table: model.to_dict()}
