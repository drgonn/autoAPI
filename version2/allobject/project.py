import os




class Project(object):
    def __init__(self,name,zh,app_root_dir):
        self.name=name
        self.zh=zh
        self.app_root_dir=app_root_dir

        self.doc_dir = os.path.join(app_root_dir, "doc")

        self.apis = []   # 对象的所有访问接口



    def reload(self):
        for table in self.tables:
            table.reload()