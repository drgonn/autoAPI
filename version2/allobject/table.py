import os




class MysqlTable(object):
    def __init__(self,name,zh_name):
        self.name=name
        self.zh_name=zh_name

        self.names = name+ "s"
        self.columns = []


    def reload(self):
        for column in self.columns:
            column.reload()