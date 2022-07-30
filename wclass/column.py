import os
from tools import name_convert
import random
import string
import time
import re
from wclass.mapping import Mapping
from tools import  name_convert
from wclass.global_args import Global

# 表里一列


class Column(object):
    def __init__(self, name, type, length, post, put, list, about, sorter, zh, unique, mapping_json, index, sql_not_null, default):
        self.name = name
        self.type = type
        self.length = length
        self.post = post    # 0不用提交，1，可选提交，2必须提交
        self.put = put      # 0不用提交，1，可选提交，2必须提交
        self.list = list    # 0不用提交，1，严格等于查找，2模糊查找
        self.about = about or ""
        self.sorter = sorter
        self.zh = zh 
        self.index = index      # 用来做唯一辨识符的标签，为true时候，get和delete请求不再使用id，而使用它
        self.unique = unique    # 用来判断该值在哪个范围内唯一，global则是全局唯一
        self.not_null = sql_not_null
        self.default = default

        self.sql_null = ""
        if sql_not_null:    
            self.sql_null = " NOT NULL"
            self.post_must = True

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
            self.go_type = self.type +  (self.length or '')
            self.go_format          = "%d"
            self.type_long_lower    = "integer"
            self.empty              = 0
            self.ts_interface       = "number"
            self.protable_valuetype = "digit"
            self.yapi_format        = "integer"
            self.sql_type           = "INT"
        elif type == "uint":
            self.db = "Integer"
            self.go_type = self.type +  (self.length or '')
            self.go_format          = "%d"
            self.type_long_lower = "integer"
            self.empty = 0
            self.ts_interface = "number"
            self.protable_valuetype = "digit"
            self.yapi_format = "integer"
            self.sql_type           = "INT UNSIGNED"
        elif type == "float":
            self.db = "Float"
            self.go_type = self.type + (self.length or '')
            self.go_format          = "%f"
            self.type_long_lower = "float"
            self.empty = 0
            self.ts_interface = "number"
            self.protable_valuetype = "digit"
            self.yapi_format = "number"
            self.sql_type           = "FLOAT"
        elif type == "string":
            self.db = "String"
            self.go_type = "string"
            self.go_format          = "%s"
            self.type_long_lower = "string"
            self.empty = '""'
            self.ts_interface = "string"
            self.protable_valuetype = "text"
            self.yapi_format = "string"
            self.sql_type           = "VARCHAR"
        elif type == "datetime":
            self.db = "DateTime"
            self.go_type = "*time.Time"
            self.go_format          = "%v"
            self.type_long_lower = "datetime"
            self.empty = '""'
            self.ts_interface = "Date"
            self.protable_valuetype = "dateTime"
            self.yapi_format = "string"
            self.sql_type           = "DATETIME"
        elif type == "time":
            self.db = "DateTime"
            self.go_type = "*time.Time"
            self.go_format          = "%v"
            self.type_long_lower = "datetime"
            self.empty = '""'
            self.ts_interface = "Date"
            self.protable_valuetype = "dateTime"
            self.yapi_format = "string"
            self.sql_type           = "TIME"
        elif type == "date":
            self.db = "Date"
            self.go_type = "*time.Time"
            self.go_format          = "%v"
            self.type_long_lower = "date"
            self.empty = '""'
            self.ts_interface = "Date"
            self.protable_valuetype = "date"
            self.yapi_format = "string"
            self.sql_type           = "DATE"
        elif type == "bool":
            self.db = "Boolean"
            self.go_type = "bool"
            self.go_format          = "%v"
            self.type_long_lower = "bool"
            self.empty = 'false'
            self.ts_interface = "boolean"
            self.protable_valuetype = "text"
            self.yapi_format = "boolean"
            self.sql_type           = "BOOLEAN"
        elif type == "text":
            self.db = "Text"
            self.go_type = "string"
            self.go_format          = "%s"
            self.type_long_lower = "text"
            self.empty = '""'
            self.ts_interface = "string"
            self.protable_valuetype = "text"
            self.yapi_format = "string"
            self.sql_type           = "TEXT"
        elif type == "json":
            self.db = "JSON"
            self.go_type = "interface{}"
            self.go_format          = "%v"
            self.type_long_lower = "text"
            self.empty = '""'
            self.ts_interface = "string"
            self.protable_valuetype = "text"
            self.yapi_format = "object"
            self.sql_type           = "JSON"
        else:
            self.db = type
            self.go_type = ""
            self.go_format          = "%s"
            self.empty = '""'
            self.type_long_lower = type
            self.protable_valuetype = type
            self.ts_interface = type
            self.yapi_format = type
            self.sql_type           = ""

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
            return self.random_time()


    def random_time(self):
        a1 = (2020, 4, 12, 0, 0, 0, 0, 0, 0)  # 设置开始日期时间元组（2020-04-12 00：00：00）
        a2 = (2020, 4, 13, 0, 0, 0, 0, 0, 0)  # 设置结束日期时间元组（2020-04-13 00：00：00）

        start = time.mktime(a1)  # 生成开始时间戳
        end = time.mktime(a2)  # 生成结束时间戳

        t = random.randint(start, end)      # 在开始和结束时间戳中随机取出一个
        date_touple = time.localtime(t)            # 将时间戳生成时间元组
        date_str = time.strftime("%Y-%m-%d %H:%M:%S", date_touple)
        return date_str

    def format_str(self, fm, tab_num=0):
        t = Global.TAB
        tab = "\t"
        s = ""

        def make_go_tag_binding(required, method=""):    
            binding = ""
            if required == 2:
                binding += "required,"
            if self.length and self.type == "string":
                binding += 'max=63,'
            if self.unique == "global":
                if method == "post":
                    binding += f'unique={self.table_names},'
            if binding.endswith(","):
                binding = binding[:-1]
            if binding:
                binding = f' binding:"{binding}"'
            return binding

        if fm == "list_commit":
            if self.list:
                pipei = ",支持精确匹配" if self.list == 1 else "，支持模糊匹配"
                sorter = ",支持排序" if self.sorter else ""
                s = f"{t*tab_num}{self.name} ({self.type} optional): {self.zh}{pipei}{sorter}{self.map_mean}\n"
        elif fm == "post_commit":
            if self.post:
                commit_need_str = "require" if self.post == 2 else "optional"
                s = f"{t*tab_num}{self.name} ({self.type}, {commit_need_str}): {self.zh}{self.map_mean}\n"
        elif fm == "put_commit":
            if self.put:
                commit_need_str = "require" if self.put == 2 else "optional"
                s = f"{t*tab_num}{self.name} ({self.type}, {commit_need_str}): {self.zh}{self.map_mean}\n"
        elif fm == "return_commit":
            s = f"{t*tab_num}{self.name} ({self.type} optional): {self.zh}{self.map_mean}\n"
        elif fm == "commit_table":
            s = f"{t*tab_num}{self.name}: {self.zh}\n"
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
                s = f"{t*tab_num}{self.table_name}.{self.name} = {self.name} or {self.table_name}.{self.name}\n"
        elif fm == "flask_model_detail":
            if self.name == "id":
                s += f"{t}id = db.Column(db.Integer, primary_key=True)\n"
            else:
                s += f"{t}{self.name} = db.Column(db.{self.db}"
                if self.length is not None and self.length != '' and self.type == 'string':
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
        # golang gin部分
        elif fm == "gin_api_service_count_valid":
            if self.list:
                binding = make_go_tag_binding(1,"list")
                s = f'{t*tab_num}{self.Name} {self.go_type} `json:"{self.name}"{binding}`\n'
        elif fm == "gin_api_create_valid":
            if self.post:
                binding = make_go_tag_binding(self.post, "post")
                s = f'{t*tab_num}{self.Name} {self.go_type} `json:"{self.name}"{binding}`\n'
        elif fm == "gin_api_update_valid":
            if self.put:
                binding = make_go_tag_binding(self.put, "put")
                s = f'{t*tab_num}{self.Name} {self.go_type} `json:"{self.name}"{binding}`\n'
        elif fm == "gin_api_query_list_valid":
            if self.list:
                s = f'{t*tab_num}{self.Name} {self.go_type} `form:"{self.name}"`\n'
        elif fm == "gin_api_service_list_param":
            if self.list:
                s = f'{t*tab_num}param.{self.Name},'
        elif fm == "gin_api_service_create_param":
            if self.post:
                s = f'{t*tab_num}param.{self.Name},'
        elif fm == "gin_api_service_update_param":
            if self.put:
                s = f'{t*tab_num}param.{self.Name},'
        elif fm == "gin_api_dao_list_args":
            if self.list:
                s = f'{t*tab_num}{self.name} {self.go_type},'
        elif fm == "gin_api_dao_create_args":
            if self.post:
                s = f'{t*tab_num}{self.name} {self.go_type},'
        elif fm == "gin_api_dao_update_args":
            if self.put:
                s = f'{t*tab_num}{self.name} {self.go_type},'
        elif fm == "gin_api_dao_list_model":
            if self.list:
                s = f'{t*tab_num}{self.Name}: {self.name},\n'
        elif fm == "gin_api_dao_create_model":
            if self.post:
                s = f'{t*tab_num}{self.Name}: {self.name},\n'
        elif fm == "gin_api_dao_update_model":
            if self.put:
                s = f'{t*tab_num}{self.Name}: {self.name},\n'
        elif fm == "gin_api_model_struct_arg":
            s = f'{tab*tab_num}{self.Name} {self.go_type} `json:"{self.name}"`\n'
        elif fm == "gin_api_model_count_sql_str":
            if self.list:
                s = f'{t*tab_num}if o.{self.Name} != "" {{\n'
                s += f'{t*tab_num}if where {{\n'
                s += f'{t*tab_num}{t}sqlStr += fmt.Sprintf("and {self.name} = \\\"%s\\\" ",o.{self.Name})\n'
                s += f'{t*tab_num}}} else {{\n'
                s += f'{t*tab_num}{t}sqlStr += fmt.Sprintf("where {self.name} = \\\"%s\\\" ",o.{self.Name})\n'
                s += f'{t*tab_num}{t}where = true \n'
                s += f'{t*tab_num}{t}}}\n'
                s += f'{t*tab_num}}}\n'
        elif fm == "gin_api_model_select_arg":
            s = f' `{self.name}`,'
        elif fm == "sql_create_col_name":
            if self.post:
                s = f' `{self.name}`,'
        elif fm == "go_sql_create_format_percent":
            if self.post:
                s = "'%s' ,"
        elif fm == "go_form_sql_create_format":
            if self.post:
                if self.type == "json":
                    s = f"{self.name}, "
                else:
                    s = f"form.{self.Name}, "
        elif fm == "gin_api_model_update_sql":
            if self.put:
                s = f' `{self.name}` = ?,'
        elif fm == "gin_api_model_create_sql_?":
            if self.post:
                s = ' ?,'
        elif fm == "gin_api_model_create_exec_arg":
            if self.post:
                s = f' o.{self.Name},'        
        elif fm == "gin_api_model_update_exec_arg":
            if self.put:
                s = f' o.{self.Name},'        
        elif fm == "gin_api_model_create_unique":
            if self.unique == "global":
                s = 'var id int\n'
                s += f'sqlStr := "select id from {self.table_names} where {self.name}=? "\n'
                s += f'err := db.QueryRow(sqlStr, o.{self.Name}).Scan(&id)\n'
                s += f'if id != 0 {{\n'
                s += f'	err := fmt.Errorf("参数%s重复", o.{self.Name})\n'
                s += f'	return 0, err\n'
                s += f'}}\n'
        elif fm == "gin_api_model_list_scan":
            s = f'&{self.table_name}.{self.Name}, '
        elif fm == "gin_api_model_get_scan":
            s = f'&o.{self.Name}, '
        elif fm == "gin_api_router_count":
            if self.list:
                s = f'{t*tab_num}{self.Name}: param.{self.Name},\n'

# go_dapr 内的文件处理    
    # mysql创建表一类sql语句文件
        elif fm == "go_gin_dapr_mysql_sql_create_args":
            auto_increment = " AUTO_INCREMENT" if self.name == "id" else ""
            length = f"({self.length})" if self.length else ""
            default = ""
            if self.default == "created_at":
                default = " DEFAULT CURRENT_TIMESTAMP"
            if self.default == "updated_at":
                default = " DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"

            s = f'{tab*tab_num}`{self.name}` {self.sql_type}{length}{self.sql_null}{auto_increment}{default} COMMENT \'{self.zh}\',\n'
        elif fm == "go_gin_dapr_mysql_sql_create_bind":
            s = "" 
            if self.name == "id":
                s = f"{tab*tab_num}PRIMARY KEY (`id`),\n"
            elif self.unique == "global":
                if self.index:
                    s = f"{tab*tab_num}UNIQUE INDEX (`{self.name}`),\n"
                else:
                    s = f"{tab*tab_num}UNIQUE KEY (`{self.name}`),\n"
        elif fm == "go_gin_dapr_repo_update_sql":
            if self.put:
                if self.type == "json":
                    s += f'\n    // 将转为string的json字段{self.name}拼入sql语句中进行更新\n'
                    s += f'{tab*tab_num}sqlvals = append(sqlvals, fmt.Sprintf(" `{self.name}` = \'%s\' ", {self.name}))\n'
                else:
                    s += f'\n    // 如果{self.name}字段不为空，拼入sql语句中进行更新\n'
                    s += f"{tab*tab_num}if 0 < len(form.{self.Name}) {{\n{t*(tab_num+1)}sqlvals = append(sqlvals, fmt.Sprintf(\" `{self.name}` = '{self.go_format}' \", form.{self.Name}))\n{tab*tab_num}}}\n"
    # 创建过程repo文件遇到JSON数据序列化
        elif fm == "go_gin_dapr_repo_create_marshal":
            s = ""
            if self.type == "json":
                s += f'    // form.{self.Name}为json数据，先将它进行序列化转为string再插入sql语句中\n'
                s += f'{tab*tab_num}data, err := json.Marshal(form.{self.Name})\n'
                s += f'{tab*tab_num}if err != nil {{\n'
                s += f'{tab*tab_num}	return err\n'
                s += f'{tab*tab_num}}}\n'
                s += f'\n    // 判断提交的{self.name}是否为空，为空时默认为{{}}\n'
                s += f'{tab*tab_num}var {self.name} string = string(data)\n'
                s += f'{tab*tab_num}if {self.name} == "null" {{\n'
                s += f'{tab*tab_num}	{self.name} = "{{}}"\n'
                s += f'{tab*tab_num}}}\n'
        # elif fm == "go_gin_dapr_repo_update_marshal":
        #     if self.type == "json":
        #         s += f'{tab*tab_num}data, err := json.Marshal(form.{self.Name})\n'
        #         s += f'{tab*tab_num}if err != nil {{\n'
        #         s += f'{tab*tab_num}	return err\n'
        #         s += f'{tab*tab_num}}}\n'
        #         s += f'{tab*tab_num}var {self.name} string = string(data)\n'
        #         s += f'{tab*tab_num}if {self.name} == "null" {{\n'
        #         s += f'{tab*tab_num}	{self.name} = "{{}}"\n'
        #         s += f'{tab*tab_num}}}\n'
        #         s += f'	sqlvals = append(sqlvals, fmt.Sprintf(" `{self.name}` = \'%s\' ", {self.name}))\n\n'
        elif fm == "go_gin_dapr_repo_get_unmarshal":
            if self.type == "json":
                s += f'\n    // 将格式为json的字段{self.name}解析后更新{self.table_Name}的{self.Name}字段\n'
                s += f'{tab*tab_num}var {self.name} map[string]interface{{}}\n'
                s += f'{tab*tab_num}err = json.Unmarshal([]byte(resp[0].{self.Name}.(string)), &{self.name})\n'
                s += f'{tab*tab_num}if err != nil {{\n'
                s += f'{tab*tab_num}	return nil, err\n'
                s += f'{tab*tab_num}}}\n'
                s += f'{tab*tab_num}resp[0].{self.Name} = {self.name}\n\n'
        elif fm == "go_gin_dapr_repo_list_sql_like":
            if self.list == 2:
                s += f'\n    // 如果有提交{self.name}，对其进行模糊查找\n'
                s += f'{tab*tab_num}if len(query.{self.Name}) > 0 {{\n'
                s += f'{tab*tab_num}    where = fmt.Sprintf(" WHERE NAME LIKE \'%%%s%%\'", query.Name)\n'
                s += f'{tab*tab_num}}}\n'
        elif fm == "go_gin_dapr_repo_list_sql_unmarshal_json":
            if self.type == "json":
                s += f'		var {self.name} map[string]interface{{}}\n'
                s += f'		if err := json.Unmarshal([]byte({self.table_name}.{self.Name}.(string)), &{self.name}); err != nil {{\n'
                s += '			logger.Error(err)\n'
                s += '		} else {\n'
                s += f'			{self.table_name}.{self.Name} = {self.name}\n'
                s += '		}\n'
                s += f'		{self.table_names} = append({self.table_names}, {self.table_name})\n'



        return s

