import importlib
import inspect
import os
from typing import List


async def get_modules_from_path(package_path, package_name, suffix=None) -> List[str]:
    module_list = []
    dirs = os.listdir(package_path)
    for _dir in dirs:
        if _dir.startswith('__'):
            continue
        if suffix and not _dir.endswith(suffix):
            continue
        # file_name = file
        if os.path.isfile(f"{package_path}/{_dir}"):
            file_name = _dir[:-3]
            imp_module = package_name + '.' + file_name
            module_list.append(imp_module)
        else:
            _module_list = await get_modules_from_path(f"{package_path}/{_dir}", f"{package_name}.{_dir}", suffix=suffix)
            module_list.extend(_module_list)
    return module_list


async def get_classes_from_module(ip_module, parent_cls=None, abs_method="", cls_suffix=None):
    classes = []
    for cls_name in dir(ip_module):
        if cls_name.startswith('__'):
            continue
        if cls_suffix and not cls_name.endswith(cls_suffix):
            continue
        target_cls = getattr(ip_module, cls_name, None)
        if not target_cls or not inspect.isclass(target_cls) or inspect.isabstract(target_cls):
            continue
        if parent_cls and (not issubclass(target_cls, parent_cls) or target_cls is parent_cls):
            continue
        if abs_method:
            _method = getattr(target_cls, abs_method, None)
            if not _method:
                temp_error = f"{target_cls} is sub class of {parent_cls} . but has not implemented function: {abs_method}"
                raise ValueError(temp_error)

        classes.append(target_cls)
    return classes


async def get_classes_from_package(package_path, package_name, parent_cls=None, abs_method="", file_suffix=None, cls_suffix=None, exclude_cls=None) -> list:
    """
    从指定位置提取符合条件的class
    Args:
        package_path: 指定位置的绝对路径，必须，用于os.dir
        package_name: 指定位置的包名，必须，用于import_lib
        parent_cls: 目标类需要继承自此父类
        abs_method: 目标类需要实现此方法
        file_suffix: 目标类所处文件需要包含此后缀
        cls_suffix: 目标类名需要包含此后缀
    Returns:
        包含目标类的列表 List[class]
    Example:
        获取某项目models包下的所有ORM Model
        classes = get_classes_from_package(
            module_path="/User/root/projects/project_name/app_name/models",
            package_name="app_name.models",
            parent_cls=tortoise.models.Model
        )
    """
    module_list = await get_modules_from_path(package_path, package_name, file_suffix)
    classes = []
    for module in module_list:
        # 处理windows下相对路径问题
        module = module.replace('...', '').replace('..', '.')
        ip_module = importlib.import_module(module)
        module_classes = await get_classes_from_module(ip_module, parent_cls, abs_method=abs_method, cls_suffix=cls_suffix)
        classes.extend(module_classes)
    if exclude_cls:
        classes = [clz for clz in classes if clz not in exclude_cls]
    return classes
