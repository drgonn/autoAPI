import os




def write_apis(root,ojson):
    tab = "    "
    app = ojson.get('app')
    appdir = os.path.join(root, f'{app}/src/app')

    for table in ojson.get('databases'):
        target_str_list=[]
        import_list = []  
        api_get_list=[]
        api_post_list=[]
        api_put_list=[]
        api_delete_list=[]
        api_list_list=[]
        commit_get_list=[]
        commit_post_list=[]
        commit_put_list=[]
        commit_delete_list=[]
        commit_list_list=[]
        if not table.get('api'):
            continue
        tableclass = table.get('table')
        tablenames = table.get('table').lower() + 's'
        tablename = table.get('table').lower()
        apifile = table.get('table')
        zh = table.get('zh')
        apidir = os.path.join(appdir,f'apiv1/{apifile}.py')
        w = open(apidir,'w+')
        im = """
import json
import logging
import math
import os
import shutil

from app import db
from app.apiv1 import api
from flask import request, jsonify, current_app, g
from sqlalchemy import func

"""
        import_list.append(im)
        import_list.append(f"from app.models import {tableclass}")
        for parent in table.get('parents'):
            parentname = parent.get('name')
            import_list.append(f",{parentname}")
        if table.get('many'):
            for many in table.get('many'):
                manyclass = many.get('name')
                import_list.append(f",{manyclass}")
        import_list.append("\n\n")


        for column in table.get('args'):
            argname = column.get('name')

        api_get_list.append(f"\n@api.route('/{tablename}/<int:id>', methods=['GET'])\n")
        api_get_list.append(f"def get_{tablename}(id):\n")
        commit_get_list.append(f'{tab*1}"""get单个{zh}接口\n\n')
        commit_get_list.append(f'{tab*1}Params:\n')
        commit_get_list.append(f'{tab*2}id: {zh}ID\n')
        commit_get_list.append(f'{tab*1}Returns:\n')
        commit_get_list.append(f'{tab*2}success: bool类型，请求成功与否\n')
        commit_get_list.append(f'{tab*2}error_code: int类型，错误代码，成功为0\n')
        commit_get_list.append(f'{tab*2}records: 对象，{zh}的详细参数\n')
        commit_get_list.append(f'{tab*1}"""\n')
        api_get_list.append(f"{tab}{tablename} = {tableclass}.query.get_or_404(id)\n")
        to_what = 'to_json' #if table.get('nodetail') else 'to_detail'

        api_get_list.append(f"""\n{tab}return jsonify({{'success': True,
                    'error_code': 0,
                    'records': {tablename}.{to_what}(),
                    }})""")
        api_get_list.append(f"\n\n")

        api_post_list.append(f"@api.route('/{tablename}', methods=['POST'])\n")
        api_post_list.append(f"def create_{tablename}():\n")
        commit_post_list.append(f'{tab*1}"""post创建单个{zh}接口\n\n')
        commit_post_list.append(f'{tab*1}requests:\n')
        commit_post_list.append(f'{tab*1}Returns:\n')
        commit_post_list.append(f'{tab*2}success: bool类型，请求成功与否\n')
        commit_post_list.append(f'{tab*2}error_code: int类型，错误代码，成功为0\n')
        commit_post_list.append(f'{tab*2}id: {zh}ID\n')
        commit_post_list.append(f'{tab*1}"""\n')
        api_post_list.append(f"{tab}print(request.json)\n")
        for column in table.get('args'):
            if column.get('post') or column.get("file"):
                argname = column.get('name')
                argmean = column.get('zh')
                api_post_list.append(f"{tab}{argname} = request.json.get('{argname}')\n")
                commit_post_list.insert(2, f"{tab*2}{argname}: {argmean}\n")
            if column.get('postmust'):
                api_post_list.append(f"{tab}if {argname} is None:\n")
                api_post_list.append(f"{tab}{tab}return jsonify({{'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：{argname}'}})\n")
        for parent in table.get('parents'):
            parentname = parent.get('name')
            parentmean = parent.get('zh')
            parenttablename = parentname.lower()
            if parent.get('name') == 'User':
                api_post_list.append(f"{tab}{parenttablename} = g.current_user\n ")
            elif parent.get('post'):
                index = parent.get('index')
                argname = f"{parenttablename}_{parent.get('index')}"
                api_post_list.append(f"\n{tab}{argname} = request.json.get('{argname}')\n")
                must = "，非必填"
                if parent.get('post')==2:
                    api_post_list.append(f"{tab}{parenttablename} = {parentname}.query.filter_by({index}={argname}).first()\n ")
                    api_post_list.append(f"\n{tab}if {parenttablename} is None:\n")
                    api_post_list.append(f"""{tab}{tab}return jsonify({{'success':False,'error_code':-1,'errmsg':'{argname}不存在'}})""")
                    api_post_list.append(f"{tab}\n")
                    must= "，必填"

                commit_post_list.insert(2, f"{tab*2}{parenttablename}_{parent.get('index')}: {parentmean}{must}\n")
        api_post_list.append(f"\n{tab}{tablename} = {tableclass}(")
        for column in table.get('args'):
            if column.get('post') or column.get("file"):
                argname = column.get('name')
                api_post_list.append(f"{argname}={argname},")
        for parent in table.get('parents'):
            parentname = parent.get('name')
            parenttablename = parentname.lower()
            if parent.get('post'):
                api_post_list.append(f"{parenttablename}_id={parenttablename}.id,")
        if table.get('appfilter'):
            api_post_list.append(f"app_id=g.app.id,")
        api_post_list.append(f")\n")

        for column in table.get('args'):
            if column.get('file'):
                argname = column.get('name')
                api_post_list.append(f"""{tab}static_folder = current_app.config['STATIC_FOLDER']\n""")
                api_post_list.append(f"""{tab}user_dir = os.path.join(static_folder, 'user_folder', f"{{g.current_user.uid}}")\n""")
                api_post_list.append(f"""{tab}tmp_file_path = os.path.join(user_dir, {argname})\n""")
                api_post_list.append(f"""{tab}if not os.path.exists(tmp_file_path):\n""")
                api_post_list.append(f"""{tab}{tab}return jsonify({{'success':False,'error_code':-1,'errmsg':f'文件{{tmp_file_path}}不存在'}})\n""")

        if table.get("many"):
            for many in table.get('many'):
                manyclass = many.get('name')
                manyname = many.get('name').lower()
                api_post_list.append(f"\n{tab}{manyname}_ids = request.json.get('{manyname}_ids') or []\n")
                api_post_list.append(f"{tab}for {manyname}_id in {manyname}_ids:\n")
                api_post_list.append(f"{tab}{tab}{manyname} = {manyclass}.query.filter_by(id={manyname}_id)\n")
                api_post_list.append(f"{tab}{tab}if {manyname} is None:\n")
                api_post_list.append(f"{tab}{tab}{tab}return jsonify({{'success':False,'error_code':-1,'errmsg':'{manyname}ID不存在'}})\n")
                api_post_list.append(f"{tab}{tab}{tablename}.{manyname}s.append({manyname})\n")
                api_post_list.append(f"{tab}\n")

        api_post_list.append(f"\n{tab}db.session.add({tablename})\n")
        api_post_list.append(f"{tab}try:\n{tab}{tab}db.session.commit()\n")
        for column in table.get('args'):
            if column.get('file'):
                argname = column.get('name')
                api_post_list.append(f"""{tab}{tab}dst_dir = os.path.join(static_folder, '{tablename}{argname}', f"{{{tablename}.id}}")\n""")
                api_post_list.append(f"""{tab}{tab}dst_file_path = os.path.join(dst_dir, {argname})\n""")
                api_post_list.append(f"""{tab}{tab}os.makedirs(dst_dir,exist_ok=True)\n""")
                api_post_list.append(f"""{tab}{tab}shutil.move(tmp_file_path,dst_file_path)\n""")
                api_post_list.append(f"""{tab}{tab}shutil.rmtree(user_dir)\n""")

        api_post_list.append(f"{tab}except Exception as e:\n{tab}{tab}db.session.rollback()\n")
        api_post_list.append(f"{tab}{tab}logging.error(f'添加数据库发生错误,已经回退:{{e}}')\n")
        api_post_list.append(f"{tab}{tab}return jsonify({{'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'}})\n")
        api_post_list.append(f"""\n{tab}return jsonify({{'success': True,
                    'error_code': 0,
                    'id': {tablename}.id,
                    }})""")
        api_post_list.append(f"\n\n")



        api_put_list.append(f"@api.route('/{tablename}/<int:id>', methods=['PUT'])\n")
        api_put_list.append(f"def modify_{tablename}(id):\n")
        api_put_list.append(f"{tab}print('put json:',request.json)\n")
        api_put_list.append(f"{tab}{tablename} = {tableclass}.query.get_or_404(id)\n")
        for column in table.get('args'):
            if column.get('putneed'):
                argname = column.get('name')
                if argname == "id":
                    api_put_list.append(f"{tab}new_{argname} = request.json.get('new_{argname}')\n")
                else:
                    api_put_list.append(f"{tab}{argname} = request.json.get('{argname}')\n")
        for parent in table.get('parents'):
            parentname = parent.get('name')
            parenttablename = parentname.lower()
            if parent.get('putneed'):
                index = parent.get('index')
                argname = f"{parenttablename}_{parent.get('index')}"
                api_put_list.append(f"{tab}{argname} = request.json.get('{argname}')\n")
                api_put_list.append(f"{tab}{parenttablename} = {parentname}.query.filter_by({index}={argname}).first()\n")
                api_put_list.append(f"{tab}if {parenttablename} is None:\n")
                api_put_list.append(f"""{tab}{tab}return jsonify({{'success':False,'error_code':-1,'errmsg':'{argname}不存在'}})""")
                api_put_list.append(f"{tab}\n")

        for column in table.get('args'):
            if column.get('putneed'):
                argname = column.get('name')
                if argname == "id":
                    api_put_list.append(f"{tab}{tablename}.{argname} = new_{argname} or {tablename}.{argname}\n")
                else:
                    api_put_list.append(f"{tab}{tablename}.{argname} = {argname} or {tablename}.{argname}\n")
        for parent in table.get('parents'):
            parentname = parent.get('name')
            parenttablename = parentname.lower()
            if parent.get('putneed'):
                api_put_list.append(f"{tab}{tablename}.{parenttablename}_id = {parenttablename}.id\n")
        if table.get("many"):
            for many in table.get('many'):
                if many.get('add_api'):
                    manyclass = many.get('name')
                    manyname = many.get('name').lower()
                    api_put_list.append(f"\n{tab}add_{manyname}_ids = request.json.get('add_{manyname}_ids')\n")
                    api_put_list.append(f"{tab}if add_{manyname}_ids:\n")
                    api_put_list.append(f"{tab}{tab}original_ids = [{manyname}.id for {manyname} in {tablename}.{manyname}s.all()]\n")
                    api_put_list.append(f"{tab}{tab}new_ids = list(set(add_{manyname}_ids).difference(set(original_ids)))\n")
                    api_put_list.append(f"{tab}{tab}for {manyname}_id in new_ids:\n")
                    api_put_list.append(f"{tab}{tab}{tab}{manyname} = {manyclass}.query.filter_by(id={manyname}_id).first()\n")
                    api_put_list.append(f"{tab}{tab}{tab}if {manyname} is None:\n")
                    api_put_list.append(f"{tab}{tab}{tab}{tab}return jsonify({{'success':False,'error_code':-1,'errmsg':'{manyname}ID不存在'}})\n")
                    api_put_list.append(f"{tab}{tab}{tab}{tablename}.{manyname}s.append({manyname})\n")

                    api_put_list.append(f"\n{tab}remove_{manyname}_ids = request.json.get('remove_{manyname}_ids')\n")
                    api_put_list.append(f"{tab}if remove_{manyname}_ids:\n")

                    api_put_list.append(f"{tab}{tab}original_ids = [{manyname}.id for {manyname} in {tablename}.{manyname}s.all()]\n")
                    api_put_list.append(f"{tab}{tab}remove_ids = list(set(remove_{manyname}_ids).intersection(set(original_ids)))\n")
                    api_put_list.append(f"{tab}{tab}for {manyname}_id in remove_ids:\n")
                    api_put_list.append(f"{tab}{tab}{tab}{manyname} = {manyclass}.query.filter_by(id={manyname}_id).first()\n")
                    api_put_list.append(f"{tab}{tab}{tab}{tablename}.{manyname}s.remove({manyname})\n")
                    api_put_list.append(f"{tab}{tab}\n")

        api_put_list.append(f"{tab}db.session.add({tablename})\n")
        api_put_list.append(f"\n{tab}try:\n{tab}{tab}db.session.commit()\n{tab}except Exception as e:\n{tab}{tab}db.session.rollback()\n")
        api_put_list.append(f"{tab}{tab}logging.error(f'修改数据库发生错误,已经回退:{{e}}')\n")
        api_put_list.append(f"""{tab}return jsonify({{'success':True,
                    'error_code':0,
                    }})""")
        api_put_list.append(f"\n\n")



        api_delete_list.append(f"@api.route('/{tablename}', methods=['DELETE'])\n")
        api_delete_list.append(f"def delete_{tablename}():\n")
        api_delete_list.append(f"{tab}print('delete json:',request.json)\n")
        api_delete_list.append(f"{tab}ids = request.json.get('ids')\n")
        api_delete_list.append(f"{tab}for id in ids:\n")
        api_delete_list.append(f"{tab}{tab}{tablename} = {tableclass}.query.get(id)\n")
        api_delete_list.append(f"{tab}{tab}if {tablename} is None:\n")
        api_delete_list.append(f"""{tab}{tab}{tab}return jsonify({{'success': False, 'error_code': -123, 'errmsg': f'删除错误，id： {{id}} 不存在'}})\n""")


        for table1 in ojson.get('databases'):
            if table1.get('parents'):
                for parent in  table1.get("parents"):
                    if parent.get("name") == tableclass:
                        api_delete_list.append(f"{tab}{tab}if {tablename}.{table1.get('table').lower()}s.first() is not None:\n")
                        api_delete_list.append(f"{tab}{tab}{tab}return jsonify({{'success':False,'error_code':-1,'errmsg':'{tablename}还拥有{table1.get('table').lower()}，不能删除'}})\n")

        api_delete_list.append(f"{tab}{tab}db.session.delete({tablename})\n")
        api_delete_list.append(f"\n{tab}{tab}try:\n{tab}{tab}{tab}db.session.commit()\n")
        for column in table.get('args'):
            if column.get('file'):
                argname = column.get('name')
                api_delete_list.append(f"""{tab}{tab}{tab}static_folder = current_app.config['STATIC_FOLDER']\n""")
                api_delete_list.append(f"""{tab}{tab}{tab}dst_dir = os.path.join(static_folder, '{tablename}', f"{{{tablename}.id}}")\n""")
                api_delete_list.append(f"""{tab}{tab}{tab}shutil.rmtree(dst_dir)\n""")
        api_delete_list.append(f"{tab}{tab}except Exception as e:\n{tab}{tab}{tab}db.session.rollback()\n")
        api_delete_list.append(f"{tab}{tab}{tab}logging.error(f'删除数据库发生错误,已经回退:{{e}}')\n")
        api_delete_list.append(f"""{tab}{tab}{tab}return jsonify({{'success': False, 'error_code': -123, 'errmsg': f'删除数据发生错误， {{e}} '}})\n""")
        api_delete_list.append(f"""\n{tab}return jsonify({{'success':True,
                'error_code':0,
                }})""")
        api_delete_list.append(f"\n\n")



        api_list_list.append(f"@api.route('/{tablename}/list', methods=['GET'])\n")
        api_list_list.append(f"def list_{tablename}():\n")
        api_list_list.append(f"{tab}print(request.args)\n")
        api_list_list.append(f"{tab}sorter = request.args.get('sorter')\n")
        api_list_list.append(f"{tab}page = int(request.args.get('current', 1))\n")
        api_list_list.append(f"{tab}pageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))\n")
        api_list_list.append(f"{tab}pageSize = 20 if pageSize < 10 else pageSize\n")

        if table.get('userfilter'):
            api_list_list.append(f"\n{tab}if is_admin():\n")
            if table.get('appfilter'):
                api_list_list.append(f"{tab}{tab}total_{tablenames} = {tableclass}.query.filter_by(app_id=g.app.id)\n")
            else:
                api_list_list.append(f"{tab}{tab}total_{tablenames} = {tableclass}.query\n")
            api_list_list.append(f"{tab}else:\n")
            api_list_list.append(f"{tab}{tab}total_{tablenames} = g.current_user.{tablenames}\n")
        else:
            if table.get('appfilter'):
                api_list_list.append(f"{tab}total_{tablenames} = {tableclass}.query.filter_by(app_id=g.app.id)\n")
            else:
                api_list_list.append(f"{tab}total_{tablenames} = {tableclass}.query\n")

        if table.get("many"):
            for many in table.get('many'):
                manyclass = many.get('name')
                manyname = many.get('name').lower()
                api_list_list.append(f"\n{tab}{manyname}_id = request.args.get('{manyname}_id')\n")
                api_list_list.append(f"{tab}if {manyname}_id is not None:\n")
                api_list_list.append(f"{tab}{tab}{manyname} = {manyclass}.query.filter_by(id={manyname}_id).first()\n")
                api_list_list.append(f"{tab}{tab}if {manyname} is None:\n")
                api_list_list.append(f"""{tab}{tab}{tab}return jsonify({{'success':False,'error_code':-1,'errmsg':f'{manyname}:{{{manyname}_id}}不存在'}})\n""")
                api_list_list.append(f"{tab}{tab}else:\n")

                api_list_list.append(f"{tab}{tab}{tab}total_{tablenames} = {manyname}.{tablename}s\n\n")
        for parent in table.get('parents'):
            parentname = parent.get('name')
            parenttablename = parentname.lower()
            if parent.get('post'):
                index = parent.get('index')
                argname = f"{parenttablename}_{parent.get('index')}"
                api_list_list.append(f"\n{tab}{argname} = request.args.get('{argname}')\n")
                api_list_list.append(f"{tab}if {argname} is not None:\n")
                api_list_list.append(f"{tab}{tab}{parenttablename} = {parentname}.query.filter_by({index}={argname}).first()\n")
                api_list_list.append(f"{tab}{tab}if {parenttablename} is None:\n")
                api_list_list.append(f"""{tab}{tab}{tab}return jsonify({{'success':False,'error_code':-1,'errmsg':'{argname}不存在'}})\n""")
                api_list_list.append(f"{tab}{tab}else:\n{tab}{tab}{tab}total_{tablenames} = total_{tablenames}.filter_by({parenttablename}_id={parenttablename}.id)\n")



        for column in table.get('args'):
            filter = column.get('filter')
            # print(tablename,filter,column,table)
            if filter:
                argname = column.get('name')
                api_list_list.append(f"{tab}{argname} = request.args.get('{argname}')\n")
                api_list_list.append(f"{tab}if {argname} is not None:\n")
                if filter == "like":
                    api_list_list.append(f"{tab}{tab}total_{tablenames} = total_{tablenames}.filter({tableclass}.{argname}.ilike(f'%{{{argname}}}%'))\n\n")
                elif filter == "precise":
                    api_list_list.append(f"{tab}{tab}total_{tablenames} = total_{tablenames}.filter_by({argname}={argname})\n\n")
        api_list_list.append(f"{tab}if sorter:\n")
        api_list_list.append(f"{tab}{tab}sorter = json.loads(sorter)\n")

        for column in table.get('args'):
            if column.get("sorter"):
                argname = column.get('name')
                api_list_list.append(f"{tab}{tab}if sorter.get('{argname}') == 'ascend':\n")
                api_list_list.append(f"{tab}{tab}{tab}total_{tablenames} = total_{tablenames}.order_by({tableclass}.{argname}.asc())\n")
                api_list_list.append(f"{tab}{tab}elif sorter.get('{argname}') == 'descend':\n")
                api_list_list.append(f"{tab}{tab}{tab}total_{tablenames} = total_{tablenames}.order_by({tableclass}.{argname}.desc())\n")
        api_list_list.append(f"{tab}{tab}pass\n")
        api_list_list.append(f"{tab}totalcount = total_{tablenames}.with_entities(func.count({tableclass}.id)).scalar()\n")
        api_list_list.append(f"{tab}page = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page\n")
        api_list_list.append(f"{tab}pagination = total_{tablenames}.paginate(page, per_page = pageSize, error_out = False)\n")
        api_list_list.append(f"{tab}{tablenames} = pagination.items\n")
        api_list_list.append(f"""\n{tab}return jsonify({{
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    "pageSize" : pageSize,
                    "current" : page,
                    "pagecount": pagination.pages,
                    'data':[{tablename}.to_json() for {tablename} in {tablenames}]
                    }})""")
        api_list_list.append(f"\n")
        api_list_list.append(f"\n")




        if table.get('detail_sons') is not None:
            api_list_list.append(f"@api.route('/{tablename}/list/detail', methods=['GET'])\n")
            api_list_list.append(f"def list_detail_{tablename}():\n")
            api_list_list.append(f"{tab}print(request.args)\n")
            api_list_list.append(f"{tab}sorter = request.args.get('sorter')\n")
            api_list_list.append(f"{tab}page = int(request.args.get('current', 1))\n")
            api_list_list.append(f"{tab}pageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))\n")
            api_list_list.append(f"{tab}pageSize = 20 if pageSize < 10 else pageSize\n")

            if table.get('userfilter'):
                api_list_list.append(f"\n{tab}if is_admin():\n")
                if table.get('appfilter'):
                    api_list_list.append(f"{tab}{tab}total_{tablenames} = {tableclass}.query.filter_by(app_id=g.app.id)\n")
                else:
                    api_list_list.append(f"{tab}{tab}total_{tablenames} = {tableclass}.query\n")
                api_list_list.append(f"{tab}else:\n")
                api_list_list.append(f"{tab}{tab}total_{tablenames} = g.current_user.{tablenames}\n")
            else:
                if table.get('appfilter'):
                    api_list_list.append(f"{tab}total_{tablenames} = {tableclass}.query.filter_by(app_id=g.app.id)\n")
                else:
                    api_list_list.append(f"{tab}total_{tablenames} = {tableclass}.query\n")

            if table.get("many"):
                for many in table.get('many'):
                    manyclass = many.get('name')
                    manyname = many.get('name').lower()
                    api_list_list.append(f"\n{tab}{manyname}_id = request.args.get('{manyname}_id')\n")
                    api_list_list.append(f"{tab}if {manyname}_id is not None:\n")
                    api_list_list.append(f"{tab}{tab}{manyname} = {manyclass}.query.filter_by(id={manyname}_id).first()\n")
                    api_list_list.append(f"{tab}{tab}if {manyname} is None:\n")
                    api_list_list.append(
                        f"""{tab}{tab}{tab}return jsonify({{'success':False,'error_code':-1,'errmsg':f'{manyname}:{{{manyname}_id}}不存在'}})\n""")
                    api_list_list.append(f"{tab}{tab}else:\n")

                    api_list_list.append(f"{tab}{tab}{tab}total_{tablenames} = {manyname}.{tablename}s\n\n")
            for parent in table.get('parents'):
                parentname = parent.get('name')
                parenttablename = parentname.lower()
                if parent.get('post'):
                    index = parent.get('index')
                    argname = f"{parenttablename}_{parent.get('index')}"
                    api_list_list.append(f"\n{tab}{argname} = request.args.get('{argname}')\n")
                    api_list_list.append(f"{tab}if {argname} is not None:\n")
                    api_list_list.append(f"{tab}{tab}{parenttablename} = {parentname}.query.filter_by({index}={argname}).first()\n")
                    api_list_list.append(f"{tab}{tab}if {parenttablename} is None:\n")
                    api_list_list.append(f"""{tab}{tab}{tab}return jsonify({{'success':False,'error_code':-1,'errmsg':'{argname}不存在'}})\n""")
                    api_list_list.append(
                        f"{tab}{tab}else:\n{tab}{tab}{tab}total_{tablenames} = total_{tablenames}.filter_by({parenttablename}_id={parenttablename}.id)\n")

            for column in table.get('args'):
                filter = column.get('filter')
                # print(tablename,filter,column,table)
                if filter:
                    argname = column.get('name')
                    api_list_list.append(f"{tab}{argname} = request.args.get('{argname}')\n")
                    api_list_list.append(f"{tab}if {argname} is not None:\n")
                    if filter == "like":
                        api_list_list.append(
                            f"{tab}{tab}total_{tablenames} = total_{tablenames}.filter({tableclass}.{argname}.ilike(f'%{{{argname}}}%'))\n\n")
                    elif filter == "precise":
                        api_list_list.append(f"{tab}{tab}total_{tablenames} = total_{tablenames}.filter_by({argname}={argname})\n\n")
            api_list_list.append(f"{tab}if sorter:\n")
            api_list_list.append(f"{tab}{tab}sorter = json.loads(sorter)\n")

            for column in table.get('args'):
                if column.get("sorter"):
                    argname = column.get('name')
                    api_list_list.append(f"{tab}{tab}if sorter.get('{argname}') == 'ascend':\n")
                    api_list_list.append(f"{tab}{tab}{tab}total_{tablenames} = total_{tablenames}.order_by({tableclass}.{argname}.asc())\n")
                    api_list_list.append(f"{tab}{tab}elif sorter.get('{argname}') == 'descend':\n")
                    api_list_list.append(f"{tab}{tab}{tab}total_{tablenames} = total_{tablenames}.order_by({tableclass}.{argname}.desc())\n")
            api_list_list.append(f"{tab}{tab}pass\n")
            api_list_list.append(f"{tab}totalcount = total_{tablenames}.with_entities(func.count({tableclass}.id)).scalar()\n")
            api_list_list.append(f"{tab}page = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page\n")
            api_list_list.append(f"{tab}pagination = total_{tablenames}.paginate(page, per_page = pageSize, error_out = False)\n")
            api_list_list.append(f"{tab}{tablenames} = pagination.items\n")
            api_list_list.append(f"""\n{tab}return jsonify({{
                        'success':True,
                        'error_code':0,
                        'total':totalcount,
                        "pageSize" : pageSize,
                        "current" : page,
                        "pagecount": pagination.pages,
                        'data':[{tablename}.to_detail() for {tablename} in {tablenames}]
                        }})""")
            api_list_list.append(f"\n")
            api_list_list.append(f"\n")


        # 加入导入包
        target_str_list += import_list

        api_get_list[2:0] = commit_get_list
        target_str_list += api_get_list
        api_post_list[2:0] = commit_post_list
        target_str_list += api_post_list
        api_put_list[2:0] = commit_put_list
        target_str_list += api_put_list
        api_delete_list[2:0] = commit_delete_list
        target_str_list += api_delete_list
        api_list_list[2:0] = commit_list_list
        target_str_list += api_list_list


        for line in target_str_list:
            w.write(line)

        w.close()


# 写入api的init文件
def write_api_init(root,ojson):
    appname = ojson.get('app')
    initdir = os.path.join(root, f'{appname}/src/app/apiv1/__init__.py')
    w = open(initdir, 'w+')
    w.write("from flask import Blueprint\napi = Blueprint('api', __name__)\n")
    w.write("from app.apiv1 import auth")
    # for table in ojson.get('databases'):
    #     if table.get('api'):
    #         w.write(f",{table.get('table')}")

    api_dir = os.path.dirname(initdir)

    for  fname in os.listdir(api_dir):
        if fname.endswith('.py') and fname != '__init__.py' and fname != 'auth.py':
            w.write(f", {fname[:-3]}")
    w.close()
