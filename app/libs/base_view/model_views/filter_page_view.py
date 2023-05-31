from typing import Dict, List

from fastapi import Body, Depends

from app.libs.base_view.base_view import BaseView, ResponseView
from app.libs.base_view.errors import ManagerApiError
from app.libs.const import Method
from app.libs.dependency import Paginator


class FilterPageModelView(BaseView):
    def __init__(self, manager):
        self.manager = manager
        super().__init__(
            path=".filter.page.get",
            methods=[Method.post],
            summary=f"分页条件过滤{self.manager.model_name}"
        )

    @ResponseView()
    async def as_view(
            self,
            filter_params: Dict = Body(..., embed=True),
            orderings: List[str] = Body(None, embed=True),
            values: List[str] = Body(None, embed=True),
            paginator: Paginator = Depends()
    ):
        unknow_fields = {param.split('__')[0] for param in filter_params}.difference(self.manager.model_cls._meta.fields)
        unknow_ordering_fields = {ordering.split("-")[-1] for ordering in orderings}.difference(self.manager.model_cls._meta.fields)
        if unknow_fields or unknow_ordering_fields:
            return ManagerApiError.field_not_found.apply(
                model_name=self.manager.model_name,
                unknow_fields=unknow_fields or unknow_ordering_fields
            )
        models = await self.manager.filter_page(filter_params, orderings, paginator.offset, paginator.limit, values=values)
        total = None
        if paginator.need_total:
            total = await self.manager.filter_count(filter_params)
        data_list = [model if issubclass(type(model), dict) else model.to_dict() for model in models]
        return paginator.get_page_data(data_list, total)
