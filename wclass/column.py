import os
from tools import name_convert
import random
import string
import time
from wclass.mapping import Mapping
from tools import  name_convert

# 表里一列


class Column(object):
    def __init__(self, name, type, length, post, put, list, about, sorter, mean, mapping_json):
        self.name = name
        self.type = type
        self.length = length
        self.post = post    # 0不用提交，1，可选提交，2必须提交
        self.put = put      # 0不用提交，1，可选提交，2必须提交
        self.list = list    # 0不用提交，1，严格等于查找，2模糊查找
        self.about = about
        self.sorter = sorter
        self.mean = mean
        self.Name = name_convert(name)
        self.mapping = []
        for a in mapping_json or []:
            m = Mapping(
                a.get('key'),
                a.get('value'),
            )
            self.mapping.append(m)        
        self.map_mean = ""
        for m in self.mapping:
            self.map_mean += f", {m.key}{m.value}"
        if type == "int":
            self.db = "Integer"
            self.type_long_lower = "integer"
            self.empty = 0
            self.ts_interface = "number"
            self.protable_valuetype = "digit"
        elif type == "bigint":
            self.db = "BIGINT"
            self.empty = 0
            self.ts_interface = "number"
            self.protable_valuetype = "digit"
        elif type == "float":
            self.db = "Float"
            self.type_long_lower = "float"
            self.empty = 0
            self.ts_interface = "number"
            self.protable_valuetype = "digit"
        elif type == "str":
            self.db = "String"
            self.type_long_lower = "string"
            self.empty = '""'
            self.ts_interface = "string"
            self.protable_valuetype = "text"
        elif type == "time":
            self.db = "DateTime"
            self.type_long_lower = "datetime"
            self.empty = '""'
            self.ts_interface = "Date"
            self.protable_valuetype = "dateTime"
        elif type == "date":
            self.db = "Date"
            self.type_long_lower = "date"
            self.empty = '""'
            self.ts_interface = "Date"
            self.protable_valuetype = "date"
        elif type == "bool":
            self.db = "Boolean"
            self.type_long_lower = "bool"
            self.empty = 'false'
            self.ts_interface = "boolean"
            self.protable_valuetype = "text"
        elif type == "text":
            self.db = "Text"
            self.type_long_lower = "text"
            self.empty = '""'
            self.ts_interface = "string"
            self.protable_valuetype = "text"
        else:
            self.db = type
            self.empty = '""'
            self.type_long_lower = type
            self.protable_valuetype = type
            self.ts_interface = type

    def make_mean(self, tab_num):
        t = "    "
        return f"{t*tab_num}{self.name}({self.type}):{self.mean},\n"

    def format_str(self, fm, tab_num):
        t = "    "
        s = ""

        if fm == "list_commit":
            if self.list:
                pipei = ",支持精确匹配" if self.list == 1 else "，支持模糊匹配"
                sorter = ",支持排序" if self.sorter else ""
                s = f"{t*tab_num}{self.name} ({self.type} optional): {self.mean}{pipei}{sorter}{self.map_mean}\n"
        elif fm == "post_commit":
            if self.post:
                commit_need_str = "require" if self.post == 2 else "optional"
                s = f"{t*tab_num}{self.name} ({self.type}, {commit_need_str}): {self.mean}{self.map_mean}\n"
        elif fm == "put_commit":
            if self.put:
                commit_need_str = "require" if self.put == 2 else "optional"
                s = f"{t*tab_num}{self.name} ({self.type}, {commit_need_str}): {self.mean}{self.map_mean}\n"
        elif fm == "return_commit":
            s = f"{t*tab_num}{self.name} ({self.type} optional): {self.mean}{self.map_mean}\n"
        elif fm == "commit_table":
            s = f"{t*tab_num}{self.name}: {self.mean}\n"
        elif fm == "flask_api_post_request":
            if self.post:
                s = f"{t*tab_num}{self.name} = request.json.get('{self.name}')\n"
                if self.post == 2:
                    s += f"{t*tab_num}if {self.name} is None:\n"
                    s += f"{t*(tab_num+1)}return jsonify({{'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：{self.name}'}})\n"
        elif fm == "flask_api_post_equal":
            if self.post:
                s = f"{t*tab_num}{self.name}={self.name},\n"
        elif fm == "flask_api_put_request":
            if self.put:
                s = f"{t*tab_num}{self.name} = request.json.get('{self.name}')\n"
        elif fm == "flask_api_put_equal":
            if self.put:
                s = f"{t*tab_num}{self.table_lower_name}.{self.name} = {self.name} or {self.table_lower_name}.{self.name}\n"
        elif fm == "flask_model_detail":
            if self.name == "id":
                s += f"{t}id = db.Column(db.Integer, primary_key=True)\n"
            else:
                s += f"{t}{self.name} = db.Column(db.{self.db}"
                if self.length is not None and self.length != '' and self.type == 'str':
                    s += f"({self.length})"
                elif self.name == "created_at" or self.name == "updated_at":
                    s += ", default=datetime.utcnow"
                s += ")\n"
                
        elif fm == "flask_model_to_json":
            if self.type == 'time':
                s += f"{t*tab_num}'{self.name}': utc_switch(self.{self.name}),\n"
            elif self.type == 'date':
                s += f"{t*tab_num}'{self.name}': self.{self.name}.strftime('%Y-%m-%d') if self.{self.name} else None,\n"
            # elif self.file:
            #     s += f"""{t*tab_num}'{self.name}_url': f"{{static_host}}/{self.name}{self.name}/{{self.id}}/"+self.{self.name} if self.{self.name} else None,\n"""
            #     s += f"""{t*tab_num}'{self.name}': self.{self.name},\n"""
            else:
                s += f"{t*tab_num}'{self.name}': self.{self.name},\n"
        return s


    # 判断column的时间单位，根据情况添加
    def handle_time_str(self, name):
        if self.name == "modified_on":
            return f"    {name}.{self.name} = datetime.now()\n"
        return ""

    def random_arg(self):
        if self.type == 'str':
            if "name" in self.name:
                return f"XX{self.table_zh_name}{random.randint(1,9)}"
            return ''.join(random.sample(string.ascii_letters + string.digits, 8))
        if self.type == 'text':
            if "about" in self.name:
                return f"这是一段有关{self.table_zh_name}的描述：" + ''.join(random.sample(string.ascii_letters + string.digits, 28)) + "..."
            return ''.join(random.sample(string.ascii_letters + string.digits, 8))
        elif self.type == "float":
            return round(random.uniform(1, 100), 3)
        elif self.type == "bool":
            return random.randint(0, 1)
        elif self.type == "int":
            if self.mapping:
                return random.randint(0, len(self.mapping))
            return random.randint(0, 9)
        elif self.type == "time":
            return random_time()


def random_time():
    a1 = (2020, 4, 12, 0, 0, 0, 0, 0, 0)  # 设置开始日期时间元组（2020-04-12 00：00：00）
    a2 = (2020, 4, 13, 0, 0, 0, 0, 0, 0)  # 设置结束日期时间元组（2020-04-13 00：00：00）

    start = time.mktime(a1)  # 生成开始时间戳
    end = time.mktime(a2)  # 生成结束时间戳

    t = random.randint(start, end)      # 在开始和结束时间戳中随机取出一个
    date_touple = time.localtime(t)            # 将时间戳生成时间元组
    date_str = time.strftime("%Y-%m-%d %H:%M:%S", date_touple)
    return date_str
