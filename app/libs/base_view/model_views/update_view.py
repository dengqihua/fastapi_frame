from typing import Dict

from fastapi import Body, Query

from app.libs.base_view.base_view import BaseView, ResponseView
from app.libs.base_view.errors import ManagerApiError
from app.libs.const import Method


class UpdateModelView(BaseView):
    def __init__(self, manager):
        self.manager = manager
        super().__init__(
            path=".edit",
            methods=[Method.post],
            summary=f"修改{self.manager.model_name}"
        )

    @ResponseView()
    async def as_view(
            self,
            model_id: int = Query(...),
            info: Dict = Body(..., embed=True)
    ):
        unknow_fields = set(info.keys()).difference(self.manager.model_cls._meta.fields)
        if unknow_fields:
            return ManagerApiError.field_not_found.apply(
                model_name=self.manager.model_name,
                unknow_fields=unknow_fields
            )
        flag = await self.manager.update(model_id, info)
        if not flag:
            return ManagerApiError.update_fail.apply(
                model_id=model_id,
                model_name=self.manager.model_name
            )
        return dict(success=flag)
