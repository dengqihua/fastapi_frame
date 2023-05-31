# BaseView使用示范

```python
"""
接口定义 project/routers/some_module/some_module_api.py
"""
from fastapi import Query, Body

from fastapi_libs.base_view.base_view import BaseView, ResponseView
from fastapi_libs.const._enum import Method
from fastapi_libs.const.struct import Error


class ExampleView(BaseView):
    def __init__(self):
        super().__init__(
            path=".example.get",
            methods=[Method.get, Method.post],
            summary="示例接口"
        )

    @ResponseView
    async def as_view(
        self,
        query_string: int = Query(...),
        body_json: Dict = Body(...)
    ):
        if some_error:
            return Error.the_error_node
        # do some logic
        res = dict()
        return res


"""
接口暴露 project/routers/some_module/__init__.py
"""
from project.routers.some_module import some_module_api
some_module_api.ExampleView().bind_router(router)
```

# BaseModel使用示范

```python
"""
model定义 project/models/some_module/my_model.py
"""
from tortoise import fields
from fastapi_libs.base_view.base_model import BaseOrmModel, CheckingModel
# tips: CheckingModel 是 BaseOrmModel 的子类


class MyModel(BaseOrmModel):
    """普通表"""
    id = fields.IntField(pk=True, description="ID")

    class Meta:
        app = "my_app"
        table = "my_table_name"

    def to_dict(self, *args, **kwargs):
        """to_dict重写示范"""
        dic = super().to_dict(*args, **kwargs)
        dic["my_key"] = "my_value"
        return dic


class MyCheckingModel(CheckingModel):
    """检验字段名 检验查询条件"""
    id = fields.IntField(pk=True, description="ID")

    valid_conditions = [
        ["id"],
        ["pk"]
    ]

    class Meta:
        app = "my_app"
        table = "my_table_name"


"""
开启model检查 project/__init__.py
"""
from fastapi_libs import Setup
from project.constants.common import SERVICE_NAME, BASE_DIR

app = FastAPI(）


@app.on_event('startup')
async def startup_event():
    await Setup.model_check(
        f"{BASE_DIR}/{SERVICE_NAME}/models",
        f"{SERVICE_NAME}.models"
    )

```

# BaseManager使用示范

```python
"""
Manager定义
"""
from fastapi_libs import BaseManager
from fastapi_libs.decorators import singleton

from project.models.some_moudle.my_model import MyModel


@singleton
class MyModelManager(BaseManager):
    def __init__(self):
        super().__init__(MyModel)

    def exposed_api_keys(self):
        """自定义ManagerApi暴露配置"""
        return [
            "create", "bulk_create", "update", "get", "filter", "filter_page",
            "filter_values"
        ]


# 给model设置manager属性
MyModel.manager = MyModelManager()
# 方式2
# MyModel.set_manager(MyModelManager())

```

# ManagerApi使用示范

```python
"""
ManagerApi是基于BaseOrmModel和BaseManager的
所以想要使用ManagerApi的model，必须继承自BaseOrmModel
project/__init__.py
"""
from fastapi_libs import Setup
from project.constants.common import SERVICE_NAME, BASE_DIR

app = FastAPI()


@app.on_event('startup')
async def startup_event():
    await Setup.init_mgr_api(
        app,
        f"{BASE_DIR}/{SERVICE_NAME}/models",
        f"{SERVICE_NAME}.models"
    )

```
