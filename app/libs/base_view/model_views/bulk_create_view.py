from typing import Dict, List

from fastapi import Body

from app.libs.base_view.base_view import BaseView, ResponseView
from app.libs.base_view.errors import ManagerApiError
from app.libs.const import Method


class BulkCreateModelView(BaseView):
    def __init__(self, manager):
        self.manager = manager
        super().__init__(
            path=".batch.add",
            methods=[Method.post],
            summary=f"批量创建{self.manager.model_name}"
        )

    @ResponseView()
    async def as_view(
            self,
            infos: List[Dict] = Body(..., embed=True)
    ):
        for info in infos:
            unknow_fields = set(info.keys()).difference(self.manager.model_cls._meta.fields)
            if unknow_fields:
                return ManagerApiError.field_not_found.apply(
                    model_name=self.manager.model_name,
                    unknow_fields=unknow_fields
                )
        success = await self.manager.bulk_create(infos)
        if not success:
            return ManagerApiError.bulk_create_fail.apply(
                model_name=self.manager.model_name
            )
        return dict(success=success)
