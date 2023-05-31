# _*_ coding: utf-8 _*_
# @创建时间：2023/4/24 13:47
# @作者：dengqihua
# @名称 : auto_create_model.py
# @描述 : 自动创建model和mangers文件
import argparse
import asyncio
import os
import re
from datetime import datetime

from tortoise import Tortoise
from app.config.setting import settings

current_dir_path = os.path.dirname(os.path.abspath(__file__))
app_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AutoCreateModelHandle:

    def __init__(self, _args):
        # 数据库名称
        self.database = _args.databse
        # 生成数据的表名
        self.table = _args.table
        # 是否强制覆盖已存在的文件
        self.force = _args.force

    async def run(self):
        await self.db_init()
        if self.table == '*':
            tables = await self.get_all_tables()
        else:
            tables = [{f'Tables_in_{self.database}': self.table}]

        for table in tables:
            table_name = list(table.values())[0]
            # 转换成大驼峰命名格式
            pascal_case_table_name = ''.join(name.capitalize() for name in table_name.split('_'))

            table_comment = await self.get_table_comment(table_name)
            columns = await self.get_table_structure(table_name)
            fields_comment_dict = await self.get_fields_comment(table_name)

            fields_str = ''
            for column in columns:
                field_name = column['Field']
                # 过滤不需要的字段
                if field_name in ['id', 'status', 'create_time', 'update_time']:
                    continue

                field_type = column['Type']

                default_str = null_str = max_digits = decimal_places = ''
                if column['Null'] == 'YES':
                    null_str = 'null=True, '
                else:
                    default_str = f"default='{column['Default']}', " if column['Default'] is not None else ''

                max_length_str = ''
                description_str = 'description="' + fields_comment_dict.get(field_name, '') + '"'
                if field_type.startswith('int') or field_type.startswith('tinyint') or field_type.startswith('smallint') or field_type.startswith('bigint'):
                    field = 'IntField'
                elif field_type.startswith('varchar') or field_type.startswith('char'):
                    # 通过正则表达式，获取长度
                    result = re.findall(r'\d+', field_type)
                    length = int(result[0]) if result else 255
                    max_length_str = f'max_length={length}, '
                    field = f'CharField'
                elif field_type.startswith('json'):
                    field = 'JSONField'
                elif field_type.startswith('text') or field_type.startswith('longtext'):
                    field = 'TextField'
                elif field_type.startswith('float'):
                    field = 'FloatField'
                elif field_type.startswith('double'):
                    field = 'DoubleField'
                elif field_type.startswith('datetime'):
                    field = 'DatetimeField'
                elif field_type.startswith('timestamp'):
                    field = 'DatetimeField'
                elif field_type.startswith('decimal'):
                    field = 'DecimalField'
                    result = re.findall(r'\d+', field_type)
                    max_digits = f'max_digits={int(result[0])}, '
                    decimal_places = f'decimal_places={int(result[1])}, '
                else:
                    field = 'CharField'
                fields_str += f'    {field_name} = fields.{field}({max_length_str}{default_str}{max_digits}{decimal_places}{null_str}{description_str})\n'

            tpl_dict = {
                'table_name': table_name,
                'model_description': f'{table_comment}模型类',
                'manager_description': f'{table_comment}Manager类',
                'pascal_case_table_name': pascal_case_table_name,
                'fields_str': fields_str,
                'now_date': datetime.now().strftime('%Y/%m/%d %H:%M')
            }

            await asyncio.gather(
                # 写入model
                self.write_model_file(tpl_dict, table_name),
                # 写入manager
                self.write_manager_file(tpl_dict, table_name)
            )

        await self.write_init_content()
        await Tortoise.close_connections()
        print('自动创建表模型文件完成')

    async def db_init(self):
        """
        数据库初始化
        """

        await Tortoise.init(
            db_url=f'mysql://root:{settings.mysql_password}@{settings.mysql_host}:{settings.mysql_port}/{self.database}',
            modules={'models': ['__main__']},
        )

    async def get_all_tables(self):
        """
        获取数据库所有表
        """
        total, tables = await Tortoise.get_connection('default').execute_query('SHOW TABLES;')
        return tables

    async def get_table_structure(self, table_name):
        """
        获取表的结构信息
        """
        total_field, columns = await Tortoise.get_connection('default').execute_query(f"DESCRIBE `{table_name}`;")
        return columns

    async def get_fields_comment(self, table_name):
        """
        获取字段的注释信息
        """
        sql = f'SELECT COLUMN_NAME, COLUMN_COMMENT FROM information_schema.COLUMNS WHERE TABLE_SCHEMA="{self.database}" AND TABLE_NAME = "{table_name}"'
        total, data = await Tortoise.get_connection('default').execute_query(sql)
        comment_dict = {}
        for value in data:
            comment_dict[value['COLUMN_NAME']] = value['COLUMN_COMMENT']
        return comment_dict

    async def get_table_comment(self, table_name):
        """
        获取表注释信息
        """
        sql = f'SELECT TABLE_COMMENT FROM information_schema.TABLES WHERE TABLE_SCHEMA = "{self.database}" AND TABLE_NAME = "{table_name}"'
        total, data = await Tortoise.get_connection('default').execute_query(sql)
        return data[0]['TABLE_COMMENT']

    async def write_init_content(self):
        """
        写入模型目录的__init__文件
        """
        model_file_path = f'{app_dir_path}/models/'
        model_init_content = ''
        for root, dirs, files in os.walk(model_file_path):
            for file in files:
                if file.endswith('_model.py'):
                    file_name = file.split('.py')[0]
                    model_init_content += f'from .{file_name} import * \n'

        model_file_path = f'{app_dir_path}/models/__init__.py'
        with open(model_file_path, 'w', encoding='utf-8') as f:
            f.write(model_init_content)

        print('写入模型目录的__init__.py文件成功！')

    async def write_model_file(self, tpl_dict, table_name):
        """ 将model模板内容替换后写入model文件 """
        model_file_name = f'{table_name}_model'
        model_file_path = f'{app_dir_path}/models/{model_file_name}.py'

        # 如果文件存在，但不强制覆盖，则跳过执行
        if os.path.exists(model_file_path) and self.force == 0:
            return None

        model_tpl_file_path = f'{current_dir_path}/tpl/model_template.tpl'
        with open(model_tpl_file_path, encoding='utf-8') as f:
            model_tpl_content = f.read()

        # 替换模板文件内容后，重新写入文件
        model_tpl_content = model_tpl_content.format(**tpl_dict)
        with open(model_file_path, 'w', encoding='utf-8') as f:
            f.write(model_tpl_content)

        print(f'写入model文件：{model_file_name}.py 成功！')

    async def write_manager_file(self, tpl_dict, table_name):
        """ 将manager模板内容替换后写入manager文件  """
        manager_file_name = f'{table_name}_manager'
        manager_file_path = f'{app_dir_path}/managers/{manager_file_name}.py'

        # 如果文件存在，但不强制覆盖，则跳过执行
        if os.path.exists(manager_file_path) and self.force == 0:
            return None

        manager_tpl_file_path = f'{current_dir_path}/tpl/manager_template.tpl'
        with open(manager_tpl_file_path, encoding='utf-8') as f:
            manager_tpl_content = f.read()

        # 替换模板文件内容后，重新写入文件
        manager_tpl_content = manager_tpl_content.format(**tpl_dict)
        with open(manager_file_path, 'w', encoding='utf-8') as f:
            f.write(manager_tpl_content)
        print(f'写入manager文件：{manager_file_name}.py 成功！')


if __name__ == '__main__':
    arg_parse = argparse.ArgumentParser(description='根据数据库表结构，自动生成model、manager文件')
    arg_parse.add_argument('--table', type=str, default='*', help='表名，默认值：*，代表全部表, 举例：--table=user')
    arg_parse.add_argument('--databse', type=str, default='test', help='数据库名称，默认值：test，如：--databse=test')
    arg_parse.add_argument('--force', type=int, default=0, help='是否强制覆盖已存在的文件，默认值：0，参数解释：0 不覆盖，1 强制覆盖')
    args = arg_parse.parse_args()
    asyncio.run(AutoCreateModelHandle(_args=args).run())
