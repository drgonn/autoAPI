import os

from allobject.data_type import DataType



class Column(object):
    def __init__(self,name, zh_name, type):
        self.name=name 
        self.zh_name=zh_name 
        self.type=DataType(type)

        self.about = ""
        self.default = ""
        self.extra = ""
        self.can_empty = True
        self.key = "PRI" if self.name=="id" else "" 

    def reload(self):
        self.create_can_empty = "NULL" if self.can_empty else "NOT NULL"
        pass