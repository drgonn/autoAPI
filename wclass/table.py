import os
from wclass.parent import Parent, Many, Son
from tools import name_convert
from wclass.column import Column
import json
import random


tab = "    "


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


        # if table.get('detail_sons') is not None:
        #     api_list_list.append(f"@api.route('/{self.name}/list/detail', methods=['GET'])\n")
        #     api_list_list.append(f"def list_detail_{self.name}():\n")
        #     api_list_list.append(f"{tab}print(request.args)\n")
        #     api_list_list.append(f"{tab}sorter = request.args.get('sorter')\n")
        #     api_list_list.append(f"{tab}page = int(request.args.get('current', 1))\n")
        #     api_list_list.append(f"{tab}pageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))\n")
        #     api_list_list.append(f"{tab}pageSize = 20 if pageSize < 10 else pageSize\n")

        #     if table.get('userfilter'):
        #         api_list_list.append(f"\n{tab}if is_admin():\n")
        #         if table.get('appfilter'):
        #             api_list_list.append(f"{tab}{tab}total_{self.names} = {self.Name}.query.filter_by(app_id=g.app.id)\n")
        #         else:
        #             api_list_list.append(f"{tab}{tab}total_{self.names} = {self.Name}.query\n")
        #         api_list_list.append(f"{tab}else:\n")
        #         api_list_list.append(f"{tab}{tab}total_{self.names} = g.current_user.{self.names}\n")
        #     else:
        #         if table.get('appfilter'):
        #             api_list_list.append(f"{tab}total_{self.names} = {self.Name}.query.filter_by(app_id=g.app.id)\n")
        #         else:
        #             api_list_list.append(f"{tab}total_{self.names} = {self.Name}.query\n")

        #     if self.many:
        #         for many in self.may:
        #             many.Name = many.Name
        #             many.name = many.Name.lower()
        #             api_list_list.append(f"\n{tab}{many.name}_id = request.args.get('{many.name}_id')\n")
        #             api_list_list.append(f"{tab}if {many.name}_id is not None:\n")
        #             api_list_list.append(f"{tab}{tab}{many.name} = {many.Name}.query.filter_by(id={many.name}_id).first()\n")
        #             api_list_list.append(f"{tab}{tab}if {many.name} is None:\n")
        #             api_list_list.append(
        #                 f"""{tab}{tab}{tab}return jsonify({{'success':False,'error_code':-1,'errmsg':f'{many.name}:{{{many.name}_id}}不存在'}})\n""")
        #             api_list_list.append(f"{tab}{tab}else:\n")

        #             api_list_list.append(f"{tab}{tab}{tab}total_{self.names} = {many.name}.{self.name}s\n\n")
        #     for parent in self.parents:
        #         parent.Name = parent.get('name')
        #         parent.name = parent.Name.lower()
        #         if parent.post:
        #             index = parent.index
        #             argname = f"{parent.name}_{parent.index}"
        #             api_list_list.append(f"\n{tab}{argname} = request.args.get('{argname}')\n")
        #             api_list_list.append(f"{tab}if {argname} is not None:\n")
        #             api_list_list.append(f"{tab}{tab}{parent.name} = {parent.Name}.query.filter_by({index}={argname}).first()\n")
        #             api_list_list.append(f"{tab}{tab}if {parent.name} is None:\n")
        #             api_list_list.append(f"""{tab}{tab}{tab}return jsonify({{'success':False,'error_code':-1,'errmsg':'{argname}不存在'}})\n""")
        #             api_list_list.append(
        #                 f"{tab}{tab}else:\n{tab}{tab}{tab}total_{self.names} = total_{self.names}.filter_by({parent.name}_id={parent.name}.id)\n")

        #     for column in self.columns:
        #         filter = column.get('filter')
        #         # print(self.name,filter,column,table)
        #         if filter:
        #             argname = column.name
        #             api_list_list.append(f"{tab}{argname} = request.args.get('{argname}')\n")
        #             api_list_list.append(f"{tab}if {argname} is not None:\n")
        #             if filter == "like":
        #                 api_list_list.append(
        #                     f"{tab}{tab}total_{self.names} = total_{self.names}.filter({self.Name}.{argname}.ilike(f'%{{{argname}}}%'))\n\n")
        #             elif filter == "precise":
        #                 api_list_list.append(f"{tab}{tab}total_{self.names} = total_{self.names}.filter_by({argname}={argname})\n\n")
        #     api_list_list.append(f"{tab}if sorter:\n")
        #     api_list_list.append(f"{tab}{tab}sorter = json.loads(sorter)\n")

        #     for column in self.columns:
        #         if column.sorter:
        #             argname = column.name
        #             api_list_list.append(f"{tab}{tab}if sorter.get('{argname}') == 'ascend':\n")
        #             api_list_list.append(f"{tab}{tab}{tab}total_{self.names} = total_{self.names}.order_by({self.Name}.{argname}.asc())\n")
        #             api_list_list.append(f"{tab}{tab}elif sorter.get('{argname}') == 'descend':\n")
        #             api_list_list.append(f"{tab}{tab}{tab}total_{self.names} = total_{self.names}.order_by({self.Name}.{argname}.desc())\n")
        #     api_list_list.append(f"{tab}{tab}pass\n")
        #     api_list_list.append(f"{tab}totalcount = total_{self.names}.with_entities(func.count({self.Name}.id)).scalar()\n")
        #     api_list_list.append(f"{tab}page = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page\n")
        #     api_list_list.append(f"{tab}pagination = total_{self.names}.paginate(page, per_page = pageSize, error_out = False)\n")
        #     api_list_list.append(f"{tab}{self.names} = pagination.items\n")
        #     api_list_list.append(f"""\n{tab}return jsonify({{
        #                 'success':True,
        #                 'error_code':0,
        #                 'total':totalcount,
        #                 "pageSize" : pageSize,
        #                 "current" : page,
        #                 "pagecount": pagination.pages,
        #                 'data':[{self.name}.to_detail() for {self.name} in {self.names}]
        #                 }})""")
        #     api_list_list.append(f"\n")
        #     api_list_list.append(f"\n")

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
        apidir = "w" + os.path.join(appdir, f'apiv1/{self.name}.py')

        # 加入导入包
        target_str_list += import_list
        target_str_list += api_get_list
        target_str_list += api_post_list
        target_str_list += api_put_list
        target_str_list += api_delete_list
        target_str_list += api_list_list

        return {apidir:target_str_list}

    def write_test_yapi(self,project_dir):
        r = []
        crud = [
                ("创建", "POST", '', False),
                ("列表", "GET", '/list', '$.data.records[-1].id'),
                ("单个获取", "GET", '/<id>', False),
                ("修改", "PUT", '/<id>', False),
                ("删除", "DELETE", '', False),
                ]
        if self.api_need:
            gp = {}
            gp['index'] = 0
            gp['name'] = self.zh_name
            gp['desc'] = self.zh_name
            gp['list'] = []            
            write_addr = "w" + os.path.join(project_dir, f'test/yapi/{self.name}.json')
            son_list=[]
            for typezh, method, p, argaddr in crud:
                prefix = "/"+self.url_prefix if self.url_prefix else ""
                path = f"{prefix}/{self.name}"
                req_query_list = [
                {
                    "required": "1",
                    "_id": "6052fca844868a00946ae536",
                    "name": "token",
                    "desc": ""
                }]
            
                pjson = {"type":"object",
                        "title":"empty object",
                        "properties":
                            {
                            },
                        "required":[]
                        }
                listjson = {"type": "object",
                    "title": "empty object",
                    "properties":
                        {"success":
                            {"type": "boolean",
                            "description": "返回成功",
                            "mock": {"mock": "true"}
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
                    "required":["success", "data"]
                    }
                getjson = {"type": "object",
                            "title": "empty object",
                            "properties":
                                {"success":
                                    {"type": "boolean",
                                    "description": "返回成功",
                                    "mock": {"mock": "true"}
                                    },
                                "record":
                                    {"type": "object",
                                    "properties": {
                                        "id": {"type": "integer", "description": "id"},
                                    },
                                    "required": ["id"]}
                                },
                            "required":["success", "record"]
                            }
                sjson = {"type": "object",
                        "title": "empty object",
                        "properties":
                            {
                                "success":
                                    {"type": "boolean",
                                    "description": "返回成功",
                                    "mock": {"mock": "true"}
                                    },
                                "error_code":
                                    {"type": "integer",
                                        "description": "错误码",
                                        "mock": {"mock": 0}
                                        },

                        },
                        "required": ["success", "error_code"]
                        }
                if typezh == "创建":
                    for column in self.columns:
                        if column.post:
                            pjson["properties"][column.name] = {
                                "type":column.type_long_lower,
                                "description":f"{self.zh_name}{column.mean}{column.map_mean}",
                                "mock":{"mock":str(column.random_arg())}}
                            if column.post == 2:
                                pjson["required"].append(column.name)
                    rstr = json.dumps(sjson)

                    for parent in self.parents:
                        if parent.post and parent.Name != 'User':
                            pjson["properties"][parent.name+"_id"] = {"type":"integer","description":parent.mean,
                                "mock":{"mock":str(random.randint(0, 9))}}
                elif typezh == "单个获取":
                    pjson["properties"]['current'] = {"type":"integer","description":"访问页"}
                    pjson["properties"]['pageSize'] = {"type":"integer","description":"单页条数"}
                    for column in self.columns:
                        if column.post:
                            getjson["properties"]['record']["properties"][column.name]= {"type": column.type_long_lower, "description": self.zh_name+column.mean + column.map_mean}
                            getjson["properties"]['record']["required"].append(column.name)
                    getjson["properties"]['record']["required"].append("token")
                    rstr = json.dumps(getjson)
                elif typezh == "列表":
                    sorter = {}
                    pjson["properties"]['current'] = {"type": "integer", "description": "访问页"}
                    pjson["properties"]['pageSize'] = {"type": "integer", "description": "单页条数"}
                    pjson["properties"]['token'] = {"type":"string","description":"token"}
                    for column in self.columns:
                        if column.post:
                            listjson["properties"]['data']['items']["properties"][column.name] = {"type": column.type_long_lower,"description": self.zh_name + column.mean + column.map_mean}
                            listjson["properties"]['data']['items']["required"].append(column.name)
                        if column.list:
                            req_query_list.append({"required":"0","name":column.name,"desc":column.mean + column.map_mean + (column.about or '')})
                    for m in self.many:
                        req_query_list.append({"required":"0","name":f"{m.prefix}{m.name}_id"})
                        
                            
                    rstr = json.dumps(listjson)
                    
                elif typezh == "修改":
                    rstr = json.dumps(sjson)
                    # for column in self.columns:
                    #     if column.put:
                    #         pjson[column.name] = column.random_arg()
                    for column in self.columns:
                        if column.put:
                            pjson["properties"][column.name] = {
                                "type": column.type_long_lower, 
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
                    rstr = json.dumps(sjson)
                    pjson["properties"]["ids"] = {"type": "array", "description": "要删除的id数组","items":{"type":"integer"}}
                pjsonstr = json.dumps(pjson)
                if p == '/<id>':
                    path += '/{id}'
                else:
                    path += p
                single_api = self.single_str(self.zh_name, typezh,  path, method, pjsonstr, rstr,req_query_list)
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
            "status": "done",
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
        model_dir = "w"+os.path.join(project_dir,f'src/models/{self.Name}.py')

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

    def make_go_gin(self,project_dir):        
        return {
            **self.make_gin_internal_routers(project_dir),
            **self.make_gin_internal_service(project_dir),
            **self.make_gin_internal_dao(project_dir),
            **self.make_gin_internal_model(project_dir),
        }

    def make_gin_internal_routers(self, project_dir):
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
        t_dir = "w" + os.path.join(project_dir,f"internal/routers/api/v1/{self.name}.go")
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
        t_dir = "w" + os.path.join(project_dir,f"internal/service/{self.name}.go")
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
        t_dir = "w" + os.path.join(project_dir,f"internal/dao/{self.name}.go")
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
        t_dir = "w" + os.path.join(project_dir,f"internal/model/{self.name}.go")
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
            t_list.append(f'	sqlStr := "insert into {self.name}s ({self.make_column_format("gin_api_model_create_sql")[:-1]}) values ({self.make_column_format("gin_api_model_create_sql_?")[:-1]})"\n')
            t_list.append(f'	ret, err := db.Exec(sqlStr,{self.make_column_format("gin_api_model_create_exec_arg")[:-1]})\n')
        else:
            t_list.append(f'	{self.index.name} := uuid.NewV4().String()\n')
            t_list.append(f'	sqlStr := "insert into {self.name}s ({self.make_column_format("gin_api_model_create_sql")}`{self.index.name}`) values ({self.make_column_format("gin_api_model_create_sql_?")} ?)"\n')
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



    



