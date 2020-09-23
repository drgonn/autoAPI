import os
from tools import Tdb


#建立models
def make_models(appdir,app):
    modeldir = os.path.join(appdir,'models.py')
    w = open(modeldir,'w+')
    w.write(packages)
    for table in app.get('databases'):
        tableclass = table.get('table')
        tablename  = table.get('table').lower()
        tablenames = tablename + 's'
        if table.get("many"):
            for many in table.get('many'):
                if many.get('w_model'):
                    manyclass = many.get('name')
                    manyname = many.get('name').lower()
                    w.write(f"\n{tableclass}{manyclass} = db.Table('{tablename}{manyname}s',\n")
                    w.write(f"\tdb.Column('{tablename}_id',db.Integer,db.ForeignKey('{tablename}s.id')),\n")
                    w.write(f"\tdb.Column('{manyname}_id',db.Integer,db.ForeignKey('{manyname}s.id')))\n")

        w.write(f"\nclass {tableclass}(db.Model):\n")
        w.write(f"\t__tablename__='{tablenames}'\n")
        w.write(f"\tid = db.Column(db.Integer, primary_key=True)\n")
        for column in table.get('args'):
            name = column.get('name')
            tp = column.get('type')
            dbtype = Tdb(tp).db
            length = column.get('length')
            w.write(f"\t{name} = db.Column(db.{dbtype}")
            if length is not None and length != '' and tp == 'str':
                w.write(f"({length})")
            if column.get('args'):
                for arg in column.get('args'):
                    name = arg.get('name')
                    value = arg.get('value')
                    w.write(f", {name}={value}")
            w.write(f")\n")
        for parent in table.get('parents'):
            parentname = parent.get('name')
            parenttablenames = parentname.lower() 
            w.write(f"\t{parenttablenames}_id = db.Column(db.Integer, db.ForeignKey('{parenttablenames}s.id'))\n")
            w.write(f"\t{parenttablenames} = db.relationship('{parentname}', backref=db.backref('{tablenames}', lazy='dynamic'))\n")
        if table.get("many"):
            for many in table.get('many'):
                if many.get('w_model'):
                    manyclass = many.get('name')
                    manyname = many.get('name').lower()
                    w.write(f"\n\t{manyname}s = db.relationship('{manyclass}',\n")
                    w.write(f"\t\tsecondary = {tableclass}{manyclass},\n")
                    w.write(f"\t\tbackref = db.backref('{tablenames}',lazy='dynamic'),\n")
                    w.write(f"\t\tlazy = 'dynamic')\n")
        w.write(f"\t\n")

        w.write(f"\tdef to_json(self):\n")
        w.write(f"\t\treturn{{\n")
        w.write(f"\t\t\t'id':self.id,\n")
        for column in table.get('args'):
            name = column.get('name')
            if column.get('type') == 'time':
                w.write(f"\t\t\t'{name}': utc_switch(self.{name}),\n")
            elif column.get('file'):
                w.write(f"""\t\t\t'{name}': f"statics/file/{{self.id}}/"+self.{name},\n""")
            else:
                w.write(f"\t\t\t'{name}': self.{name},\n")
        for parent in table.get('parents'):           # 显示父表中的值
            parentname = parent.get('name')
            show = parent.get("show")
            if show is not None:
                for sho in show:
                    s_name = sho['name']
                    w.write(f"\t\t\t'{parentname.lower()}_{s_name}' : self.{parentname.lower()}.{s_name},\n")
        w.write(f"\t\t}}\n")
        if table.get('detail_sons') is not None:
            w.write(f"\tdef to_detail(self):\n")
            w.write(f"\t\treturn{{\n")
            w.write(f"\t\t\t'id':self.id,\n")
            for column in table.get('args'):
                name = column.get('name')
                if column.get('type') == 'time':
                    w.write(f"\t\t\t'{name}':utc_switch(self.{name}),\n")
                else:
                    w.write(f"\t\t\t'{name}':self.{name},\n")

            for son in table.get('detail_sons'):
                son = son.lower()
                w.write(f"\t\t\t'{son}s':[{son}.to_detail() for {son} in self.{son}s],\n")

            w.write(f"\t\t}}\n")

        if table.get('repr'):
            w.write(f"\n\tdef __repr__(self):\n\t\treturn '<{tableclass} %r>' % self.{table.get('repr')}\n")




    w.close()



packages = """from datetime import datetime  #记录时间
from app import db
from app.tools import utc_switch,generate_token,certify_token,get_permission
from app.standard import Permission
from datetime import datetime  
"""