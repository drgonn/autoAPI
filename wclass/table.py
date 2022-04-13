import os
from wclass.parent import Parent, Many, Son
from tools import name_convert
from wclass.column import Column
import json
import random
import re
import datetime
import time
from wclass.global_args import Global

tab = Global.TAB


# 单表
class Table(object):
    def __init__(self, table_class, api_need, table_zh, table_about, url_prefix, repr, arg_json, parent_json, many_json, sons_json):
        self.Name = table_class
        self.api_need = api_need
        self.zh_name = table_zh
        self.about = table_about
        self.url_prefix = url_prefix
        self.repr = repr

        self.name = name_convert(self.Name)
        self.names = self.name + "s"
        self.columns = []
        self.many = []
        self.parents = []
        self.sons = []
        self.index = None

        now = datetime.datetime.now() - datetime.timedelta(days=1)
        self.now = time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))
        self.now_date = now.strftime('%Y/%m/%d')

        for a in arg_json:
            column = Column(
                a.get('name'),
                a.get('type'),
                a.get('length'),
                a.get('post'),
                a.get('put'),
                a.get('list'),
                a.get('about'),
                a.get('sorter'),
                a.get('mean'),
                a.get('unique'),
                a.get('mapping'),
                a.get('index'),
                a.get('not_null'),
                a.get("default")
            )
            column.table_zh_name = table_zh
            column.table_Name = self.Name
            column.table_name = self.name
            column.table_names = self.names
            if column.name == "id":
                self.index = column
            if column.index:
                self.index = column
            self.columns.append(column)
        for parnet in parent_json:
            p = Parent(
                parnet.get("name"),
                parnet.get("index"),
                parnet.get("post"),
                parnet.get("put"),
                parnet.get("list"),
                parnet.get("mean"),
                parnet.get("show"),
            )
            p.table_Name = self.Name
            p.table_name = self.name
            p.table_names = self.names
            self.parents.append(p)
        for many in many_json or []:
            m = Many(
                many.get("name"),
                many.get("w_model"),
                many.get("add_api"),
                many.get("mean"),
                many.get("prefix"),
            )
            m.table_Name = self.Name
            m.table_name = self.name
            m.table_names = self.names
            self.many.append(m)
        for son in sons_json or []:
            s = Son(
                son.get("name"),
                son.get("to_json"),
                son.get("add"),
            )
            self.sons.append(s)


    # 生成url地址
    def format_table_str(self, format):
        prefix = "/"+self.url_prefix if self.url_prefix else ""
        table_map = {
            "flask_api_route_get": f"\n@api.route('{prefix}/{self.name}/<int:id>', methods=['GET'])\n",
            "flask_api_route_post": f"\n@api.route('{prefix}/{self.name}', methods=['POST'])\n",
            "flask_api_route_put": f"\n@api.route('{prefix}/{self.name}/<int:id>', methods=['PUT'])\n",
            "flask_api_route_delete": f"\n@api.route('{prefix}/{self.name}', methods=['DELETE'])\n",
            "flask_api_route_list": f"\n@api.route('{prefix}/{self.name}/list', methods=['GET'])\n",
            "doc_url": ""
             
        }
        s = table_map.get(format)
        
        return s

    # 生成一列column的格式化字符串
    def make_column_format(self, fm, tabs=0):
        rs = ''
        for column in self.columns:
            rs += column.format_str(fm, tabs)
        return rs

    def make_parent_format(self, fm, tabs):
        rs = ''
        for parent in self.parents:
            rs += parent.format_str(fm, tabs)
        return rs

    def make_many_format(self, fm, tabs):
        rs = ''
        for m in self.many:
            rs += m.format_str(fm, tabs)
        return rs

    # 生成flask文件app下的api文件
    # 生成api文件的import行列表
    def make_import_list(self):
        im = "import json\nimport logging\nimport math\nimport os\nimport shutil\n\nfrom app import db\nfrom app.apiv1 import api\nfrom flask import request, jsonify, current_app, g\nfrom sqlalchemy import func\n"
        import_list = []
        import_list.append(im)        

        if self.many != []:
            for m in self.many:
                import_list.append(f"from app.models.{m.name} import {m.Name}\n")
        import_list.append("\n")
        for parent in self.parents:
            import_list.append(f"from app.models.{parent.name} import {parent.Name}\n")
        import_list.append("\n\n")
        return import_list

    # 生成api文件的import行列表
    def make_api_get_list(self):
        api_get_list = []
        commit_get_list = []
        api_get_list.append(self.format_table_str("flask_api_route_get"))
        api_get_list.append(f"def get_{self.name}(id):\n")
        commit_get_list.append(f'{tab*1}"""get单个{self.zh_name}接口\n')
        commit_get_list.append(f'\n{tab*1}Params:\n')
        commit_get_list.append(f'{tab*2}id (int, require): {self.zh_name}ID\n')
        commit_get_list.append(f'\n{tab*1}Returns:\n')
        commit_get_list.append(f'{tab*2}success (bool): 请求成功与否\n')
        commit_get_list.append(f'{tab*2}error_code (int): 错误代码，无错为0\n')
        commit_get_list.append(f'{tab*2}records (json): {self.zh_name}的详细参数\n')
        commit_get_list.append(self.make_column_format("return_commit",3))
        for son in self.sons:
            son = self.table_map.get(son.Name)
            commit_get_list.append(f'{tab*3}{self.names} (json): {self.zh_name}的子表{son.zh_name}详细参数\n')
            commit_get_list.append(son.make_column_format("return_commit",4))
        commit_get_list.append(f'{tab*1}"""\n')
        api_get_list.append(f"{tab}{self.name} = {self.Name}.query.get_or_404(id)\n")
        to_what = 'to_json'  # if table.get('nodetail') else 'to_detail'
        api_get_list.append(f"""\n{tab}return jsonify({{'success': True,
                    'error_code': 0,
                    'records': {self.name}.{to_what}(),
                    }})""")
        api_get_list.append(f"\n\n")    
        api_get_list[2:0] = commit_get_list
        return api_get_list

    # 生成api文件的import行列表
    def make_api_post_list(self):
        api_post_list = []
        commit_post_list = []

        api_post_list.append(self.format_table_str("flask_api_route_post"))
        api_post_list.append(f"def create_{self.name}():\n")
        commit_post_list.append(f'{tab*1}"""post创建单个{self.zh_name}接口\n')
        commit_post_list.append(f'\n{tab*1}Requests:\n')
        commit_post_list.append(f'\n{tab*1}Returns:\n')
        commit_post_list.append(f'{tab*2}success (bool): 请求成功与否\n')
        commit_post_list.append(f'{tab*2}error_code (int): 错误代码，无错为0\n')
        commit_post_list.append(f'{tab*2}id (int): {self.zh_name}主键ID\n')
        commit_post_list.append(f'{tab*1}"""\n')
        commit_post_list.insert(2, self.make_column_format("post_commit",2))
        commit_post_list.insert(2, self.make_parent_format("post_commit",2))
        api_post_list.append(f"{tab}print(request.json)\n")
        for son in self.sons:
            son = self.table_map.get(son.Name)
            commit_post_list.insert(2, f"{tab*2}add_{son.name}_ids (list, optional): 要添加的{son.zh_name}的主键id列表\n")

        api_post_list.append(self.make_column_format("flask_api_post_request", 1))

        api_post_list.append(self.make_parent_format("flask_api_post_verify", 1))
        # for parent in self.parents:
        #     elif parent.post:
        #         index = parent.index
        #         must = "，非必填"
        #         if parent.post ==2:
        #             must = "，必填"
                # commit_post_list.insert(2, f"{tab*2}{parent.name}_{parent.index} (int, {parent.commit_need_str}): {parent.mean}{must}\n")

        api_post_list.append(f"\n{tab}{self.name} = {self.Name}(\n")
        api_post_list.append(self.make_column_format("flask_api_post_equal", 2))
        api_post_list.append(self.make_parent_format("flask_api_post_equal", 2))
        api_post_list.append(f"{tab})\n")

        # for column in self.columns:
        #     if column.get('file'):
        #         api_post_list.append(f"""{tab}static_folder = current_app.config['STATIC_FOLDER']\n""")
        #         api_post_list.append(f"""{tab}user_dir = os.path.join(static_folder, 'user_folder', f"{{g.current_user.uid}}")\n""")
        #         api_post_list.append(f"""{tab}tmp_file_path = os.path.join(user_dir, {column.name})\n""")
        #         api_post_list.append(f"""{tab}if not os.path.exists(tmp_file_path):\n""")
        #         api_post_list.append(f"""{tab}{tab}return jsonify({{'success':False,'error_code':-1,'errmsg':f'文件{{tmp_file_path}}不存在'}})\n""")

        api_post_list.append(self.make_many_format("flask_api_post", 1))
        api_post_list.append(f"\n{tab}db.session.add({self.name})\n")
        api_post_list.append(f"{tab}try:\n{tab}{tab}db.session.commit()\n")
        # for column in self.columns:
        #     if column.get('file'):
        #         column.name = column.name
        #         api_post_list.append(f"""{tab}{tab}dst_dir = os.path.join(static_folder, '{self.name}{column.name}', f"{{{self.name}.id}}")\n""")
        #         api_post_list.append(f"""{tab}{tab}dst_file_path = os.path.join(dst_dir, {column.name})\n""")
        #         api_post_list.append(f"""{tab}{tab}os.makedirs(dst_dir,exist_ok=True)\n""")
        #         api_post_list.append(f"""{tab}{tab}shutil.move(tmp_file_path,dst_file_path)\n""")
        #         api_post_list.append(f"""{tab}{tab}shutil.rmtree(user_dir)\n""")

        api_post_list.append(f"{tab}except Exception as e:\n{tab}{tab}db.session.rollback()\n")
        api_post_list.append(f"{tab}{tab}logging.error(f'添加数据库发生错误,已经回退:{{e}}')\n")
        api_post_list.append(f"{tab}{tab}return jsonify({{'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'}})\n")
        api_post_list.append(f"""\n{tab}return jsonify({{'success': True,
                    'error_code': 0,
                    'id': {self.name}.id,
                    }})""")
        api_post_list.append(f"\n\n")


        api_post_list[2:0] = commit_post_list

        return api_post_list

    # 生成api文件的import行列表
    def make_api_put_list(self):
        api_put_list = []
        commit_put_list = []

        api_put_list.append(self.format_table_str("flask_api_route_put"))
        api_put_list.append(f"def modify_{self.name}(id):\n")        
        commit_put_list.append(f'{tab*1}"""put修改单个{self.zh_name}接口\n')
        commit_put_list.append(f'\n{tab*1}Requests:\n')
        commit_put_list.append(f'\n{tab*1}Returns:\n')
        commit_put_list.append(f'{tab*2}success (bool): 请求成功与否\n')
        commit_put_list.append(f'{tab*2}error_code (int): 错误代码，无错为0\n')
        commit_put_list.append(f'{tab*1}"""\n')
        commit_put_list.insert(2, self.make_column_format("put_commit",2))
        api_put_list.append(f"{tab}print(request.json)\n")
        for son in self.sons:
            son = self.table_map.get(son.Name)
            commit_put_list.insert(2, f"{tab*2}add_{son.name}_ids (list, optional): 要添加的{son.zh_name}的主键id列表\n")
            commit_put_list.insert(2, f"{tab*2}remove_{son.name}_ids (list, optional): 要删除的{son.zh_name}的主键id列表\n")

        api_put_list.append(f"{tab}{self.name} = {self.Name}.query.get_or_404(id)\n")
        api_put_list.append(self.make_column_format("flask_api_put_request", 1))

        for parent in self.parents:
            if parent.put:
                index = parent.index
                argname = f"{parent.name}_{parent.index}"
                api_put_list.append(f"{tab}{argname} = request.json.get('{argname}')\n")
                api_put_list.append(f"{tab}{parent.name} = {parent.Name}.query.filter_by({index}={argname}).first()\n")
                api_put_list.append(f"{tab}if {parent.name} is None:\n")
                api_put_list.append(f"""{tab}{tab}return jsonify({{'success':False,'error_code':-1,'errmsg':'{argname}不存在'}})""")
                api_put_list.append(f"{tab}\n")

        api_put_list.append(self.make_column_format("flask_api_put_equal", 1))
        for parent in self.parents:
            if parent.put:
                api_put_list.append(f"{tab}{self.name}.{parent.name}_id = {parent.name}.id\n")
        api_put_list.append(self.make_many_format("flask_api_put", 1))
        # if self.many:
        #     for many in self.many:
        #         if many.add_api:
        #             api_put_list.append(f"\n{tab}add_{many.name}_ids = request.json.get('add_{many.name}_ids')\n")
        #             api_put_list.append(f"{tab}if add_{many.name}_ids:\n")
        #             api_put_list.append(f"{tab}{tab}original_ids = [{many.name}.id for {many.name} in {self.name}.{many.name}s.all()]\n")
        #             api_put_list.append(f"{tab}{tab}new_ids = list(set(add_{many.name}_ids).difference(set(original_ids)))\n")
        #             api_put_list.append(f"{tab}{tab}for {many.name}_id in new_ids:\n")
        #             api_put_list.append(f"{tab}{tab}{tab}{many.name} = {many.Name}.query.filter_by(id={many.name}_id).first()\n")
        #             api_put_list.append(f"{tab}{tab}{tab}if {many.name} is None:\n")
        #             api_put_list.append(f"{tab}{tab}{tab}{tab}return jsonify({{'success':False,'error_code':-1,'errmsg':'{many.name}ID不存在'}})\n")
        #             api_put_list.append(f"{tab}{tab}{tab}{self.name}.{many.name}s.append({many.name})\n")

        #             api_put_list.append(f"\n{tab}remove_{many.name}_ids = request.json.get('remove_{many.name}_ids')\n")
        #             api_put_list.append(f"{tab}if remove_{many.name}_ids:\n")

        #             api_put_list.append(f"{tab}{tab}original_ids = [{many.name}.id for {many.name} in {self.name}.{many.name}s.all()]\n")
        #             api_put_list.append(f"{tab}{tab}remove_ids = list(set(remove_{many.name}_ids).intersection(set(original_ids)))\n")
        #             api_put_list.append(f"{tab}{tab}for {many.name}_id in remove_ids:\n")
        #             api_put_list.append(f"{tab}{tab}{tab}{many.name} = {many.Name}.query.filter_by(id={many.name}_id).first()\n")
        #             api_put_list.append(f"{tab}{tab}{tab}{self.name}.{many.name}s.remove({many.name})\n")
        #             api_put_list.append(f"{tab}{tab}\n")

        api_put_list.append(f"{tab}db.session.add({self.name})\n")
        api_put_list.append(f"\n{tab}try:\n{tab}{tab}db.session.commit()\n{tab}except Exception as e:\n{tab}{tab}db.session.rollback()\n")
        api_put_list.append(f"{tab}{tab}logging.error(f'修改数据库发生错误,已经回退:{{e}}')\n")
        api_put_list.append(f"""{tab}return jsonify({{'success':True,
                    'error_code':0,
                    }})""")
        api_put_list.append(f"\n\n")



        api_put_list[2:0] = commit_put_list

        return api_put_list

    # 生成api文件的import行列表
    def make_api_delete_list(self):
        api_delete_list = []
        commit_delete_list = []
    
        api_delete_list.append(self.format_table_str("flask_api_route_delete"))
        api_delete_list.append(f"def delete_{self.name}():\n")        
        commit_delete_list.append(f'{tab*1}"""delete删除多个{self.zh_name}接口\n')
        commit_delete_list.append(f'\n{tab*1}Params:\n')
        commit_delete_list.append(f'{tab*2}ids (list, require): 需要删除的{self.zh_name}ID主键列表，当包含关联子表时，会删除失败\n')
        commit_delete_list.append(f'\n{tab*1}Returns:\n')
        commit_delete_list.append(f'{tab*2}success (bool): 请求成功与否\n')
        commit_delete_list.append(f'{tab*2}error_code (int): 错误代码，无错为0\n')
        commit_delete_list.append(f'{tab*1}"""\n')
        api_delete_list.append(f"{tab}print('delete json:',request.json)\n")
        api_delete_list.append(f"{tab}ids = request.json.get('ids')\n")
        api_delete_list.append(f"{tab}for id in ids:\n")
        api_delete_list.append(f"{tab}{tab}{self.name} = {self.Name}.query.get(id)\n")
        api_delete_list.append(f"{tab}{tab}if {self.name} is None:\n")
        api_delete_list.append(f"""{tab}{tab}{tab}return jsonify({{'success': False, 'error_code': -123, 'errmsg': f'删除错误，id： {{id}} 不存在'}})\n""")

        # for table1 in self.ojson.get('databases'):
        #     if table1.get('parents'):
        #         for parent in table1.get("parents"):
        #             if parent.get("name") == self.Name:
        #                 api_delete_list.append(f"{tab}{tab}if {self.name}.{table1.get('table').lower()}s.first() is not None:\n")
        #                 api_delete_list.append(f"{tab}{tab}{tab}return jsonify({{'success':False,'error_code':-1,'errmsg':'{self.name}还拥有{table1.get('table').lower()}，不能删除'}})\n")

        api_delete_list.append(f"{tab}{tab}db.session.delete({self.name})\n")
        api_delete_list.append(f"\n{tab}try:\n{tab}{tab}db.session.commit()\n")
        # for column in self.columns:
        #     if column.get('file'):
        #         argname = column.name
        #         api_delete_list.append(f"""{tab}{tab}{tab}static_folder = current_app.config['STATIC_FOLDER']\n""")
        #         api_delete_list.append(f"""{tab}{tab}{tab}dst_dir = os.path.join(static_folder, '{self.name}', f"{{{self.name}.id}}")\n""")
        #         api_delete_list.append(f"""{tab}{tab}{tab}shutil.rmtree(dst_dir)\n""")
        api_delete_list.append(f"{tab}except Exception as e:\n{tab}{tab}db.session.rollback()\n")
        api_delete_list.append(f"{tab}{tab}logging.error(f'删除数据库发生错误,已经回退:{{e}}')\n")
        api_delete_list.append(f"""{tab}{tab}return jsonify({{'success': False, 'error_code': -123, 'errmsg': f'删除数据发生错误， {{e}} '}})\n""")
        api_delete_list.append(f"""\n{tab}return jsonify({{'success':True,
                'error_code':0,
                }})""")
        api_delete_list.append(f"\n\n")


        api_delete_list[2:0] = commit_delete_list

        return api_delete_list

    def make_api_list_list(self):
        api_list_list = []
        commit_list_list = []

        commit_list_list.append(f'{tab*1}"""get查询{self.zh_name}列表接口\n')
        commit_list_list.append(f'\n{tab*1}Args:\n')
        commit_list_list.append(f'{tab*2}page (int, optional): 指定过滤条件，页数Args:\n')
        commit_list_list.append(f'{tab*2}pageSize (int, optional): 指定过滤条件，单页最大个数Args:\n')
        commit_list_list.append(self.make_column_format("list_commit",2))
        commit_list_list.append(self.make_parent_format("list_commit",2))
        commit_list_list.append(f'\n{tab*1}Returns:\n')
        commit_list_list.append(f'{tab*2}success (bool): 请求成功与否\n')
        commit_list_list.append(f'{tab*2}error_code (int): 错误代码，无错为0\n')
        commit_list_list.append(f'{tab*2}data (list): {self.zh_name}的json列表\n')
        commit_list_list.append(self.make_column_format("return_commit",3))
        for son in self.sons:
            son = self.table_map.get(son.Name)
            commit_list_list.append(f'{tab*3}{self.names} (json): {self.zh_name}的子表{son.zh_name}详细参数\n')
            commit_list_list.append(son.make_column_format("return_commit",4))
        commit_list_list.append(f'{tab*1}"""\n')
        api_list_list.append(self.format_table_str("flask_api_route_list"))
        api_list_list.append(f"def list_{self.name}():\n")
        api_list_list.append(f"{tab}print(request.args)\n")
        api_list_list.append(f"{tab}sorter = request.args.get('sorter')\n")
        api_list_list.append(f"{tab}page = int(request.args.get('current', 1))\n")
        api_list_list.append(f"{tab}pageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))\n")
        api_list_list.append(f"{tab}pageSize = 20 if pageSize < 10 else pageSize\n")

        # if table.get('userfilter'):
        if False:
            api_list_list.append(f"\n{tab}if is_admin():\n")
            if table.get('appfilter'):
                api_list_list.append(f"{tab}{tab}total_{self.names} = {self.Name}.query.filter_by(app_id=g.app.id)\n")
            else:
                api_list_list.append(f"{tab}{tab}total_{self.names} = {self.Name}.query\n")
            api_list_list.append(f"{tab}else:\n")
            api_list_list.append(f"{tab}{tab}total_{self.names} = g.current_user.{self.names}\n")
        else:
            # if table.get('appfilter'):
            if False:
                api_list_list.append(f"{tab}total_{self.names} = {self.Name}.query.filter_by(app_id=g.app.id)\n")
            else:
                api_list_list.append(f"{tab}total_{self.names} = {self.Name}.query\n")

        api_list_list.append(self.make_many_format("flask_api_list", 1))
        for parent in self.parents:
            if parent.list:
                index = parent.index
                argname = f"{parent.name}_{parent.index}"
                api_list_list.append(f"\n{tab}{argname} = request.args.get('{argname}')\n")
                api_list_list.append(f"{tab}if {argname} is not None:\n")
                api_list_list.append(f"{tab}{tab}{parent.name} = {parent.Name}.query.filter_by({index}={argname}).first()\n")
                api_list_list.append(f"{tab}{tab}if {parent.name} is None:\n")
                api_list_list.append(f"""{tab}{tab}{tab}return jsonify({{'success':False,'error_code':-1,'errmsg':'{argname}不存在'}})\n""")
                api_list_list.append(f"{tab}{tab}else:\n{tab}{tab}{tab}total_{self.names} = total_{self.names}.filter_by({parent.name}_id={parent.name}.id)\n")


        for column in self.columns:
            filter = column.list
            # print(self.name,filter,column,table)
            if filter:
                argname = column.name
                api_list_list.append(f"{tab}{argname} = request.args.get('{argname}')\n")
                api_list_list.append(f"{tab}if {argname} is not None:\n")
                if filter == 2:
                    api_list_list.append(f"{tab}{tab}total_{self.names} = total_{self.names}.filter({self.Name}.{argname}.ilike(f'%{{{argname}}}%'))\n\n")
                elif filter == 1:
                    api_list_list.append(f"{tab}{tab}total_{self.names} = total_{self.names}.filter_by({argname}={argname})\n\n")
        api_list_list.append(f"{tab}if sorter:\n")
        api_list_list.append(f"{tab}{tab}sorter = json.loads(sorter)\n")

        for column in self.columns:
            if column.sorter:
                argname = column.name
                api_list_list.append(f"{tab}{tab}if sorter.get('{argname}') == 'ascend':\n")
                api_list_list.append(f"{tab}{tab}{tab}total_{self.names} = total_{self.names}.order_by({self.Name}.{argname}.asc())\n")
                api_list_list.append(f"{tab}{tab}elif sorter.get('{argname}') == 'descend':\n")
                api_list_list.append(f"{tab}{tab}{tab}total_{self.names} = total_{self.names}.order_by({self.Name}.{argname}.desc())\n")
        api_list_list.append(f"{tab}{tab}pass\n")
        api_list_list.append(f"{tab}totalcount = total_{self.names}.with_entities(func.count({self.Name}.id)).scalar()\n")
        api_list_list.append(f"{tab}page = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page\n")
        api_list_list.append(f"{tab}pagination = total_{self.names}.paginate(page, per_page = pageSize, error_out = False)\n")
        api_list_list.append(f"{tab}{self.names} = pagination.items\n")
        api_list_list.append(f"""\n{tab}return jsonify({{
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    "pageSize" : pageSize,
                    "current" : page,
                    "pagecount": pagination.pages,
                    'data':[{self.name}.to_json() for {self.name} in {self.names}]
                    }})""")
        api_list_list.append(f"\n")
        api_list_list.append(f"\n")


        api_list_list[2:0] = commit_list_list

        return api_list_list

    def write_api(self,appdir):
        if not self.api_need:
            return {}
        target_str_list = []
        import_list = self.make_import_list()
        api_get_list = self.make_api_get_list()
        api_post_list = self.make_api_post_list()
        api_put_list = self.make_api_put_list()
        api_delete_list = self.make_api_delete_list()
        api_list_list = self.make_api_list_list()
        apidir =  os.path.join(appdir, f'src/app/apiv1/{self.name}.py')

        # 加入导入包
        target_str_list += import_list
        target_str_list += api_get_list
        target_str_list += api_post_list
        target_str_list += api_put_list
        target_str_list += api_delete_list
        target_str_list += api_list_list

        return {apidir:target_str_list}


# 生成yapi测试文件
    def write_test_yapi(self,project_dir):
        r = []
        crud = [
                ("创建", "POST", ''),
                ("列表", "GET", '/list'),
                ("单个获取", "GET", '/<id>'),
                ("修改", "PUT", '/<id>'),
                ("删除", "DELETE", ''),
                ]
        if self.api_need:
            gp = {}
            gp['index'] = 0
            gp['name'] = self.zh_name
            gp['desc'] = self.zh_name
            gp['list'] = []            
            write_addr =  os.path.join(project_dir, f'test/yapi/{self.name}.json')
            son_list=[]
            for typezh, method, p in crud:
                prefix = "/"+self.url_prefix if self.url_prefix else ""
                path = f"{prefix}/{self.name}"
                req_query_list = []
            
                pjson = {"type":"object",
                        "title":"empty object",
                        "properties":
                            {
                            },
                        "required":[]
                        }
                getjson = {"type": "object",
                            "title": "empty object",
                            "properties":
                                {Global.RETURNBOOLNAME:
                                    {"type": "boolean",
                                    "description": "成功状态",
                                    "mock": {"mock": "true"}
                                    },
                                Global.RETURNINTNAME:
                                    {"type": "integer",
                                        "description": "错误码",
                                        "mock": {"mock": 0}
                                        },
                                Global.RETURNSTRNAME:
                                    {"type": "integer",
                                        "description": "错误信息",
                                        },
                                "record":
                                    {"type": "object",
                                    "properties": {
                                        "id": {"type": "integer", "description": "id"},
                                    },
                                    "required": ["id"]}
                                },
                            "required":[Global.RETURNBOOLNAME, Global.RETURNINTNAME, "record"]
                            }
                return_json = {"type": "object",
                        "title": "empty object",
                        "properties":
                            {
                                Global.RETURNBOOLNAME:
                                    {"type": "boolean",
                                    "description": "成功状态",
                                    "mock": {"mock": "true"}
                                    },
                                Global.RETURNINTNAME:
                                    {"type": "integer",
                                        "description": "错误码",
                                        "mock": {"mock": 0}
                                        },
                                Global.RETURNSTRNAME:
                                    {"type": "integer",
                                        "description": "错误信息",
                                        },

                        },
                        "required": [Global.RETURNBOOLNAME, Global.RETURNINTNAME]
                        }
                listjson = {"type": "object",
                    "title": "empty object",
                    "properties":
                        {Global.RETURNBOOLNAME:
                            {"type": "boolean",
                            "description": "成功状态",
                            "mock": {"mock": "true"}
                            },
                        Global.RETURNINTNAME:
                            {"type": "integer",
                                "description": "错误码",
                                "mock": {"mock": 0}
                                },
                        Global.RETURNSTRNAME:
                            {"type": "string",
                                "description": "错误信息",
                                },
                        Global.RETURNLISTPERNAME:
                            {"type": "integer",
                                "description": "分页条数",
                                "mock": {"mock": 20}
                                },
                        Global.RETURNLISTCURRENTNAME:
                            {"type": "integer",
                                "description": "当前页数",
                                "mock": {"mock": 1}
                                },
                        Global.RETURNLISTSIZENAME:
                            {"type": "integer",
                                "description": "当页数据条数",
                                "mock": {"mock": 5}
                                },
                        Global.RETURNLISTTOTALNAME:
                            {"type": "integer",
                                "description": "数据总条数",
                                },
                        "data":
                            {"type": "array",
                            "items":
                                {"type": "object",
                                    "properties": {
                                        "id": {"type": "integer", "description": "id"},
                                    },
                                    "required": ["id"]},
                            "description": "数据列表"}
                        },
                    "required":[Global.RETURNBOOLNAME, Global.RETURNINTNAME, "data"]
                    }
                if typezh == "创建":
                    for column in self.columns:
                        if column.post:
                            pjson["properties"][column.name] = {
                                "type":column.yapi_format,
                                "description":f"{self.zh_name}{column.mean}{column.map_mean}",
                                "mock":{"mock":str(column.random_arg())}}
                            if column.post == 2:
                                pjson["required"].append(column.name)
                    return_str = json.dumps(return_json)

                    for parent in self.parents:
                        if parent.post and parent.Name != 'User':
                            pjson["properties"][parent.name+"_id"] = {"type":"integer","description":parent.mean,
                                "mock":{"mock":str(random.randint(0, 9))}}
                elif typezh == "单个获取":
                    pjson["properties"]['current'] = {"type":"integer","description":"访问页"}
                    pjson["properties"]['pageSize'] = {"type":"integer","description":"单页条数"}
                    for column in self.columns:
                        if column.post:
                            getjson["properties"]['record']["properties"][column.name]= {"type": column.yapi_format, "description": self.zh_name+column.mean + column.map_mean}
                            getjson["properties"]['record']["required"].append(column.name)
                    # getjson["properties"]['record']["required"].append("token")
                    return_str = json.dumps(getjson)
                elif typezh == "列表":
                    sorter = {}
                    pjson["properties"]['current'] = {"type": "integer", "description": "访问页"}
                    pjson["properties"]['pageSize'] = {"type": "integer", "description": "单页条数"}
                    req_query_list.append({"required":"0","name":"per_page","desc":"分页条数"})
                    req_query_list.append({"required":"0","name":"current","desc":"当前页数"})
                    # pjson["properties"]['token'] = {"type":"string","description":"token"}
                    for column in self.columns:
                        if column.post:
                            listjson["properties"]['data']['items']["properties"][column.name] = {"type": column.yapi_format,"description": self.zh_name + column.mean + column.map_mean}
                            listjson["properties"]['data']['items']["required"].append(column.name)
                        if column.list:
                            req_query_list.append({"required":"0","name":column.name,"desc":column.mean + column.map_mean + (column.about or '')})
                    for m in self.many:
                        req_query_list.append({"required":"0","name":f"{m.prefix}{m.name}_id"})
                        
                            
                    return_str = json.dumps(listjson)             
                elif typezh == "修改":
                    return_str = json.dumps(return_json)
                    # for column in self.columns:
                    #     if column.put:
                    #         pjson[column.name] = column.random_arg()
                    for column in self.columns:
                        if column.put:
                            pjson["properties"][column.name] = {
                                "type": column.yapi_format, 
                                "description": column.mean+ column.map_mean,
                                "mock":{"mock":str(column.random_arg())}}
                                
                    for parent in self.parents:
                        if parent.put and parent.Name != 'User':
                            pjson["properties"][parent.name+"_id"] = {
                                "type": "integer", 
                                "description": parent.mean,
                                "mock":{"mock":str(random.randint(0, 9))}}
                    for m in self.many:
                        pjson["properties"][m.name + "_ids"] = {
                            "type": "array", 
                            "description": f"要更新的{m.mean}主键ID数组",
                            "mock":{"mock":str(random.randint(0, 9))}}
                elif typezh == "删除":
                    return_str = json.dumps(return_json)
                    pjson["properties"]["ids"] = {"type": "array", "description": "要删除的id数组","items":{"type":"integer"}}
                pjsonstr = json.dumps(pjson)
                if p == '/<id>':
                    path += '/{id}'
                else:
                    path += p
                single_api = self.single_str(self.zh_name, typezh,  path, method, pjsonstr, return_str,req_query_list)
                gp["list"].append(single_api)
            r.append(gp)
            son_list.append(gp)
            sonjs = json.dumps(son_list)
            return {write_addr:sonjs}
        return {}

    def single_str(self,zh, typezh,  path, method, pjson, rstr,req_query_list):
        item = {
            "query_path": {
                "path": path,
                "params": []
            },
            "edit_uid": 0,
            "status": "undone",
            "type": "static",
            "req_body_is_json_schema": True,
            "res_body_is_json_schema": True,
            "api_opened": False,
            "index": 0,
            "tag": [],
            # "_id": 926,
            "title": zh + typezh,
            "path": path,
            "method": method,
            "desc": "",
            "req_query": req_query_list,
            "req_headers": [
                {
                    "required": "1",
                    "_id": "5fa39b1d6935300090607d7a",
                    "name": "Content-Type",
                    "value": "application/json"
                },
                {
                    "required": "1",
                    "_id": "62187d4fd1fc1e00112c333d",
                    "name": "Authorization",
                    "value": "Bearer {token}",
                    "example": "",
                    "desc": "用户token"
                }
            ],
            "req_body_type": "json",
            "req_body_form": [],
            "req_body_other": pjson,
            "project_id": 26,
            "catid": 86,
            "req_params": [],
            "res_body_type": "json",
            "uid": 11,
            "add_time": 1604218693,
            "up_time": 1604557597,
            "__v": 0,
            "markdown": "",
            "res_body": rstr
        }

        return item

    def write_flask_models(self,project_dir):
        """生成数据库模型文件
        root: string，项目当中src/app的目录位置，绝对地址
        ojson: json,  项目的原始json数据
        """
        tab = "    "
        import_list = []  
        import_list.append('from flask import request, jsonify, current_app, g\n')
        import_list.append('from app import db\n')
        import_list.append('from datetime import datetime,date\n')
        import_list.append('from app.tools import utc_switch\n')
        import_list.append('\n\n')

        target_str_list=[]
        model_dir = os.path.join(project_dir,f'src/models/{self.Name}.py')

        # 加入导入包
        target_str_list += import_list


        # 加入多对多数据库
        target_str_list.append(self.make_many_format("flask_model_map_table",0))
        # 加入数据库class
        class_list = []   
        class_commit_list = []   #注释列表
        class_tojson_commit_list = []   #tojson方法注释列表

        class_commit_list.append(f'{tab}"""{self.zh_name}数据库模型\n\n')
        class_commit_list.append(f'{tab}{self.about}\n\n')
        class_commit_list.append(f'{tab}Attributes:\n')
        class_commit_list.append(f'{tab}"""\n')
        class_list.append(f"class {self.Name}(db.Model):\n")
        class_list.append(f"{tab}__tablename__ = '{self.names}'\n")
        class_commit_list.insert(-1,self.make_column_format("commit_table",2))
        class_commit_list.insert(-1,self.make_parent_format("commit_table",2))
        class_tojson_commit_list.append(f'{tab*2}"""返回请求json数据\n\n')
        class_tojson_commit_list.append(f'{tab*2}Returns:\n')
        # class_list.append(self.make_column_format("commit_to_json",2))
        class_tojson_commit_list.append(f'{tab*2}"""\n')
        
        class_list.append(self.make_column_format("flask_model_detail",0))
        class_list.append(self.make_parent_format("flask_model_detail",0))
        #     for column in self.columns:
        #         tp = column.get('type')
        #         dbtype = Tdb(tp).db
        #         length = column.get('length')
        #         if self.name == "id":
        #             continue
        #         class_commit_list.insert(-1, f"{tab*2}{self.name}: {self.mean}\n")
        #         if column.get('args'):
        #             for arg in column.get('args'):
        #                 self.name = arg.get('self.name')
        #                 value = arg.get('value')
        # for parent in table.get('parents'):
        #     parentname = parent.get('self.name')
        #     parenttablenames = parentname.lower()
        #     class_list.append(
        #         f"{tab}{parenttablenames}_id = db.Column(db.Integer, db.ForeignKey('{parenttablenames}s.id'))\n")
        #     class_list.append(
        #         f"{tab}{parenttablenames} = db.relationship('{parentname}', backref=db.backref('{self.names}', lazy='dynamic'))\n")
        #     class_tojson_commit_list.insert(-1,f'{tab*3}{parenttablenames}_id: 父表{parentname}的ID\n')
        # target_str_list.append(self.make_many_format("flask_model_relation",0))
        # class_list.append(f"\n")

        class_list.append(f"\n{tab}def to_json(self):\n")
        class_list.extend(class_tojson_commit_list)
        # for column in self.columns:
        #     if column.get('file'):
        #         class_list.append(
        #             f"""{tab}{tab}static_host = current_app.config['STATIC_HOST']\n""")
        #         break
        class_list.append(f"{tab}{tab}return{{\n")
        class_list.append(self.make_column_format("flask_model_to_json",3))
        class_list.append(self.make_parent_format("flask_model_to_json",3))
        class_list.append(f"{tab}{tab}}}\n")
        # if table.get('detail_sons') is not None:
        #     class_list.append(f"\n{tab}def to_detail(self):\n")
        #     class_list.append(f"{tab}{tab}return{{\n")
        #     class_list.append(f"{tab}{tab}{tab}'id':self.id,\n")
        #     for column in self.columns:
        #         self.name = column.get('self.name')
        #         if column.get('type') == 'time':
        #             class_list.append(f"{tab}{tab}{tab}'{self.name}':utc_switch(self.{self.name}),\n")
        #         else:
        #             class_list.append(f"{tab}{tab}{tab}'{self.name}':self.{self.name},\n")
        #     for parent in table.get('parents'):  # 显示父表中的值
        #         parentname = parent.get('self.name')
        #         show = parent.get("show")
        #         if show is not None:
        #             for sho in show:
        #                 s_name = sho['name']
        #                 class_list.append(
        #                     f"{tab}{tab}{tab}'{parentname.lower()}_{s_name}' : self.{parentname.lower()}.{s_name},\n")

        #     for son in table.get('detail_sons'):
        #         son = son.lower()
        #         class_list.append(
        #             f"{tab}{tab}{tab}'{son}s':[{son}.to_detail() for {son} in self.{son}s],\n")

        #     class_list.append(f"{tab}{tab}}}\n")

        if self.repr:
            class_list.append(
                f"\n{tab}def __repr__(self):\n{tab}{tab}return '<{self.Name} %r>' % self.{self.repr}\n")

        class_list[1:0] = class_commit_list

        target_str_list += class_list

        # w = open(model_dir, 'w+')
        # for line in target_str_list:
        #     w.write(line)
        # w.close()
        return {model_dir:target_str_list}

# 生成gin文件
    def make_go_gin(self,project_dir):        
        return {
            **self.make_gin_internal_routers(project_dir),
            **self.make_gin_internal_service(project_dir),
            **self.make_gin_internal_dao(project_dir),
            **self.make_gin_internal_model(project_dir),
        }

    def make_gin_internal_routers(self, project_dir):
        t_dir =  os.path.join(project_dir,f"internal/routers/api/v1/{self.name}.go")
        def make_valid_str():
            s = 'response := app.NewResponse(c)\n'
            s += 'valid, errs := app.BindAndValid(c, &param)\n'
            s += 'if !valid {\n'
            s += '    global.Logger.Errorf("app.BindAndValid errs: %v", errs)\n'
            s += '    errRsp := errcode.InvalidParams.WithDetails(errs.Errors()...)\n'
            s += '    response.ToErrorResponse(errRsp)\n'
            s += '    return\n}\n'
            s += '    svc := service.New(c.Request.Context())\n'
            return s
        t_list = []
        t_list.append("package v1\n")
        t_list.append(f"type {self.Name} struct{{}}\n")
        t_list.append(f"func New{self.Name}() {self.Name}{{return {self.Name}{{}}}}\n\n")

        t_list.append(f"func (p {self.Name}) Create(c *gin.Context) {{\n")
        t_list.append(f"param := service.Create{self.Name}Request{{}}\n")
        t_list.append(make_valid_str())
        t_list.append(f"{self.name}_id, err := svc.Create{self.Name}(&param)\n")
        t_list.append(f"if err != nil {{\n")
        t_list.append(f'global.Logger.Errorf("svc.Create{self.Name} err: %v", err)\n')
        t_list.append(f'if {self.name}_id == 0 {{\n')
        t_list.append(f'	response.ToErrorResponse(errcode.ErrorCreate{self.Name}NameExisted)\n')
        t_list.append(f'}} else {{\n')
        t_list.append(f'	response.ToErrorResponse(errcode.ErrorCreate{self.Name}Fail)\n')
        t_list.append(f'}}\n')
        t_list.append(f'return\n')
        t_list.append(f'}}\n')
        t_list.append(f'param.Id = {self.name}_id\n')
        t_list.append(f'response.ToResponse(param)\n')
        t_list.append(f'return\n}}\n')

        t_list.append(f'func (t {self.Name}) Get(c *gin.Context) {{\n')
        if self.index.name != "id":
            t_list.append(f'	param := service.Get{self.Name}Request{{{self.index.Name}: c.Param("{self.index.name}")}}\n')
        else:
            t_list.append(f'	param := service.Get{self.Name}Request{{Id: convert.StrTo(c.Param("id")).MustUInt32()}}\n')
        t_list.append(f'	response := app.NewResponse(c)\n')
        t_list.append(f'	valid, errs := app.BindAndValid(c, &param)\n')
        t_list.append(f'	if !valid {{\n')
        t_list.append(f'		global.Logger.Errorf("app.BindAndValid errs: %v", errs)\n')
        t_list.append(f'		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))\n')
        t_list.append(f'		return\n')
        t_list.append(f'	}}\n')
        t_list.append(f'	svc := service.New(c.Request.Context())\n')
        t_list.append(f'	{self.name}, err := svc.Get{self.Name}(&param)\n')
        t_list.append(f'	if err != nil {{\n')
        t_list.append(f'		global.Logger.Errorf("svc.Get{self.Name} err: %v", err)\n')
        t_list.append(f'		response.ToErrorResponse(errcode.ErrorGet{self.Name}Fail)\n')
        t_list.append(f'		return\n')
        t_list.append(f'	}}\n')
        t_list.append(f'	response.ToResponse({self.name})\n')
        t_list.append(f'	return\n')
        t_list.append(f'}}\n\n')

        t_list.append(f'func (t {self.Name}) List(c *gin.Context) {{\n')
        t_list.append(f'	param := service.{self.Name}ListRequest{{}}\n')
        t_list.append(f'	response := app.NewResponse(c)\n')
        t_list.append(f'	valid, errs := app.BindAndValid(c, &param)\n')
        t_list.append(f'	if !valid {{\n')
        t_list.append(f'		global.Logger.Errorf("app.BindAndValid errs: %v", errs)\n')
        t_list.append(f'		errRsp := errcode.InvalidParams.WithDetails(errs.Errors()...)\n')
        t_list.append(f'		response.ToErrorResponse(errRsp)\n')
        t_list.append(f'		return\n')
        t_list.append(f'	}}\n')
        t_list.append(f'\n')
        t_list.append(f'	svc := service.New(c)\n')
        t_list.append(f'	pager := app.Pager{{\n')
        t_list.append(f'		Page:     app.GetPage(c),\n')
        t_list.append(f'		PageSize: app.GetPageSize(c),\n')
        t_list.append(f'	}}\n')
        t_list.append(f'	totalRows, err := svc.Count{self.Name}(&service.Count{self.Name}Request{{\n')
        t_list.append(self.make_column_format("gin_api_router_count",2))
        t_list.append(f'	}})\n')
        t_list.append(f'	if err != nil {{\n')
        t_list.append(f'		global.Logger.Errorf("svc.Count{self.Name} err: %v", err)\n')
        t_list.append(f'		response.ToErrorResponse(errcode.ErrorCount{self.Name}Fail)\n')
        t_list.append(f'	}}\n')
        t_list.append(f'	{self.names}, err := svc.Get{self.Name}List(&param, &pager)\n')
        t_list.append(f'	if err != nil {{\n')
        t_list.append(f'		global.Logger.Errorf("svc.Get{self.Name}List err: %v", err)\n')
        t_list.append(f'		response.ToErrorResponse(errcode.ErrorGet{self.Name}ListFail)\n')
        t_list.append(f'		return\n')
        t_list.append(f'	}}\n')
        t_list.append(f'	response.ToResponseList({self.names}, totalRows)\n')
        t_list.append(f'	return\n')
        t_list.append(f'}}\n\n')

        t_list.append(f'func (t {self.Name}) Update(c *gin.Context) {{\n')
        if self.index.name != "id":
            t_list.append(f'	param := service.Update{self.Name}Request{{{self.index.Name}: c.Param("{self.index.name}")}}\n')
        else:
            t_list.append(f'	param := service.Update{self.Name}Request{{Id: convert.StrTo(c.Param("id")).MustUInt32()}}\n')
        t_list.append(f'	response := app.NewResponse(c)\n')
        t_list.append(f'	valid, errs := app.BindAndValid(c, &param)\n')
        t_list.append(f'	if !valid {{\n')
        t_list.append(f'		global.Logger.Errorf("app.BindAndValid errs: %v", errs)\n')
        t_list.append(f'		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))\n')
        t_list.append(f'		return\n')
        t_list.append(f'	}}\n')
        t_list.append(f'\n')
        t_list.append(f'	svc := service.New(c.Request.Context())\n')
        t_list.append(f'	n, err := svc.Update{self.Name}(&param)\n')
        t_list.append(f'	if err != nil || n < 1 {{\n')
        t_list.append(f'		global.Logger.Errorf("svc.Update{self.Name} err: %v", err)\n')
        t_list.append(f'		response.ToErrorResponse(errcode.ErrorUpdate{self.Name}Fail)\n')
        t_list.append(f'		return\n')
        t_list.append(f'	}}\n')
        t_list.append(f'\n')
        t_list.append(f'	response.ToResponse(gin.H{{}})\n')
        t_list.append(f'	return\n')
        t_list.append(f'}}\n\n')
        t_list.append(f'func (t {self.Name}) Delete(c *gin.Context) {{\n')
        if self.index.name != "id":
            t_list.append(f'	param := service.Delete{self.Name}Request{{{self.index.Name}: c.Param("{self.index.name}")}}\n')
        else:
            t_list.append(f'	param := service.Delete{self.Name}Request{{Id: convert.StrTo(c.Param("id")).MustUInt32()}}\n')
        # t_list.append(f'	param := service.Delete{self.Name}Request{{}}\n')
        t_list.append(f'	response := app.NewResponse(c)\n')
        t_list.append(f'	valid, errs := app.BindAndValid(c, &param)\n')
        t_list.append(f'	if !valid {{\n')
        t_list.append(f'		global.Logger.Errorf("app.BindAndValid errs: %v", errs)\n')
        t_list.append(f'		response.ToErrorResponse(errcode.InvalidParams.WithDetails(errs.Errors()...))\n')
        t_list.append(f'		return\n')
        t_list.append(f'	}}\n')
        t_list.append(f'\n')
        t_list.append(f'	svc := service.New(c.Request.Context())\n')
        t_list.append(f'	n, err := svc.Delete{self.Name}(&param)\n')
        t_list.append(f'	if err != nil || n < 1{{\n')
        t_list.append(f'		global.Logger.Errorf("svc.Delete{self.Name} err: %v", err)\n')
        t_list.append(f'		response.ToErrorResponse(errcode.ErrorDelete{self.Name}Fail)\n')
        t_list.append(f'		return\n')
        t_list.append(f'	}}\n')
        t_list.append(f'\n')
        t_list.append(f'	response.ToResponse(gin.H{{}})\n')
        t_list.append(f'	return\n')
        t_list.append(f'}}\n')

        return {t_dir:t_list}
    
    def make_gin_internal_service(self, project_dir):
        t_dir =  os.path.join(project_dir,f"internal/service/{self.name}.go")
        t_list = []
        t_list.append("package service\n\n")
        t_list.append(f'type Count{self.Name}Request struct {{\n')
        t_list.append(self.make_column_format("gin_api_service_count_valid",1))
        t_list.append(f'}}\n\n')
        t_list.append(f'type {self.Name}ListRequest struct {{\n')
        t_list.append(self.make_column_format("gin_api_service_count_valid",1))
        t_list.append(f'}}\n\n')
        t_list.append(f'type Create{self.Name}Request struct {{\n')
        t_list.append(f'	Id       int64  `json:"id"`\n')
        t_list.append(self.make_column_format("gin_api_create_valid",1))
        t_list.append(f'}}\n\n')
        t_list.append(f'type Update{self.Name}Request struct {{\n')
        t_list.append(f'	 {self.index.Name} {self.index.go_type} `form:"{self.index.name} binding:"required"`\n')
        t_list.append(self.make_column_format("gin_api_update_valid",1))
        t_list.append(f'}}\n\n')
        t_list.append(f'type Get{self.Name}Request struct {{\n')        
        t_list.append(f'	 {self.index.Name} {self.index.go_type} `form:"{self.index.name} binding:"required"`\n}}\n\n')
        t_list.append(f'type Delete{self.Name}Request struct {{\n')
        t_list.append(f'	 {self.index.Name} {self.index.go_type} `form:"{self.index.name} binding:"required"`\n}}\n\n')
        t_list.append(f'func (svc *Service) Count{self.Name}(param *Count{self.Name}Request) (int, error) {{\n')
        t_list.append(f'	return svc.dao.Count{self.Name}({self.make_column_format("gin_api_service_list_param")})\n}}\n\n')
        t_list.append(f'func (svc *Service) Get{self.Name}List(param *{self.Name}ListRequest, pager *app.Pager) ([]*model.{self.Name}, error) {{\n')
        t_list.append(f'	return svc.dao.Get{self.Name}List({self.make_column_format("gin_api_service_list_param")} pager.Page, pager.PageSize)\n}}\n\n')
        t_list.append(f'func (svc *Service) Create{self.Name}(param *Create{self.Name}Request) (int64, error) {{\n')
        t_list.append(f'	return svc.dao.Create{self.Name}({self.make_column_format("gin_api_service_create_param")})\n}}\n\n')
        t_list.append(f'func (svc *Service) Update{self.Name}(param *Update{self.Name}Request) (int64, error) {{\n')
        t_list.append(f'	return svc.dao.Update{self.Name}({self.make_column_format("gin_api_service_update_param")} param.{self.index.Name})\n}}\n\n')
        t_list.append(f'func (svc *Service) Delete{self.Name}(param *Delete{self.Name}Request) (int64, error) {{\n')
        t_list.append(f'	return svc.dao.Delete{self.Name}(param.{self.index.Name})\n}}\n\n')
        t_list.append(f'func (svc *Service) Get{self.Name}(param *Get{self.Name}Request) (*model.{self.Name}, error) {{\n')
        t_list.append(f'	return svc.dao.Get{self.Name}(param.{self.index.Name})\n}}\n\n')
        return {t_dir:t_list}

    def make_gin_internal_dao(self, project_dir):
        t_dir =  os.path.join(project_dir,f"internal/dao/{self.name}.go")
        t_list = []
        t_list.append("package dao\n\n")
        t_list.append(f'func (d *Dao) Count{self.Name}({self.make_column_format("gin_api_dao_list_args")}) (int, error) {{\n')
        t_list.append(f'	{self.name} := model.{self.Name}{{{self.make_column_format("gin_api_dao_list_model",2)}}}\n')
        t_list.append(f'	return {self.name}.Count(d.engine)\n}}\n\n')
        t_list.append(f'func (d *Dao) Get{self.Name}({self.index.name} {self.index.go_type}) (*model.{self.Name}, error) {{\n')
        t_list.append(f'	{self.name} := model.{self.Name}{{{self.index.Name}: {self.index.name}}}\n')
        t_list.append(f'	return {self.name}.Get(d.engine)\n}}\n\n')
        t_list.append(f'func (d *Dao) Get{self.Name}List({self.make_column_format("gin_api_dao_list_args")} page, pageSize int) ([]*model.{self.Name}, error) {{\n')
        t_list.append(f'	{self.name} := model.{self.Name}{{{self.make_column_format("gin_api_dao_list_model",2)}}}\n')
        t_list.append(f'	pageOffset := app.GetPageOffset(page, pageSize)\n')
        t_list.append(f'	return {self.name}.List(d.engine, pageOffset, pageSize)\n}}\n\n')
        t_list.append(f'func (d *Dao) Create{self.Name}({self.make_column_format("gin_api_dao_create_args")}) (int64, error) {{\n')
        t_list.append(f'	{self.name} := model.{self.Name}{{\n')
        t_list.append(self.make_column_format("gin_api_dao_create_model",2))
        t_list.append(f'	}}\n')
        t_list.append(f'	return {self.name}.Create(d.engine)\n}}\n\n')
        t_list.append(f'func (d *Dao) Update{self.Name}({self.make_column_format("gin_api_dao_update_args")} {self.index.name} {self.index.go_type}) (int64, error) {{\n')
        t_list.append(f'	{self.name} := model.{self.Name}{{\n')
        t_list.append(f'	{self.index.Name}: {self.index.name},\n')
        t_list.append(self.make_column_format("gin_api_dao_update_model",2))
        t_list.append(f'	}}\n')
        t_list.append(f'	return {self.name}.Update(d.engine)\n}}\n\n')
        if self.index:
            t_list.append(f'func (d *Dao) Delete{self.Name}({self.index.name} {self.index.go_type}) (int64, error) {{\n')        
            t_list.append(f'	{self.name} := model.{self.Name}{{{self.index.Name}: {self.index.name}}}\n')
            t_list.append(f'	return {self.name}.Delete(d.engine)\n}}\n\n')
        else:
            t_list.append(f'func (d *Dao) Delete{self.Name}(ids []uint) (int64, error) {{\n')        
            t_list.append(f'	sqlStr := "delete from {self.name}s where id in (%s)"\n')
            t_list.append(f'	idStr := strings.Replace(strings.Trim(fmt.Sprint(ids), "[]"), " ", ", ", -1)\n')
            t_list.append(f'	sqlStr = fmt.Sprintf(sqlStr, idStr)\n')
            t_list.append(f'	ret, err := d.engine.Exec(sqlStr)\n')
            t_list.append(f'	if err != nil {{\n')
            t_list.append(f'		return -1, err\n')
            t_list.append(f'	}}\n')
            t_list.append(f'	n, err := ret.RowsAffected()\n')
            t_list.append(f'	if err != nil {{\n')
            t_list.append(f'		return -1, err\n')
            t_list.append(f'	}}\n')
            t_list.append(f'	return n, err\n}}\n\n')
        return {t_dir:t_list}

    def make_gin_internal_model(self, project_dir):
        t_dir =  os.path.join(project_dir,f"internal/model/{self.name}.go")
        t_list = []
        t_list.append("package model\n\n")
        t_list.append('import (\n  "database/sql"\n"fmt"\n"strings"\n)\n')

        t_list.append(f'type {self.Name} struct {{\n')
        t_list.append(self.make_column_format("gin_api_model_struct_arg",1))
        t_list.append(f'}}\n')
        t_list.append(f' \n')
        t_list.append(f'func (o {self.Name}) TableName() string {{\n')
        t_list.append(f'	return "{self.name}s"\n')
        t_list.append(f'}}\n')
        t_list.append(f' \n')
        t_list.append(f'func (o {self.Name}) Count(db *sql.DB) (int, error) {{\n')
        t_list.append(f'	var count int\n')
        t_list.append(f'	sqlStr := "select count(id) from {self.name}s "\n')
        t_list.append(f'	var where bool\n')
        t_list.append(self.make_column_format("gin_api_model_count_sql_str",1))
        t_list.append(f'	err := db.QueryRow(sqlStr).Scan(&count)\n')
        t_list.append(f'	if err != nil {{\n')
        t_list.append(f'		return 0, err\n')
        t_list.append(f'	}}\n')
        t_list.append(f'	return count, nil\n')
        t_list.append(f'}}\n\n')
        t_list.append(f'func (o {self.Name}) List(db *sql.DB, pageOffset, pageSize int) ([]*{self.Name}, error) {{\n')
        t_list.append(f'	var {self.name}s []*{self.Name}\n')
        t_list.append(f'	sqlStr := "select {self.make_column_format("gin_api_model_select_arg")[:-1]} from {self.name}s"\n')
        t_list.append(f'	var where bool\n')
        t_list.append(self.make_column_format("gin_api_model_count_sql_str",1))
        t_list.append(f'	if pageOffset >= 0 && pageSize > 0 {{\n')
        t_list.append(f'		sqlStr += fmt.Sprintf(" limit %d offset %d", pageSize, pageOffset)\n')
        t_list.append(f'	}}\n')
        t_list.append(f'	rows, err := db.Query(sqlStr)\n')
        t_list.append(f'	if err != nil {{\n')
        t_list.append(f'		return nil, err\n')
        t_list.append(f'	}}\n')
        t_list.append(f'	defer rows.Close()\n')
        t_list.append(f'	for rows.Next() {{\n')
        t_list.append(f'		var {self.name} {self.Name}\n')
        t_list.append(f'		err := rows.Scan({self.make_column_format("gin_api_model_list_scan")})\n')
        t_list.append(f'		if err != nil {{\n')
        t_list.append(f'			return nil, err\n')
        t_list.append(f'		}}\n')
        t_list.append(f'		{self.name}s = append({self.name}s, &{self.name})\n')
        t_list.append(f'	}}\n')
        t_list.append(f'	return {self.name}s, nil\n}}\n\n')
        t_list.append(f'func (o *{self.Name}) Get(db *sql.DB) (*{self.Name}, error) {{\n')
        t_list.append(f'	sqlStr := "select {self.make_column_format("gin_api_model_select_arg")[:-1]} from {self.name}s where {self.index.name} = ?"\n')
        t_list.append(f'	err := db.QueryRow(sqlStr, o.{self.index.Name}).Scan({self.make_column_format("gin_api_model_get_scan")})\n')
        t_list.append(f'	if err != nil {{\n')
        t_list.append(f'		return nil, err\n')
        t_list.append(f'	}}\n')
        t_list.append(f'	return o, nil\n}}\n\n')
        t_list.append(f'func (o {self.Name}) Create(db *sql.DB) (int64, error) {{\n')
        t_list.append(self.make_column_format("gin_api_model_create_unique"))
        if self.index.name == "id":
            t_list.append(f'	sqlStr := "insert into {self.name}s ({self.make_column_format("sql_create_col_name")[:-1]}) values ({self.make_column_format("gin_api_model_create_sql_?")[:-1]})"\n')
            t_list.append(f'	ret, err := db.Exec(sqlStr,{self.make_column_format("gin_api_model_create_exec_arg")[:-1]})\n')
        else:
            t_list.append(f'	{self.index.name} := uuid.NewV4().String()\n')
            t_list.append(f'	sqlStr := "insert into {self.name}s ({self.make_column_format("sql_create_col_name")}`{self.index.name}`) values ({self.make_column_format("gin_api_model_create_sql_?")} ?)"\n')
            t_list.append(f'	ret, err := db.Exec(sqlStr,{self.make_column_format("gin_api_model_create_exec_arg")} {self.index.name})\n')
        t_list.append(f'	if err != nil {{\n')
        t_list.append(f'		return -1, err\n')
        t_list.append(f'	}}\n')
        t_list.append(f'	{self.name}_id, err := ret.LastInsertId()\n')
        t_list.append(f'	return {self.name}_id, err\n')
        t_list.append(f'}}\n\n')
        t_list.append(f'func (o {self.Name}) Update(db *sql.DB) (int64, error) {{\n')
        t_list.append(self.make_column_format("gin_api_model_create_unique"))
        t_list.append(f'	sqlStr := "UPDATE {self.names} SET {self.make_column_format("gin_api_model_update_sql")[:-1]} where {self.index.name} = ?"\n')
        t_list.append(f'	ret, err := db.Exec(sqlStr,{self.make_column_format("gin_api_model_update_exec_arg")} o.{self.index.Name})\n')
        t_list.append(f'	if err != nil {{\n		return -1, err\n	}}\n')
        t_list.append(f'	n, err := ret.RowsAffected()\n')
        t_list.append(f'	if err != nil {{\n		return -1, err\n	}}\n')
        t_list.append(f'	return n, err\n')
        t_list.append(f'}}\n\n')
        t_list.append(f'func (o {self.Name}) Delete(db *sql.DB) (int64, error) {{\n')
        t_list.append(f'	sqlStr := "delete from {self.name}s where {self.index.name} = ?"\n')
        t_list.append(f'	ret, err := db.Exec(sqlStr, o.{self.index.Name})\n')
        t_list.append(f'	if err != nil {{\n')
        t_list.append(f'		return -1, err\n')
        t_list.append(f'	}}\n')
        t_list.append(f'	n, err := ret.RowsAffected()\n')
        t_list.append(f'	if err != nil {{\n')
        t_list.append(f'		return -1, err\n')
        t_list.append(f'	}}\n')
        t_list.append(f'	return n, err\n')
        t_list.append(f'}}\n')
        return {t_dir:t_list}



# 生成go_dapr的后端文件
    def make_go_gin_dapr(self,project_dir):        
        return {
            **self.make_gin_dapr_internal_database_migrations_up(project_dir),
            **self.make_gin_dapr_internal_database_migrations_down(project_dir),
            **self.make_gin_dapr_internal_http_controllers(project_dir),
            **self.make_gin_dapr_internal_repo(project_dir),
            **self.make_gin_dapr_internal_forms(project_dir),
        }

    def make_gin_dapr_internal_database_migrations_up(self, project_dir):
        file_path =  os.path.join(project_dir,f"internal/database/migrations/00000_{self.names}.up.sql")
        f_list = []
        f_list.append(f"/* {self.zh_name} */\n")
        f_list.append(f"CREATE TABLE IF NOT EXISTS `{self.names}`  (\n")
        f_list.append(self.make_column_format("go_gin_dapr_mysql_sql_create_args", 1))
        f_list.append(self.make_column_format("go_gin_dapr_mysql_sql_create_bind", 1))
        f_list[-1] =re.sub(",\n$","\n",f_list[-1])
        f_list.append(f") CHARACTER SET = utf8mb4;\n")
        return {file_path:f_list}
 
    def make_gin_dapr_internal_database_migrations_down(self, project_dir):
        file_path =  os.path.join(project_dir,f"internal/database/migrations/00000_{self.names}.down.sql")
        f_list = []
        f_list.append(f"DROP TABLE IF EXISTS `{self.names}`;")
        return {file_path:f_list}

    def make_gin_dapr_internal_http_wire(self):
        f_list = []
        f_list.append(f"// @title		init{self.Name}Controller\n")
        f_list.append(f"// @description	初始化{self.zh_name}控制器\n")
        f_list.append(f"// @author		rong	{self.now_date}\n")
        f_list.append(f"// @return 	    {self.Name}Controller {self.zh_name}控制器\n")
        f_list.append(f"//         	    error 错误，无错误为成功\n")
        f_list.append(f"func init{self.Name}Controller(mysqlcfg *database.DaprMysqlConfig) (*controllers.{self.Name}Controller, error) {{\n")
        f_list.append(f"	wire.Build(controllers.{self.Name}ControllerProviderSet, repo.{self.Name}RepoProviderSet, database.DaprMysqlProviderSet)\n")
        f_list.append(f"	return nil, nil\n")
        f_list.append(f"}}\n\n")
        return f_list
  
    def make_gin_dapr_internal_http_server(self):
        f_list = []
        f_list.append(f"    // {self.name} {self.zh_name}router\n")
        f_list.append(f"    {self.name}, err := init{self.Name}Controller(global.DaprConfig.Mysql)\n")
        f_list.append(f"    if err != nil {{\n        return err\n    }}\n")
        f_list.append(f'    {self.name}Router := r.Group("/{self.names}")\n')
        f_list.append(f'    {self.name}Router.POST("", {self.name}.Create)\n')
        f_list.append(f'    {self.name}Router.PUT("/:{self.index.name}", {self.name}.Update)\n')
        f_list.append(f'    {self.name}Router.GET("/:{self.index.name}", {self.name}.Get)\n')
        f_list.append(f'    {self.name}Router.GET("", {self.name}.List)\n')
        f_list.append(f'    {self.name}Router.DELETE("", {self.name}.Delete)\n\n')

        return f_list

    def make_gin_dapr_internal_http_controllers(self, project_dir):
        file_path =  os.path.join(project_dir,f"internal/http/controllers/{self.name}.go")
        f_list = []
        f_list.append(f'// @Title  {self.name}.go\n')
        f_list.append(f'// @Description  {self.zh_name}控制器定义以及初始化\n')
        f_list.append(f'// @Author	rong	{self.now_date}\n')
        f_list.append(f'// @Update\n')
        f_list.append(f'package controllers\n\n')
        f_list.append(f'import (\n')
        f_list.append(f'	"net/http"\n')
        f_list.append(f'	"strconv"\n\n')
        f_list.append(f'	"{self.app_name}/internal/forms"\n')
        f_list.append(f'	"{self.app_name}/internal/repo"\n')
        f_list.append(f'	"{self.app_name}/internal/response"\n')
        f_list.append(f'	\n')
        f_list.append(f'	"github.com/gin-gonic/gin"\n')
        f_list.append(f'	"github.com/google/wire"\n')
        f_list.append(f')\n\n')
        f_list.append(f'// {self.Name}Controller {self.zh_name}控制器\n')
        f_list.append(f'type {self.Name}Controller struct {{\n')
        f_list.append(f'	repo repo.I{self.Name}Repo\n')
        f_list.append(f'}}\n\n')
        f_list.append(f'// I{self.Name}Controller {self.zh_name}控制器接口\n')
        f_list.append(f'type I{self.Name}Controller interface{{}}\n')
        f_list.append(f'\n')
        f_list.append(f'var {self.Name}ControllerProviderSet = wire.NewSet(New{self.Name}Controller, wire.Bind(new(I{self.Name}Controller), new(*{self.Name}Controller)))\n\n')
        f_list.append(f'// @title	New{self.Name}Controller\n')
        f_list.append(f'// @description	初始化{self.zh_name}控制器\n')
        f_list.append(f'// @author	rong	{self.now_date}\n')
        f_list.append(f'// @param	repo interface {self.zh_name}接口类\n')
        f_list.append(f'// @return  *{self.Name}Controller interface {self.zh_name}类\n')
        f_list.append(f'func New{self.Name}Controller(repo repo.I{self.Name}Repo) *{self.Name}Controller {{\n')
        f_list.append(f'	return &{self.Name}Controller{{\n')
        f_list.append(f'		repo: repo,\n')
        f_list.append(f'	}}\n')
        f_list.append(f'}}\n\n')

        f_list.append(f'// @title	Create\n')
        f_list.append(f'// @description	创建{self.zh_name}\n')
        f_list.append(f'// @author	rong	{self.now_date}\n')
        f_list.append(f'// @param	form forms.{self.Name}CreateForm 创建{self.zh_name}表单参数\n')
        f_list.append(f'// @return  无\n')
        f_list.append(f'func (ctl *{self.Name}Controller) Create(c *gin.Context) {{\n')
        f_list.append(f'	// 验证并绑定post提交的json数据到forms.{self.Name}CreateForm结构体实例form当中，验证错误则返回参数信息错误\n')
        f_list.append(f'	var form forms.{self.Name}CreateForm\n')
        f_list.append(f'	err := c.ShouldBindJSON(&form)\n')
        f_list.append(f'	if err != nil {{\n')
        f_list.append(f'		c.JSON(http.StatusOK, response.NewResponseMessage(response.ParamBindError, err.Error()))\n')
        f_list.append(f'		return\n')
        f_list.append(f'	}}\n')
        f_list.append(f'\n    //将post提交的数据绑定的结构体传递到repo当中，对数据库进行新增操作\n')
        f_list.append(f'	err = ctl.repo.Create(form)\n')
        f_list.append(f'	if err != nil {{\n')
        f_list.append(f'		c.JSON(http.StatusOK, response.NewResponseMessage(response.CreateError, err.Error()))\n')
        f_list.append(f'		return\n	}}\n\n')
        f_list.append(f'    //接口返回创建成功json信息\n')
        f_list.append(f'	c.JSON(http.StatusOK, response.ResponseSuccess())\n}}\n\n')

        f_list.append(f'// @title	Update\n')
        f_list.append(f'// @description	修改{self.zh_name}\n')
        f_list.append(f'// @author	rong	{self.now_date}\n')
        f_list.append(f'// @param	form forms.{self.Name}UpdateForm 修改{self.zh_name}表单参数\n')
        f_list.append(f'//          id int 要修改的{self.zh_name}ID\n')
        f_list.append(f'// @return  无\n')
        f_list.append(f'func (ctl *{self.Name}Controller) Update(c *gin.Context) {{\n')
        f_list.append(f'	var err error\n')
        f_list.append(f'\n    // 获取url当中的参数，参数为空或类型不对返回非法请求错误\n')
        if self.index.db == "Integer":
            f_list.append(f'	idStr := c.Param("{self.index.name}")\n')
            f_list.append(f'	id, err := strconv.Atoi(idStr)\n')
            f_list.append(f'	if err != nil {{\n')
        elif self.index.type == "string":
            f_list.append(f'	id := c.Param("{self.index.name}")\n')
            f_list.append(f'	if len(id) <= 0 {{\n')
        f_list.append(f'		c.JSON(http.StatusOK, response.NewResponse(response.InvalidRequest))\n')
        f_list.append(f'		return\n')
        f_list.append(f'	}}\n')
        f_list.append(f'\n    // 验证并绑定put提交的json数据到forms.{self.Name}UpdateForm结构体实例form当中，验证错误则返回参数信息错误\n')
        f_list.append(f'	var form forms.{self.Name}UpdateForm\n')
        f_list.append(f'	err = c.ShouldBindJSON(&form)\n')
        f_list.append(f'	if err != nil {{\n')
        f_list.append(f'		c.JSON(http.StatusOK, response.NewResponseMessage(response.ParamBindError, err.Error()))\n')
        f_list.append(f'		return\n')
        f_list.append(f'	}}\n')
        f_list.append(f'\n    // 将put提交的数据绑定的结构体传递到repo当中，对数据库进行修改操作\n')
        f_list.append(f'	err = ctl.repo.Update(id, form)\n')
        f_list.append(f'	if err != nil {{\n')
        f_list.append(f'		c.JSON(http.StatusOK, response.NewResponseMessage(response.UpdateError, err.Error()))\n')
        f_list.append(f'		return\n	}}\n\n')
        f_list.append(f'    // 接口返回修改成功json信息\n')
        f_list.append(f'	c.JSON(http.StatusOK, response.ResponseSuccess())\n}}\n\n')

        f_list.append(f'// @title	Get\n')
        f_list.append(f'// @description	获取某个{self.zh_name}\n')
        f_list.append(f'// @author	rong	{self.now_date}\n')
        f_list.append(f'// @param	id int 要修改的{self.zh_name}ID\n')
        f_list.append(f'// @return  无\n')
        f_list.append(f'func (ctl *{self.Name}Controller) Get(c *gin.Context) {{\n')
        f_list.append(f'	var err error\n')
        f_list.append(f'\n    // 获取url当中的参数，参数为空或类型不对返回非法请求错误\n')
        if self.index.db == "Integer":
            f_list.append(f'	idStr := c.Param("{self.index.name}")\n')
            f_list.append(f'	id, err := strconv.Atoi(idStr)\n')
            f_list.append(f'	if err != nil {{\n')
        elif self.index.type == "string":
            f_list.append(f'	id := c.Param("{self.index.name}")\n')
            f_list.append(f'	if len(id) <= 0 {{\n')
        f_list.append(f'		c.JSON(http.StatusOK, response.NewResponse(response.InvalidRequest))\n')
        f_list.append(f'		return\n    }}\n\n')
        f_list.append(f'\n    // 将url当中获取的{self.index.name}传给repo，作为唯一标识去数据库查找一条数据，并返回{self.zh_name}的详情结构体\n')
        f_list.append(f'	{self.name}, err := ctl.repo.Get(id)\n')
        f_list.append(f'	if err != nil {{\n')
        f_list.append(f'		c.JSON(http.StatusOK, response.NewResponseMessage(response.GetError, err.Error()))\n')
        f_list.append(f'		return\n	}}\n')
        f_list.append(f'\n    // 接口返回成功json信息和{self.zh_name}详情\n')
        f_list.append(f'	c.JSON(http.StatusOK, response.NewResponseData(response.Success, {self.name}))\n}}\n\n')

        f_list.append(f'// @title	List\n')
        f_list.append(f'// @description	获取{self.zh_name}列表\n')
        f_list.append(f'// @author	rong	{self.now_date}\n')
        f_list.append(f'// @param	query forms.{self.Name} 分页请求参数表单\n')
        f_list.append(f'// @return  无\n')
        f_list.append(f'func (ctl *{self.Name}Controller) List(c *gin.Context) {{\n')
        f_list.append(f'	// 验证并绑定url当中的查询参数到forms.{self.Name}Query结构体实例query当中，验证错误则返回参数信息错误\n')
        f_list.append(f'	var query forms.{self.Name}Query\n')
        f_list.append(f'	err := c.ShouldBindQuery(&query)\n')
        f_list.append(f'	if err != nil {{\n')
        f_list.append(f'		c.JSON(http.StatusOK, response.NewResponseMessage(response.ParamBindError, err.Error()))\n')
        f_list.append(f'		return\n')
        f_list.append(f'	}}\n')
        f_list.append(f'\n    // 每页数据条数未提交默认为20条\n')
        f_list.append(f'	if query.PerPage < 1 {{\n')
        f_list.append(f'		query.PerPage = 20\n')
        f_list.append(f'	}}\n')
        f_list.append(f'\n    // 当前页未提交默认为第一页\n')
        f_list.append(f'	if query.Current < 1 {{\n')   
        f_list.append(f'		query.Current = 1\n')
        f_list.append(f'	}}\n')
        f_list.append(f'\n    // 将分页查询数据提交到repo中到数据库找到对应的数据列表和总数据条数\n')
        f_list.append(f'	total, {self.names}, err := ctl.repo.List(query)\n')
        f_list.append(f'	if err != nil {{\n')
        f_list.append(f'		c.JSON(http.StatusOK, response.NewResponseMessage(response.GetError, err.Error()))\n')
        f_list.append(f'		return\n')
        f_list.append(f'	}}\n')
        f_list.append(f'\n    // 将取得的分页数据数组，数据总条数，当页数据条数，请求分页数据插入到标准json输出结构体中\n')
        f_list.append(f'	size := len({self.names})\n')
        f_list.append(f'	res := response.NewResponseData(response.Success, {self.names})\n')
        f_list.append(f'	res.Total = &total\n')
        f_list.append(f'	res.Current = query.Current\n')
        f_list.append(f'	res.PerPage = query.PerPage\n')
        f_list.append(f'	res.Size = &size\n\n')
        f_list.append(f'    //接口返回成功信息和{self.zh_name}分页列表\n')
        f_list.append(f'	c.JSON(http.StatusOK, res)\n}}\n')

        f_list.append(f'// @title	Delete\n')
        f_list.append(f'// @description	批量删除{self.zh_name}\n')
        f_list.append(f'// @author	rong	{self.now_date}\n')
        f_list.append(f'// @param	form forms.DeleteIds 要删除的{self.zh_name}ID列表表单\n')
        f_list.append(f'// @return  无\n')
        f_list.append(f'func (ctl *{self.Name}Controller) Delete(c *gin.Context) {{\n')
        f_list.append(f'	// 验证并绑定提交的json数据到DeleteIds结构体实例当中，为一个名为ids的需要删除的Id列表，验证错误则返回参数信息错误\n')
        f_list.append(f'	var form forms.DeleteIds\n')
        f_list.append(f'	err := c.ShouldBindJSON(&form)\n')
        f_list.append(f'	if err != nil {{\n')
        f_list.append(f'		c.JSON(http.StatusOK, response.NewResponseMessage(response.ParamBindError, err.Error()))\n')
        f_list.append(f'		return\n')
        f_list.append(f'	}}\n')
        f_list.append(f'\n    //将要删除的id切片传给repo去进行批量删除\n')
        f_list.append(f'	err = ctl.repo.Delete(form.Ids)\n')
        f_list.append(f'	if err != nil {{\n')
        f_list.append(f'		c.JSON(http.StatusOK, response.NewResponseMessage(response.DeleteError, err.Error()))\n')
        f_list.append(f'		return\n')
        f_list.append(f'	}}\n\n')
        f_list.append(f'    //接口返回删除成功信息\n')
        f_list.append(f'	c.JSON(http.StatusOK, response.ResponseSuccess())\n')
        f_list.append(f'}}\n')

        return {file_path:f_list}

    def make_gin_dapr_internal_repo(self, project_dir):
        file_path =  os.path.join(project_dir,f"internal/repo/{self.name}.go")
        f_list = []
        
        f_list.append(f'// @Title  {self.name}.go\n')
        f_list.append(f'// @Description  {self.zh_name}初始化\n')
        f_list.append(f'// @Autor: rong	{self.now_date}\n')
        f_list.append(f'// @Update:\n')
        f_list.append(f'package repo\n\n')
        f_list.append(f'import (\n')
        f_list.append(f'	"encoding/json"\n')
        f_list.append(f'	"errors"\n')
        f_list.append(f'	"fmt"\n')
        f_list.append(f'	"strings"\n')
        f_list.append(f'	"time"\n\n')
        f_list.append(f'	"{self.app_name}/internal/{Global.GODAPRDBPACKAGE}"\n')
        f_list.append(f'	"{self.app_name}/internal/forms"\n')
        f_list.append(f'	\n')
        f_list.append(f'	"dev.azure.com/netkit/unknown/gokit.git/logger"\n')
        f_list.append(f'	"github.com/google/wire"\n')
        f_list.append(f')\n\n')
        f_list.append(f'// {self.Name}Repo {self.zh_name}Repo\n')
        f_list.append(f'type {self.Name}Repo struct {{\n')
        f_list.append(f'	db {Global.GODAPRDBPACKAGE}.IDaprMysqlClient\n')
        f_list.append(f'}}\n\n')
        f_list.append(f'// I{self.Name}Repo {self.zh_name}Repo公开接口\n')
        f_list.append(f'type I{self.Name}Repo interface {{\n')
        f_list.append(f'	Create(form forms.{self.Name}CreateForm) error\n')
        f_list.append(f'	Update(id int, form forms.{self.Name}UpdateForm) error\n')
        f_list.append(f'	Get(id int) (*{self.Name}, error)\n')
        f_list.append(f'	List(query forms.{self.Name}Query) (int, []{self.Name}, error)\n')
        f_list.append(f'	Delete(ids []uint) error\n')
        f_list.append(f'}}\n\n')
        f_list.append(f'// {self.Name}RepoProviderSet {self.zh_name}IRepo公开接口与Repo绑定关系\n')
        f_list.append(f'var {self.Name}RepoProviderSet = wire.NewSet(New{self.Name}Repo, wire.Bind(new(I{self.Name}Repo), new(*{self.Name}Repo)))\n\n')
        f_list.append(f'func New{self.Name}Repo(db {Global.GODAPRDBPACKAGE}.IDaprMysqlClient) *{self.Name}Repo {{\n')
        f_list.append(f'	return &{self.Name}Repo{{\n')
        f_list.append(f'		db: db,\n')
        f_list.append(f'	}}\n')
        f_list.append(f'}}\n\n')
        f_list.append(f'// {self.Name} {self.zh_name}结构\n')
        f_list.append(f'type {self.Name} struct {{\n')
        f_list.append(self.make_column_format("gin_api_model_struct_arg", 1))
        f_list.append(f'}}\n\n')

        f_list.append(f'// @title: Create\n')
        f_list.append(f'// @description: 插入{self.zh_name}表一条数据\n')
        f_list.append(f'// @author: rong {self.now_date}\n')
        f_list.append(f'// @param: from froms.{self.Name}CreateForm {self.zh_name}创建表单\n')
        f_list.append(f'// @return err error 错误或者无错误就是成功\n')
        f_list.append(f'func (r *{self.Name}Repo) Create(form forms.{self.Name}CreateForm) error {{\n')
        f_list.append(self.make_column_format("go_gin_dapr_repo_create_marshal", 1))
        f_list.append(f'\n    // 将form内数据插入{self.Name}表中 \n')
        f_list.append(f'	sqlStr := fmt.Sprintf("INSERT INTO `{self.names}` ({self.make_column_format("sql_create_col_name")[:-1]}) VALUES ({self.make_column_format("go_sql_create_format_percent")[:-1]})", {self.make_column_format("go_form_sql_create_format")[:-2]})\n')
        f_list.append(f'	logger.Debug("sql string: ", sqlStr)\n')
        f_list.append(f'	if _, err := r.db.Exec(sqlStr); err != nil {{\n')
        f_list.append(f'		logger.Error(err)\n')
        f_list.append(f'		return err\n')
        f_list.append(f'	}}\n')
        f_list.append(f'	return nil\n}}\n\n')
       
        f_list.append(f'// @title: Update\n')
        f_list.append(f'// @description: 修改{self.zh_name}表一条数据\n')
        f_list.append(f'// @author: rong {self.now_date}\n')
        f_list.append(f'// @param: id int {self.zh_name}ID\n')
        f_list.append(f'//         from froms.{self.Name}UpdateForm {self.zh_name}修改表单\n')
        f_list.append(f'// @return err error 错误或者无错误就是成功\n')
        f_list.append(f'func (r *{self.Name}Repo) Update(id int, form forms.{self.Name}UpdateForm) error {{\n')
        f_list.append(f'    // 声明build用来组合sql sting\n')
        f_list.append(f'	var build strings.Builder\n')
        f_list.append(f'	build.WriteString("UPDATE `{self.names}` SET ")\n\n')
        f_list.append(f'    // 声明sqlvals用来添加要更新的key = value\n')
        f_list.append(f'	var sqlvals []string\n\n')
        f_list.append(self.make_column_format("go_gin_dapr_repo_create_marshal", 1))
        f_list.append(self.make_column_format("go_gin_dapr_repo_update_sql", 1))
        f_list.append(f'\n    // 判断是否有需要修改的数据，如果没有，返回更新参数错误\n')
        f_list.append(f'    if len(sqlvals) == 0 {{\n')
        f_list.append(f'    	return errors.New(ErrorNoUpdateArgs)\n	}}\n')
        f_list.append(f'\n    // 将sqlvals用逗号合并，然后build合成sql对数据库进更新\n')
        f_list.append(f'    build.WriteString(strings.Join(sqlvals, ","))\n')
        f_list.append(f'    build.WriteString(fmt.Sprintf(" WHERE `id` =  %d", id))\n')
        f_list.append(f'    logger.Debug("sql string: ", build.String())\n')
        f_list.append(f'	if _, err := r.db.Exec(build.String()); err != nil {{\n')
        f_list.append(f'		logger.Error(err)\n')
        f_list.append(f'		return err\n	}}\n')
        f_list.append(f'	return nil\n}}\n\n')

        f_list.append(f'// @title: Get\n')
        f_list.append(f'// @description: 获取{self.zh_name}表一条数据\n')
        f_list.append(f'// @author: rong {self.now_date}\n')
        f_list.append(f'// @param: id int 要查询的{self.zh_name}Id\n')
        f_list.append(f'// @return *{self.Name} {self.zh_name}详情结构体\n')
        f_list.append(f'//         err error 错误或者无错误就是成功\n')
        f_list.append(f'func (r *{self.Name}Repo) Get(id int) (*{self.Name}, error) {{\n')
        f_list.append(f'    // 声明resp用来存查询获得的数据\n')
        f_list.append(f'	var resp []{self.Name}\n')
        f_list.append(f'\n    // 使用{self.zh_name}{self.index.Name}查询数据\n')
        f_list.append(f'	sqlStr := fmt.Sprintf("SELECT * FROM `{self.names}` WHERE id = %d", id)\n')
        f_list.append(f'    out, err := r.db.Query(sqlStr)\n')
        f_list.append(f'    if err != nil {{\n    	return nil, err\n	}}\n')
        f_list.append(f'\n    // 解析查询返回的数据\n')
        f_list.append(f'    err = json.Unmarshal(out.Data, &resp)\n')
        f_list.append(f'    if err != nil {{\n')
        f_list.append(f'    	return nil, err\n')
        f_list.append(f'	}}\n')
        f_list.append(f'\n    // 如果返回的数据少于1条，说明没有找到，返回没找到错误\n')
        f_list.append(f'    if len(resp) < 1 {{\n')
        f_list.append(f'    	return nil, errors.New(ErrorNotFound)\n')
        f_list.append(f'	}}\n')
        f_list.append(self.make_column_format("go_gin_dapr_repo_get_unmarshal", 1))
        f_list.append(f'    return &resp[0], nil\n}}\n\n')

        f_list.append(f'// @title: List\n')
        f_list.append(f'// @description: 获取{self.zh_name}列表\n')
        f_list.append(f'// @author: rong {self.now_date}\n')
        f_list.append(f'// @param: query forms.{self.Name}Query 请求{self.zh_name}分页表单\n')
        f_list.append(f'// @return int 列表数据总条数\n')
        f_list.append(f'//          []{self.Name} {self.zh_name}详细信息切片\n')
        f_list.append(f'//          err error 错误或者无错误就是成功\n')
        f_list.append(f'func (r *{self.Name}Repo) List(query forms.{self.Name}Query) (count int, {self.names} []{self.Name}, err error) {{\n')
        f_list.append(f'    // 声明resp用来存查询获得的数据\n')
        f_list.append(f'	var resp []{self.Name}\n')
        f_list.append(f'	where := ""\n')
        f_list.append(self.make_column_format("go_gin_dapr_repo_list_sql_like", 1))
        f_list.append(f'\n    // 查询总数据条数并解析出值count\n')
        f_list.append(f'	countSql := fmt.Sprintf("SELECT count(id) AS count FROM {self.names}%s", where)\n')
        f_list.append(f'	out, err := r.db.Query(countSql)\n')
        f_list.append(f'	if err != nil {{\n')
        f_list.append(f'		logger.Error(err)\n')
        f_list.append(f'		return 0, nil, err\n')
        f_list.append(f'	}}\n')
        f_list.append(f'	count, err = UnmarshalCount(out.Data)\n')
        f_list.append(f'	if count <= 0 {{\n')
        f_list.append(f'		return 0, {self.names}, nil\n')
        f_list.append(f'	}}\n')
        f_list.append(f'\n    // 判断要获取的数据起始序号，如果它大于总数据条数，说明没有符合的数据分段，直接返回空切片\n')
        f_list.append(f'	offset := (query.Current - 1) * query.PerPage\n')
        f_list.append(f'	if offset >= count {{\n')
        f_list.append(f'	    return count, {self.names}, nil\n')
        f_list.append(f'	}}\n')
        f_list.append(f'\n    // 查询分页数据并解析到{self.Name}切片当中\n')
        f_list.append(f'	sqlstr := fmt.Sprintf("SELECT * FROM `{self.names}` %s LIMIT %d, %d", where, offset, query.PerPage)\n')
        f_list.append(f'	out, err = r.db.Query(sqlstr)\n')
        f_list.append(f'	if err != nil {{\n')
        f_list.append(f'		return 0, nil, err\n')
        f_list.append(f'	}}\n')
        f_list.append(f'	err = json.Unmarshal(out.Data, &resp)\n')
        f_list.append(f'	if err != nil {{\n')
        f_list.append(f'		return 0, nil, err\n')
        f_list.append(f'	}}\n')
        f_list.append(f'\n    // 循环{self.Name}切片resp，将json字段解析为json数据更新到新的{self.Name}切片{self.names}当中，并返回该新切片\n')
        f_list.append(f'	for _, {self.name} := range resp {{\n')
        f_list.append(self.make_column_format("go_gin_dapr_repo_list_sql_unmarshal_json", 1))
        f_list.append(f'	}}\n\n')
        f_list.append(f'	return count, {self.names}, nil\n')
        f_list.append(f'}}\n\n')
        f_list.append(f'// @title: Delete\n')
        f_list.append(f'// @description: 批量删除{self.zh_name}\n')
        f_list.append(f'// @author: rong {self.now_date}\n')
        f_list.append(f'// @param: ids []uint {self.zh_name}ID切片\n')
        f_list.append(f'// @return err error 错误或者无错误就是成功\n')
        f_list.append(f'func (r *{self.Name}Repo) Delete(ids []uint) error {{\n')
        f_list.append(f'    // 将数字切片ids []uint转化为[]string,里面的数字都变为string类型\n')
        f_list.append(f'	idsStrList := ArrayUint2Str(ids)\n')
        f_list.append(f'\n    // 用逗号合并id切片为一条字符串偏于sql中执行\n')
        f_list.append(f'	idsStr := strings.Join(idsStrList, ",")\n')
        f_list.append(f'\n    // sql执行删除操作,删掉包含在id列表里面的行\n')
        f_list.append(f'	sqlstr := fmt.Sprintf("DELETE FROM `{self.names}` WHERE `id` IN (%s)", idsStr)\n')
        f_list.append(f'	_, err := r.db.Exec(sqlstr)\n')
        f_list.append(f'	if err != nil {{\n')
        f_list.append(f'		return err\n')
        f_list.append(f'	}}\n')
        f_list.append(f'	return nil\n')
        f_list.append(f'}}\n\n')


        return {file_path:f_list}

    def make_gin_dapr_internal_forms(self, project_dir):
        file_path =  os.path.join(project_dir,f"internal/forms/{self.name}.go")
        f_list = []

        f_list.append(f'// @Title  {self.name}.go\n')
        f_list.append(f'// @Description  {self.zh_name}表单\n')
        f_list.append(f'// @Autor: rong	{self.now_date}\n')
        f_list.append(f'// @Update:\n')
        f_list.append(f'package forms\n\n')
        f_list.append(f'// {self.Name}CreateForm {self.zh_name}创建表单\n')
        f_list.append(f'type {self.Name}CreateForm struct {{\n')
        f_list.append(self.make_column_format("gin_api_create_valid", 1))
        f_list.append(f'}}\n\n')
        f_list.append(f'// {self.Name}UpdateForm {self.zh_name}修改表单\n')
        f_list.append(f'type {self.Name}UpdateForm struct {{\n')
        f_list.append(self.make_column_format("gin_api_update_valid", 1))
        f_list.append(f'}}\n\n')
        f_list.append(f'// {self.Name}Query 请求{self.zh_name}分页表单\n')
        f_list.append(f'type {self.Name}Query struct {{\n')
        f_list.append(self.make_column_format("gin_api_query_list_valid", 1))
        f_list.append(f'	PerPage int `form:"per_page"`\n')
        f_list.append(f'	Current int `form:"current"`\n')
        f_list.append(f'}}\n\n')

        return {file_path:f_list}