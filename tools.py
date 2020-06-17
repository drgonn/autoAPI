import os

class Tdb():
    def __init__(self,t):
        if t == "int":
            self.db = "Integer"
        elif t == "float":
            self.db = "Float"
        elif t == "str":
            self.db = "String"
        elif t == "time":
            self.db = "DateTime"
        elif t == "date":
            self.db = "Date"
        elif t == "bool":
            self.db = "Boolean"
        elif t == "text":
            self.db = "Text"
        else:
            self.db = None

class Tdbgo():
    def __init__(self,t):
        if t == "int":
            self.db = "int"
        elif t == "float":
            self.db = 'float32 `gorm:"type:float"`'
        elif t == "str":
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


def mkdir(path):
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print (path+' 创建成功')
        return True
    else:
        print (path+' 目录已存在')
        return False

def make_tree(root,app,blues):             #建立所有文件夹
    path = os.path.join(root,app)
    mkdir(path)
    mkdir(os.path.join(path,'doc'))
    mkdir(os.path.join(path,'jMeter'))
    mkdir(os.path.join(path,'src'))
    mkdir(os.path.join(path,'src/app'))
    mkdir(os.path.join(path,'src/app/admin'))
    mkdir(os.path.join(path,'src/app'))
    mkdir(os.path.join(path,'go'))
    mkdir(os.path.join(path,'go/src'))
    mkdir(os.path.join(path,'go/bin'))
    mkdir(os.path.join(path,'go/pkg'))
    app_path = os.path.join(path,'src/app')
    for b in blues:
        mkdir(os.path.join(app_path,b.get('name')))








