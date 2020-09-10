import os




def write_apis(root,ojson):
    app = ojson.get('app')
    appdir = os.path.join(root, f'{app}/src/app')
    for table in ojson.get('databases'):
        if not table.get('api'):
            continue
        tableclass = table.get('table')
        tablenames = table.get('table').lower() + 's'
        tablename = table.get('table').lower()
        apifile = table.get('table')
        zh = table.get('zh')
        apidir = os.path.join(appdir,f'apiv1/{apifile}.py')
        w = open(apidir,'w+')
        im = """from datetime import date,timedelta,datetime
import logging
import math
import json

from flask import request,jsonify,current_app,g
from sqlalchemy import func
from sqlalchemy import not_,or_,and_,extract

from app.apiv1 import api
from app.standard import Permission
from app.decorators import admin_required, permission_required
from app import db
from app.tools import is_admin,get_permission
"""
        w.write(im)
        w.write(f"from app.models import {tableclass}")
        for parent in table.get('parents'):
            parentname = parent.get('name')
            w.write(f",{parentname}")
        if table.get('many'):
            for many in table.get('many'):
                manyclass = many.get('name')
                w.write(f",{manyclass}")
        w.write("\n\n")

        for column in table.get('args'):
            argname = column.get('name')

        w.write(f"@api.route('/{tablename}/<int:id>', methods=['GET'])\n")
        w.write(f"def get_{tablename}(id):\n")
        w.write(f"\t{tablename} = {tableclass}.query.get_or_404(id)\n")
        to_what = 'to_json' #if table.get('nodetail') else 'to_detail'

        w.write(f"""\n\treturn jsonify({{'success':True,
                    'error_code':0,
                    'records':{tablename}.{to_what}(),
                    }})""")
        w.write(f"\n\n")


        w.write(f"@api.route('/{tablename}', methods=['POST'])\n")
        w.write(f"def create_{tablename}():\n")
        w.write(f"\tprint(request.json)\n")
        for column in table.get('args'):
            if column.get('post'):
                argname = column.get('name')
                w.write(f"\t{argname} = request.json.get('{argname}')\n")
            if column.get('postmust'):
                w.write(f"\tif {argname} is None:\n")
                w.write(f"\t\treturn jsonify({{'success': False, 'error_code': -123, 'errmsg': '缺少必填参数：{argname}'}})\n")
        for parent in table.get('parents'):
            parentname = parent.get('name')
            parenttablename = parentname.lower()
            if parent.get('name') == 'User':
                w.write(f"\t{parenttablename} = g.current_user\n ")
            elif parent.get('post'):
                index = parent.get('index')
                argname = f"{parenttablename}{parent.get('index').capitalize()}"
                w.write(f"\n\t{argname} = request.json.get('{argname}')\n")
                if parent.get('post')==2:
                    w.write(f"\t{parenttablename} = {parentname}.query.filter_by({index}={argname}).first()\n ")
                    w.write(f"\n\tif {parenttablename} is None:\n")
                    w.write(f"""\t\treturn jsonify({{'success':False,'error_code':-1,'errmsg':'{argname}不存在'}})""")
                    w.write(f"\t\n")
        w.write(f"\n\t{tablename} = {tableclass}(")
        for column in table.get('args'):
            if column.get('post'):
                argname = column.get('name')
                w.write(f"{argname}={argname},")
        for parent in table.get('parents'):
            parentname = parent.get('name')
            parenttablename = parentname.lower()
            if parent.get('post'):
                w.write(f"{parenttablename}_id={parenttablename}.id,")
        if table.get('appfilter'):
            w.write(f"app_id=g.app.id,")
        w.write(f")\n")

        if table.get("many"):
            for many in table.get('many'):
                manyclass = many.get('name')
                manyname = many.get('name').lower()
                w.write(f"\n\t{manyname}_ids = request.json.get('{manyname}_ids') or []\n")
                w.write(f"\tfor {manyname}_id in {manyname}_ids:\n")
                w.write(f"\t\t{manyname} = {manyclass}.query.filter_by(id={manyname}_id)\n")
                w.write(f"\t\tif {manyname} is None:\n")
                w.write(f"\t\t\treturn jsonify({{'success':False,'error_code':-1,'errmsg':'{manyname}ID不存在'}})\n")
                w.write(f"\t\t{tablename}.{manyname}s.append({manyname})\n")
                w.write(f"\t\n")

        w.write(f"\n\tdb.session.add({tablename})\n")
        w.write(f"\ttry:\n\t\tdb.session.commit()\n\texcept Exception as e:\n\t\tdb.session.rollback()\n")
        w.write(f"\t\tlogging.error(f'添加数据库发生错误,已经回退:{{e}}')\n")
        w.write(f"\t\treturn jsonify({{'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'}})\n")
        w.write(f"""\n\treturn jsonify({{'success':True,
                    'error_code':0,
                    }})""")
        w.write(f"\n\n")



        w.write(f"@api.route('/{tablename}/<int:id>', methods=['PUT'])\n")
        w.write(f"def modify_{tablename}(id):\n")
        w.write(f"\tprint('put json:',request.json)\n")
        w.write(f"\t{tablename} = {tableclass}.query.get_or_404(id)\n")
        for column in table.get('args'):
            if column.get('putneed'):
                argname = column.get('name')
                w.write(f"\t{argname} = request.json.get('{argname}')\n")
        for parent in table.get('parents'):
            parentname = parent.get('name')
            parenttablename = parentname.lower()
            if parent.get('putneed'):
                index = parent.get('index')
                argname = f"{parenttablename}{parent.get('index').capitalize()}"
                w.write(f"\t{argname} = request.json.get('{argname}')\n")
                w.write(f"\t{parenttablename} = {parentname}.query.filter_by({index}={argname}).first()\n")
                w.write(f"\tif {parenttablename} is None:\n")
                w.write(f"""\t\treturn jsonify({{'success':False,'error_code':-1,'errmsg':'{argname}不存在'}})""")
                w.write(f"\t\n")

        for column in table.get('args'):
            if column.get('putneed'):
                argname = column.get('name')
                w.write(f"\t{tablename}.{argname} = {argname} or {tablename}.{argname}\n")
        for parent in table.get('parents'):
            parentname = parent.get('name')
            parenttablename = parentname.lower()
            if parent.get('putneed'):
                w.write(f"\t{tablename}.{parenttablename}_id = {parenttablename}.id\n")
        if table.get("many"):
            for many in table.get('many'):
                if many.get('add_api'):
                    manyclass = many.get('name')
                    manyname = many.get('name').lower()
                    w.write(f"\n\tadd_{manyname}_ids = request.json.get('add_{manyname}_ids')\n")
                    w.write(f"\tif add_{manyname}_ids:\n")
                    w.write(f"\t\toriginal_ids = [{manyname}.id for {manyname} in {tablename}.{manyname}s.all()]\n")
                    w.write(f"\t\tnew_ids = list(set(add_{manyname}_ids).difference(set(original_ids)))\n")
                    w.write(f"\t\tfor {manyname}_id in new_ids:\n")
                    w.write(f"\t\t\t{manyname} = {manyclass}.query.filter_by(id={manyname}_id).first()\n")
                    w.write(f"\t\t\tif {manyname} is None:\n")
                    w.write(f"\t\t\t\treturn jsonify({{'success':False,'error_code':-1,'errmsg':'{manyname}ID不存在'}})\n")
                    w.write(f"\t\t\t{tablename}.{manyname}s.append({manyname})\n")

                    w.write(f"\n\tremove_{manyname}_ids = request.json.get('remove_{manyname}_ids')\n")
                    w.write(f"\tif remove_{manyname}_ids:\n")

                    w.write(f"\t\toriginal_ids = [{manyname}.id for {manyname} in {tablename}.{manyname}s.all()]\n")
                    w.write(f"\t\tremove_ids = list(set(remove_{manyname}_ids).intersection(set(original_ids)))\n")
                    w.write(f"\t\tfor {manyname}_id in remove_ids:\n")
                    w.write(f"\t\t\t{manyname} = {manyclass}.query.filter_by(id={manyname}_id).first()\n")
                    w.write(f"\t\t\t{tablename}.{manyname}s.remove({manyname})\n")
                    w.write(f"\t\t\n")

        w.write(f"\tdb.session.add({tablename})\n")
        w.write(f"\n\ttry:\n\t\tdb.session.commit()\n\texcept Exception as e:\n\t\tdb.session.rollback()\n")
        w.write(f"\t\tlogging.error(f'修改数据库发生错误,已经回退:{{e}}')\n")
        w.write(f"""\treturn jsonify({{'success':True,
                    'error_code':0,
                    }})""")
        w.write(f"\n\n")



        w.write(f"@api.route('/{tablename}', methods=['DELETE'])\n")
        w.write(f"def delete_{tablename}():\n")
        w.write(f"\tprint('delete json:',request.json)\n")
        w.write(f"\tids = request.json.get('ids')\n")
        w.write(f"\tfor id in ids:\n")
        w.write(f"\t\t{tablename} = {tableclass}.query.get(id)\n")
        w.write(f"\t\tif {tablename} is None:\n")
        w.write(f"""\t\t\treturn jsonify({{'success': False, 'error_code': -123, 'errmsg': f'删除错误，id： {{id}} 不存在'}})\n""")


        for table1 in ojson.get('databases'):
            if table1.get('parents'):
                for parent in  table1.get("parents"):
                    if parent.get("name") == tableclass:
                        w.write(f"\tif {tablename}.{table1.get('table').lower()}s.first() is not None:\n")
                        w.write(f"\t\treturn jsonify({{'success':False,'error_code':-1,'errmsg':'{tablename}还拥有{table1.get('table').lower()}，不能删除'}})\n")

        w.write(f"\tdb.session.delete({tablename})\n")
        w.write(f"\n\ttry:\n\t\tdb.session.commit()\n\texcept Exception as e:\n\t\tdb.session.rollback()\n")
        w.write(f"\t\tlogging.error(f'删除数据库发生错误,已经回退:{{e}}')\n")
        w.write(f"""\n\treturn jsonify({{'success':True,
                'error_code':0,
                }})""")
        w.write(f"\n\n")



        w.write(f"@api.route('/{tablename}/list', methods=['GET'])\n")
        w.write(f"def list_{tablename}():\n")
        w.write(f"\tprint(request.args)\n")
        w.write(f"\tsorter = request.args.get('sorter')\n")
        w.write(f"\tpage = int(request.args.get('current', 1))\n")
        w.write(f"\tpageSize = int(request.args.get('pageSize', current_app.config['PER_PAGE']))\n")
        w.write(f"\tpageSize = 20 if pageSize < 10 else pageSize\n")

        if table.get('userfilter'):
            w.write(f"\n\tif is_admin():\n")
            if table.get('appfilter'):
                w.write(f"\t\ttotal_{tablenames} = {tableclass}.query.filter_by(app_id=g.app.id)\n")
            else:
                w.write(f"\t\ttotal_{tablenames} = {tableclass}.query\n")
            w.write(f"\telse:\n")
            w.write(f"\t\ttotal_{tablenames} = g.current_user.{tablenames}\n")
        else:
            if table.get('appfilter'):
                w.write(f"\ttotal_{tablenames} = {tableclass}.query.filter_by(app_id=g.app.id)\n")
            else:
                w.write(f"\ttotal_{tablenames} = {tableclass}.query\n")

        if table.get("many"):
            for many in table.get('many'):
                manyclass = many.get('name')
                manyname = many.get('name').lower()
                w.write(f"\n\t{manyname}_id = request.args.get('{manyname}_id')\n")
                w.write(f"\tif {manyname}_id is not None:\n")
                w.write(f"\t\t{manyname} = {manyclass}.query.filter_by(id={manyname}_id).first()\n")
                w.write(f"\t\tif {manyname} is None:\n")
                w.write(f"""\t\t\treturn jsonify({{'success':False,'error_code':-1,'errmsg':f'{manyname}:{{{manyname}_id}}不存在'}})\n""")
                w.write(f"\t\telse:\n")

                w.write(f"\t\t\ttotal_{tablenames} = {manyname}.{tablename}s\n\n")
        for parent in table.get('parents'):
            parentname = parent.get('name')
            parenttablename = parentname.lower()
            if parent.get('post'):
                index = parent.get('index')
                argname = f"{parenttablename}_{parent.get('index')}"
                w.write(f"\n\t{argname} = request.args.get('{argname}')\n")
                w.write(f"\tif {argname} is not None:\n")
                w.write(f"\t\t{parenttablename} = {parentname}.query.filter_by({index}={argname}).first()\n")
                w.write(f"\t\tif {parenttablename} is None:\n")
                w.write(f"""\t\t\treturn jsonify({{'success':False,'error_code':-1,'errmsg':'{argname}不存在'}})\n""")
                w.write(f"\t\telse:\n\t\t\ttotal_{tablenames} = total_{tablenames}.filter_by({parenttablename}_id={parenttablename}.id)\n")



        for column in table.get('args'):
            filter = column.get('filter')
            # print(tablename,filter,column,table)
            if filter:
                argname = column.get('name')
                w.write(f"\t{argname} = request.args.get('{argname}')\n")
                w.write(f"\tif {argname} is not None:\n")
                if filter == "like":
                    w.write(f"\t\ttotal_{tablenames} = total_{tablenames}.filter({tableclass}.{argname}.ilike(f'%{{{argname}}}%'))\n\n")
                elif filter == "precise":
                    w.write(f"\t\ttotal_{tablenames} = total_{tablenames}.filter_by({argname}={argname})\n\n")
        w.write(f"\tif sorter:\n")
        w.write(f"\t\tsorter = json.loads(sorter)\n")

        for column in table.get('args'):
            if column.get("sorter"):
                argname = column.get('name')
                w.write(f"\t\tif sorter.get('{argname}') == 'ascend':\n")
                w.write(f"\t\t\ttotal_{tablenames} = total_{tablenames}.order_by({tableclass}.{argname}.asc())\n")
                w.write(f"\t\telif sorter.get('{argname}') == 'descend':\n")
                w.write(f"\t\t\ttotal_{tablenames} = total_{tablenames}.order_by({tableclass}.{argname}.desc())\n")
        w.write(f"\t\tpass\n")
        w.write(f"\ttotalcount = total_{tablenames}.with_entities(func.count({tableclass}.id)).scalar()\n")
        w.write(f"\tpage = math.ceil(totalcount/pageSize) if  math.ceil(totalcount/pageSize) < page else page\n")
        w.write(f"\tpagination = total_{tablenames}.paginate(page, per_page = pageSize, error_out = False)\n")
        w.write(f"\t{tablenames} = pagination.items\n")
        w.write(f"""\n\treturn jsonify({{
                    'success':True,
                    'error_code':0,
                    'total':totalcount,
                    "pageSize" : pageSize,
                    "pagecount": pagination.pages,
                    'data':[{tablename}.to_json() for {tablename} in {tablenames}]
                    }})""")
        w.write(f"\n")
        w.write(f"\n")
        w.close()

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
