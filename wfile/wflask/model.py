import os
from tools import Tdb
from tools import make_tree,name_convert


def write_models(root, ojson):
    """生成数据库模型文件

    root: string，项目当中src/app的目录位置，绝对地址
    ojson: json,  项目的原始json数据
    """
    print(root)
    tab = "    "
    app = ojson.get('app')
    appdir = os.path.join(root, f'{app}/src')

    import_list = []  
    import_list.append('from flask import request, jsonify, current_app, g\n')
    import_list.append('from app import db\n')
    import_list.append('from datetime import datetime,date\n')
    import_list.append('from app.tools import utc_switch\n')
    import_list.append('\n\n')


    for table in ojson.get('databases'):
        target_str_list=[]
        tableclass = table.get('table')
        tablename = name_convert(tableclass)
        tablenames = tablename + 's'
        model_file = table.get("table")
        zh = table.get('zh')
        about = table.get('about') or ""
        model_dir = os.path.join(appdir,f'models/{model_file}.py')

        # 加入导入包
        target_str_list += import_list


        # 加入多对多数据库
        if table.get("many"):
            many2many_list = []
            for many in table.get('many'):
                if many.get('w_model'):
                    manyclass = many.get('name')
                    manyname = many.get('name').lower()
                    many2many_list.append(
                        f"{tableclass}{manyclass} = db.Table('{tablename}{manyname}s',\n")
                    many2many_list.append(
                        f"{tab}db.Column('{tablename}_id',db.Integer,db.ForeignKey('{tablename}s.id')),\n")
                    many2many_list.append(
                        f"{tab}db.Column('{manyname}_id',db.Integer,db.ForeignKey('{manyname}s.id'))\n)\n\n")
            target_str_list += many2many_list

        # 加入数据库class
        class_list = []   
        class_commit_list = []   #注释列表
        class_tojson_commit_list = []   #tojson方法注释列表

        class_commit_list.append(f'{tab}"""{zh}数据库模型\n\n')
        class_commit_list.append(f'{tab}{about}\n\n')
        class_commit_list.append(f'{tab}Attributes:\n')
        class_commit_list.append(f'{tab}"""\n')
        class_list.append(f"class {tableclass}(db.Model):\n")
        class_list.append(f"{tab}__tablename__ = '{tablenames}'\n")
        class_list.append(f"{tab}id = db.Column(db.Integer, primary_key=True)\n")
        class_commit_list.insert(-1, f"{tab*2}id: 序号， 主键\n")
        class_tojson_commit_list.append(f'{tab*2}"""返回请求json数据\n\n')
        class_tojson_commit_list.append(f'{tab*2}Returns:\n')
        class_tojson_commit_list.append(f'{tab*3}id: 序号\n')
        class_tojson_commit_list.append(f'{tab*2}"""\n')
        
        try:
            for column in table.get('args'):
                name = column.get('name')
                mean = column.get('mean')
                tp = column.get('type')
                dbtype = Tdb(tp).db
                length = column.get('length')
                if name == "id":
                    continue
                class_list.append(f"{tab}{name} = db.Column(db.{dbtype}")
                class_commit_list.insert(-1, f"{tab*2}{name}: {mean}\n")
                class_tojson_commit_list.insert(-1,f'{tab*3}{name}: {mean}\n')
                if length is not None and length != '' and tp == 'str':
                    class_list.append(f"({length})")
                if column.get('args'):
                    for arg in column.get('args'):
                        name = arg.get('name')
                        value = arg.get('value')
                        class_list.append(f", {name}={value}")
                class_list.append(f")\n")
        except TypeError:
            print(table.get("name"), "的args是空的。", table)
        for parent in table.get('parents'):
            parentname = parent.get('name')
            parenttablenames = parentname.lower()
            class_list.append(
                f"{tab}{parenttablenames}_id = db.Column(db.Integer, db.ForeignKey('{parenttablenames}s.id'))\n")
            class_list.append(
                f"{tab}{parenttablenames} = db.relationship('{parentname}', backref=db.backref('{tablenames}', lazy='dynamic'))\n")
            class_commit_list.insert(-1, f"{tab*2}{parenttablenames}_id: 父表{parentname}的ID\n")
            class_commit_list.insert(-1, f"{tab*2}{parenttablenames}: 父表{parentname}对象\n")
            class_tojson_commit_list.insert(-1,f'{tab*3}{parenttablenames}_id: 父表{parentname}的ID\n')
        if table.get("many"):
            for many in table.get('many'):
                if many.get('w_model'):
                    manyclass = many.get('name')
                    manyname = many.get('name').lower()
                    class_list.append(
                        f"\n{tab}{manyname}s = db.relationship('{manyclass}',\n")
                    class_list.append(f"{tab}{tab}secondary = {tableclass}{manyclass},\n")
                    class_list.append(
                        f"{tab}{tab}backref = db.backref('{tablenames}',lazy='dynamic'),\n")
                    class_list.append(f"{tab}{tab}lazy = 'dynamic')\n")
        class_list.append(f"\n")

        class_list.append(f"{tab}def to_json(self):\n")
        class_list.extend(class_tojson_commit_list)
        for column in table.get('args'):
            if column.get('file'):
                class_list.append(
                    f"""{tab}{tab}static_host = current_app.config['STATIC_HOST']\n""")
                break
        class_list.append(f"{tab}{tab}return{{\n")
        class_list.append(f"{tab}{tab}{tab}'id':self.id,\n")
        for column in table.get('args'):
            name = column.get('name')
            if name == "id":
                continue
            if column.get('type') == 'time':
                class_list.append(f"{tab}{tab}{tab}'{name}': utc_switch(self.{name}),\n")
            elif column.get('type') == 'date':
                class_list.append(
                    f"{tab}{tab}{tab}'{name}': self.{name}.strftime('%Y-%m-%d') if self.{name} else None,\n")
            elif column.get('file'):
                class_list.append(
                    f"""{tab}{tab}{tab}'{name}_url': f"{{static_host}}/{tablename}{name}/{{self.id}}/"+self.{name} if self.{name} else None,\n""")
                class_list.append(f"""{tab}{tab}{tab}'{name}': self.{name},\n""")
            else:
                class_list.append(f"{tab}{tab}{tab}'{name}': self.{name},\n")
        for parent in table.get('parents'):           # 显示父表中的值
            parentname = parent.get('name')
            show = parent.get("show")
            if show is not None:
                for sho in show:
                    s_name = sho['name']
                    class_list.append(
                        f"{tab}{tab}{tab}'{parentname.lower()}_{s_name}' : self.{parentname.lower()}.{s_name} if self.{parentname.lower()} else None,\n")
        class_list.append(f"{tab}{tab}}}\n")
        if table.get('detail_sons') is not None:
            class_list.append(f"\n{tab}def to_detail(self):\n")
            class_list.append(f"{tab}{tab}return{{\n")
            class_list.append(f"{tab}{tab}{tab}'id':self.id,\n")
            for column in table.get('args'):
                name = column.get('name')
                if column.get('type') == 'time':
                    class_list.append(f"{tab}{tab}{tab}'{name}':utc_switch(self.{name}),\n")
                else:
                    class_list.append(f"{tab}{tab}{tab}'{name}':self.{name},\n")
            for parent in table.get('parents'):  # 显示父表中的值
                parentname = parent.get('name')
                show = parent.get("show")
                if show is not None:
                    for sho in show:
                        s_name = sho['name']
                        class_list.append(
                            f"{tab}{tab}{tab}'{parentname.lower()}_{s_name}' : self.{parentname.lower()}.{s_name},\n")

            for son in table.get('detail_sons'):
                son = son.lower()
                class_list.append(
                    f"{tab}{tab}{tab}'{son}s':[{son}.to_detail() for {son} in self.{son}s],\n")

            class_list.append(f"{tab}{tab}}}\n")

        if table.get('repr'):
            class_list.append(
                f"\n{tab}def __repr__(self):\n{tab}{tab}return '<{tableclass} %r>' % self.{table.get('repr')}\n")

        class_list[1:0] = class_commit_list

        target_str_list += class_list

        w = open(model_dir, 'w+')
        for line in target_str_list:
            w.write(line)
        w.close()


