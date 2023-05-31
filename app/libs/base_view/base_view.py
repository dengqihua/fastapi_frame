import abc
import logging
import time
from functools import wraps
from typing import Dict

from fastapi.routing import APIRoute
from starlette.background import BackgroundTasks
from starlette.requests import Request
from starlette.responses import Response

from app.libs.const import ErrorNode, Method

logger = logging.getLogger(__name__)


class GlobalDenpends:
    """写法1"""

    def __init__(
            self,
            request: Request,
            response: Response,
            background_tasks: BackgroundTasks
    ):
        self.request = request
        self.response = response
        self.background_tasks = background_tasks


# class GlobalDenpends(BaseModel):
#     """写法2"""
#     request: Request
#     response: Response
#     background_tasks: BackgroundTasks
#
#     class Config:
#         arbitrary_types_allowed = True


class ResponseView(object):

    def __call__(self, func):
        @wraps(func)
        async def decorated(view, *args, **kwargs):
            self.view = view
            result = await func(view, *args, **kwargs)
            if isinstance(result, ErrorNode):
                return self.fail(result)
            return self.success(result)

        return decorated

    def success(self, data):
        return self.response(data)

    def fail(self, error_node):
        return self.response(**error_node.to_dict())

    def response(self, data: Dict = None, code="0000", message="SUCCESS"):
        if data is None:
            data = dict()
        if not isinstance(data, dict):
            logger.exception(f"{self.view.__class__.__name__} 返回值类型异常")
            data = {
                "temp_data": data
            }
        now_ts = int(time.time())  # 服务器时间
        return dict(
            now_ts=now_ts,
            code=code,
            message=message,
            data=data
        )


class BaseView(metaclass=abc.ABCMeta):
    def __init__(
            self,
            path,
            response_model=None,
            dependencies=None,
            summary=None,
            methods=None,
            deprecated=False,
            **kwargs
    ):
        self.path = path
        self.end_point = self.as_view
        self.response_model = response_model
        self.dependencies = dependencies
        self.summary = summary
        self.methods = methods or [Method.get]
        self.deprecated = deprecated
        self.kwargs = kwargs

    def bind_router(self, router):
        route = APIRoute(
            path=self.path,
            endpoint=self.as_view,
            response_model=self.response_model,
            dependencies=self.dependencies,
            summary=self.summary,
            methods=self.methods,
            deprecated=self.deprecated,
            **self.kwargs
        )
        router.routes.append(route)

    @abc.abstractmethod
    async def as_view(
            self,
            *args,
            **kwargs
    ):
        ...
