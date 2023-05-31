import logging
import re
from typing import Dict, List, Set, Tuple, Type, Union

from app.libs.base_view.base_model import BaseOrmModel
from app.libs.base_view.model_views.bulk_create_view import \
    BulkCreateModelView
from app.libs.base_view.model_views.create_view import CreateModelView
from app.libs.base_view.model_views.filter_page_view import \
    FilterPageModelView
from app.libs.base_view.model_views.filter_values_view import \
    FilterValuesModelView
from app.libs.base_view.model_views.filter_view import FilterModelView
from app.libs.base_view.model_views.get_view import GetModelView
from app.libs.base_view.model_views.update_view import UpdateModelView
from app.libs.decorators import singleton

logger = logging.getLogger(__name__)


class DangerOperation(Exception):
    """高危SQL 禁止执行"""

    def __init__(self, check_res, sql):
        super(DangerOperation, self).__init__(
            f"高危SQL 禁止执行 命中：[{check_res}] 原SQL：{sql}")


@singleton
class Managers(object):
    """manager集合"""
    ...
    # __slots__ = ()


class BaseManager(object):

    def __init__(self, model_cls=None):
        self.model_cls: Type[BaseOrmModel] = model_cls
        self.model_name = model_cls._meta.db_table
        self.__check_model_name()
        self.__check_conn()

    def __check_conn(self):
        if not hasattr(self.model_cls, 'read_conn'):
            setattr(self.model_cls, "read_conn", lambda: None)
        if not hasattr(self.model_cls, "write_conn"):
            setattr(self.model_cls, "write_conn", lambda: None)

    def __check_model_name(self):
        """
        如果Model没有指定表名 生成一个 用于ManagerApi的path
        大驼峰转下划线
        TableName -> _Table_Name -> _table_name -> table_name
        """
        if not self.model_name:
            model_name = re.sub(r'([A-Z])', r'_\1', self.model_cls.__name__)
            model_name = model_name.lower().strip('_')
            self.model_name = model_name

    @property
    def danger_keywords(self) -> Set:
        """高危操作检测关键字"""
        return {"delete", "drop", "select *"}

    def _mgr_api_mapping(self):
        """ManagerApi关联的View"""
        return {
            "create": CreateModelView,
            "bulk_create": BulkCreateModelView,
            "update": UpdateModelView,
            "get": GetModelView,
            "filter": FilterModelView,
            "filter_page": FilterPageModelView,
            "filter_values": FilterValuesModelView
        }

    def _default_exposed_api_keys(self):
        """默认的ManagerApi暴露配置"""
        return [
            "create", "bulk_create", "update", "get", "filter", "filter_page",
            "filter_values"
        ]

    def exposed_api_keys(self):
        """重写此方法 可修改自定义manager的api暴露配置"""
        return self._default_exposed_api_keys()

    def exposed_apis(self):
        return [self._mgr_api_mapping()[key] for key in self.exposed_api_keys()]

    async def create(self, to_create: Dict) -> Union[BaseOrmModel, None]:
        """
        创建一个
        """
        try:
            obj = await self.model_cls.create(
                **to_create,
                using_db=self.model_cls.write_conn()
            )
            logger.info(f"{self.model_cls.__name__}.create 创建成功 id: {obj.id}")
            return obj
        except Exception:
            logger.exception(f"{self.model_cls.__name__}.create 创建失败")
            return None

    async def bulk_create_old(self, to_creates: List[Dict], using_db=None) -> bool:
        """
        批量创建
        """
        if not to_creates:
            return False
        try:
            models = [self.model_cls(**to_create) for to_create in to_creates]
            using_db = using_db or self.model_cls.write_conn()
            await self.model_cls.bulk_create(models, using_db=using_db)
            logger.info(
                f"{self.model_cls.__name__}.bulk_create 批量创建成功 数量: {len(models)}")
            return True
        except Exception:
            logger.exception(f"{self.model_cls.__name__}.bulk_create 批量创建失败")
            return False

    async def bulk_create(self, to_creates: List[Dict], ignore_conflicts=False, **kwargs) -> bool:
        """
        批量创建新版本
        Tortoise 0.18.1版本后支持ignore_conflicts=True(忽略冲突)
        新版本功能拓展：https://tortoise.github.io/models.html?highlight=bulk_create
        """
        if not to_creates:
            return False
        try:
            models = [self.model_cls(**to_create) for to_create in to_creates]
            await self.model_cls.bulk_create(
                models,
                ignore_conflicts=ignore_conflicts,
                **kwargs
            )
            return True
        except Exception:
            logger.exception(f"{self.model_cls.__name__}.bulk_create 批量创建失败")
            return False

    async def update(self, model_id: int, to_update: Dict) -> bool:
        """
        更新一个
        """
        # 过滤值为None的情况
        # 1. 表设计时尽量不要使值为None
        # 2. 此处可以兼容更新记录时， Pydantic Model 的非必传字段默认为 None 的情况
        to_update = {
            k: v
            for k, v in to_update.items()
            if v is not None
        }
        if not to_update:
            return False
        obj = await self.get(model_id)
        if not obj:
            return False
        try:
            effect_rows = await self.model_cls \
                .filter(id=model_id) \
                .using_db(self.model_cls.write_conn()) \
                .update(**to_update)
            if effect_rows == 1:
                logger.info(
                    f"{self.model_cls.__name__}.update model_id: {model_id} to_update: {to_update}")
                return True
            return False
        except Exception:
            logger.exception(f"{self.model_cls.__name__}.update 更新失败")
            return False

    async def bulk_update(self, filter_params: Dict, to_update: Dict) -> int:
        """
        批量更新
        """
        # 过滤值为None的情况
        # 1. 表设计时尽量不要使值为None
        # 2. 此处可以兼容更新记录时， Pydantic Model 的非必传字段默认为 None 的情况
        to_update = {
            k: v
            for k, v in to_update.items()
            if v is not None
        }
        if not to_update:
            return 0
        try:
            effect_rows = await self.model_cls \
                .filter(**filter_params) \
                .using_db(self.model_cls.write_conn()) \
                .update(**to_update)
            return effect_rows
        except Exception:
            logger.exception(f"{self.model_cls.__name__}.update 更新失败")
            return 0

    async def get(self, model_id) -> BaseOrmModel:
        """
        主键单个查询
        """
        return await self.model_cls \
            .filter(pk=model_id) \
            .using_db(self.model_cls.read_conn()) \
            .first()

    async def filter(
            self, filter_params: Dict, orderings: List = ["id"]
    ) -> List[BaseOrmModel]:
        """
        条件筛选
        """
        try:
            return await self.model_cls \
                .filter(**filter_params) \
                .using_db(self.model_cls.read_conn()) \
                .order_by(*orderings)
        except Exception:
            logger.exception(f"{self.model_cls.__name__}.filter 筛选失败")
            return []

    async def filter_first(
            self, filter_params: Dict, orderings: List = ["id"]
    ) -> Union[BaseOrmModel, None]:
        """
        首条筛选：条件筛选 + 排序规则 + 取第一个
        """
        return await self.model_cls \
            .filter(**filter_params) \
            .using_db(self.model_cls.read_conn()) \
            .order_by(*orderings) \
            .first()

    async def filter_values(
            self, filter_params: Dict, values: List, orderings: List = ["id"]
    ) -> List[Dict]:
        """
        字段筛选：条件筛选 + 自定字段列表
        返属性字典列表
        """
        try:
            return await self.model_cls \
                .filter(**filter_params) \
                .using_db(self.model_cls.read_conn()) \
                .order_by(*orderings) \
                .values(*values)
        except Exception:
            logger.exception(f"{self.model_cls.__name__}.filter_values 筛选失败")
            return []

    async def filter_value(
            self, filter_params: Dict, value: str, orderings: List = ["id"]
    ) -> List:
        """
        单字段筛选：条件筛选 + 指定字段
        返字段值列表
        """
        try:
            return await self.model_cls \
                .filter(**filter_params) \
                .using_db(self.model_cls.read_conn()) \
                .order_by(*orderings) \
                .values_list(value, flat=True)
        except Exception:
            logger.exception(f"{self.model_cls.__name__}.filter_value 筛选失败")
            return []

    async def filter_page(
            self, filter_params: Dict, orderings: List = ["id"],
            offset: int = 0, limit: int = 10, values: List[str] = None
    ) -> List[BaseOrmModel]:
        """
        分页筛选：条件筛选 + 排序规则 + 条数限制
        """
        cur = self.model_cls \
            .filter(**filter_params) \
            .using_db(self.model_cls.read_conn()) \
            .order_by(*orderings) \
            .offset(offset) \
            .limit(limit)
        if values:
            cur = cur.values(*values)
        return await cur

    async def filter_values_page(
            self, filter_params: Dict, values: List, orderings: List = ["id"],
            offset: int = 0, limit: int = 10
    ) -> List[Dict]:
        """
        分页字段筛选：分页筛选 + 自定字段列表
        返属性字典
        """
        return await self.model_cls \
            .filter(**filter_params) \
            .using_db(self.model_cls.read_conn()) \
            .order_by(*orderings) \
            .offset(offset) \
            .limit(limit) \
            .values(*values)

    async def filter_count(self, filter_params: Dict) -> int:
        """
        Count统计
        """
        return await self.model_cls \
            .filter(**filter_params) \
            .using_db(self.model_cls.read_conn()) \
            .count()

    async def filter_existed(self, filter_params: Dict) -> bool:
        """
        存在性判断
        """
        return await self.model_cls \
            .filter(**filter_params) \
            .using_db(self.model_cls.read_conn()) \
            .exists()

    async def execute_sql(self, sql: str) -> Tuple:
        """
        sql 执行
        【force_index use_index，tortoise-orm==0.17.2才支持，可通过execute_sql方式使用】
        - 高危操作检测
        - 连接池区分
        """
        check_res = map(lambda x: x in sql.lower(), self.danger_keywords)
        if any(list(check_res)):
            raise DangerOperation(check_res, sql)
        # TODO: try catch, execute_many[Optional], execute_script[Optional]
        con = self.model_cls.db_conn()
        res = await con.execute_query(sql)
        return res
