import os
import re


class Tdb():
    def __init__(self,t):
        if t == "int":
            self.db = "Integer"
            self.empty = 0
            self.ts_interface = "number"
            self.protable_valuetype = "digit"
        elif t == "bigint":
            self.db = "BIGINT"
            self.empty = 0
            self.ts_interface = "number"
            self.protable_valuetype = "digit"
        elif t == "float":
            self.db = "Float"
            self.empty = 0
            self.ts_interface = "number"
            self.protable_valuetype = "digit"
        elif t == "string":
            self.db = "String"
            self.empty = '""'
            self.ts_interface = "string"
            self.protable_valuetype = "text"
        elif t == "time":
            self.db = "DateTime"
            self.empty = '""'
            self.ts_interface = "Date"
            self.protable_valuetype = "dateTime"
        elif t == "date":
            self.db = "Date"
            self.empty = '""'
            self.ts_interface = "Date"
            self.protable_valuetype = "date"
        elif t == "bool":
            self.db = "Boolean"
            self.empty = 'false'
            self.ts_interface = "boolean"
            self.protable_valuetype = "text"
        elif t == "text":
            self.db = "Text"
            self.empty = '""'
            self.ts_interface = "string"
            self.protable_valuetype = "text"
        else:
            self.db = t
            self.empty = '""'
            self.protable_valuetype = t
            self.ts_interface = t

class Tdbgo():
    def __init__(self,t):
        if t == "int":
            self.db = "int"
        elif t == "float":
            self.db = 'float32 `gorm:"type:float"`'
        elif t == "string":
            self.db = "string"
        elif t == "time":
            self.db = "time.Time"
        elif t == "date":
            self.db = "Date"
        elif t == "bool":
            self.db = "bool"
        elif t == "text":
            self.db = f'string `gorm:"type:text"`'
        else:
            self.db = None

class Tdbjson():
    def __init__(self,t):
        if t == "int":
            self.db = "int"
        elif t == "float":
            self.db = 'float32'
        elif t == "string":
            self.db = "string"
        elif t == "time":
            self.db = "time.Time"
        elif t == "date":
            self.db = "Date"
        elif t == "bool":
            self.db = "bool"
        elif t == "text":
            self.db = f'string'
        else:
            self.db = None

def mkdir(path):
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False






def make_tree(root,app,blues):             #建立所有文件夹
    path = os.path.join(root,app)
    mkdir(path)
    mkdir(os.path.join(path,'doc'))
    mkdir(os.path.join(path,'test'))
    mkdir(os.path.join(path,'test/postman_json'))
    mkdir(os.path.join(path,'test/yapi'))
    mkdir(os.path.join(path,'src'))
    mkdir(os.path.join(path,'src/app'))
    mkdir(os.path.join(path,'src/models'))
    mkdir(os.path.join(path,'src/statics'))
    mkdir(os.path.join(path,'src/app/admin'))
    mkdir(os.path.join(path,'src/app/tools'))
    mkdir(os.path.join(path,'src/app'))
    mkdir(os.path.join(path,'go'))
    mkdir(os.path.join(path,'go/src'))
    mkdir(os.path.join(path,'go/bin'))
    mkdir(os.path.join(path,'go/pkg'))
    os.makedirs(os.path.join(path,'src/app/tasks'), exist_ok=True)
    app_path = os.path.join(path,'src/app')

    for b in blues:
        mkdir(os.path.join(app_path,b.get('name')))



def replace_file(file,source,target):
    f = open(file, 'r')
    alllines = f.readlines()
    f.close()
    f = open(file, 'w+')
    for eachline in alllines:
        a = re.sub(source, target, eachline)
        f.writelines(a)
    f.close()


def name_convert(name: str) -> str:
    """驼峰式命名和下划线式命名互转"""
    is_camel_name = True  # 是否为驼峰式命名
    if re.match(r'[a-z][_a-z]+$', name):
        is_camel_name = False
    elif re.match(r'[a-zA-Z0-9]+$', name) is None:
        raise ValueError(f'Value of "name" is invalid: {name}')
    if is_camel_name:  # 驼峰转下划线
        name = re.sub('(.)([A-Z]+)', r'\1_\2', name).lower()
    else:  # 下划线转驼峰
        name = name.title().replace("_","")
    return name


