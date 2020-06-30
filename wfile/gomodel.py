import os
from tools import Tdbgo,Tdbjson,Tdb


#建立models
def make_gomodels(appdir,app):
    modeldir = os.path.join(appdir,'models.go')
    w = open(modeldir,'w+')
    # w.write(packages)
    w.write(f"package main\n")
    w.write('import (\n\t"github.com/jinzhu/gorm"\n\t"time"\n)\n')
    w.write('var db *gorm.DB\n')

    w.write('func init() {\n')
    w.write('\tvar err error\n')
    w.write('\tdb, err = gorm.Open("mysql", "root:781117@/bridge?charset=utf8&parseTime=True&loc=Local")\n')
    w.write('\tif err != nil {\n')
    w.write('\t\tpanic("failed to conect database")\n')
    w.write('\t}\n')
    for table in app.get('databases'):
        tableclass = table.get('table')
        tablename  = table.get('table').lower()
        w.write(f'\tdb.AutoMigrate(&{tableclass}{{}})\n')
    w.write('}\n')


    for table in app.get('databases'):
        tableclass = table.get('table')
        tablename  = table.get('table').lower()

        sons = []
        for stable in app.get('databases'):
            for parent in stable.get('parents'):
                parentname = parent.get('name')
                if parentname == tableclass:
                    sons.append(stable.get('table'))

        # if table.get("many"):
        #     for many in table.get('many'):
        #         manyclass = many.get('name')
        #         manyname = many.get('name').lower()
        #         w.write(f"\n{tableclass}{manyclass} = db.Table('{tablename}{manyname}s',\n")
        #         w.write(f"\tdb.Column('{tablename}_id',db.Integer,db.ForeignKey('{tablename}s.id')),\n")
        #         w.write(f"\tdb.Column('{manyname}_id',db.Integer,db.ForeignKey('{manyname}s.id')))\n")

        w.write(f"type {tableclass} struct {{\n")
        w.write(f"\tID uint\n")
        for column in table.get('args'):
            name = column.get('name')
            tp = column.get('type')
            dbtype = Tdbgo(tp).db
            length = column.get('length')
            w.write(f"\t{name.title()} {dbtype}")
            if length is not None and length != '':
                w.write(f' `gorm:"size:{length}"`')
            # if column.get('args'):
            #     for arg in column.get('args'):
            #         name = arg.get('name')
            #         value = arg.get('value')
            #         w.write(f", {name}={value}")
            w.write(f"\n")
        for parent in table.get('parents'):
            parentname = parent.get('name')
            parenttablenames = parentname.lower()
            w.write(f"\t{parentname}ID uint\n")

        for son in sons:
            w.write(f'\t{son}s []{son} `gorm:"foreignkey:{tableclass}ID"`\n')


        # if table.get("many"):
        #     for many in table.get('many'):
        #         manyclass = many.get('name')
        #         manyname = many.get('name').lower()
        #         w.write(f"\n\t{manyname}s = db.relationship('{manyclass}',\n")
        #         w.write(f"\t\tsecondary = {tableclass}{manyclass},\n")
        #         w.write(f"\t\tbackref = db.backref('{tablenames}',lazy='dynamic'),\n")
        #         w.write(f"\t\tlazy = 'dynamic')\n")
        # w.write(f"\t\n")

        w.write('}\n')

        w.write(f"type json{tableclass} struct {{\n")
        w.write(f'\tID uint  `json:"id"`\n')
        for column in table.get('args'):
            name = column.get('name')
            tp = column.get('type')
            dbtype = Tdbjson(tp).db
            length = column.get('length')
            w.write(f'\t{name.title()} {dbtype} `json:"{name}"`')
            w.write(f"\n")
        for parent in table.get('parents'):
            parentname = parent.get('name')
            parenttablenames = parentname.lower()
            w.write(f'\t{parentname}ID uint `json:"{parentname.lower()}_id"`\n')

        w.write('}\n')
        # for parent in table.get('parents'):
        #     parentname = parent.get('name')
        #     w.write(f"db.Model(&{tablenames}).Related(&{parentname.lower()}s)\n")

    w.write('\n')
    w.close()



packages = """from datetime import datetime  #记录时间
from app import db
from app.tools import utc_switch,generate_token,certify_token,get_permission
from app.standard import Permission
from datetime import datetime  
"""