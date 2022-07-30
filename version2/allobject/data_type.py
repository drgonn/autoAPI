import os
import re




class DataType(object):
    def __init__(self, name):
        self.name = name.lower()
        self.Name = name.title()
        self.NAME = name.upper()
        


        varcharre = re.match("varchar\((\d+)\)",self.name)
        intre = re.match("int\((\d+)\)",self.name)
        if name.lower() in ["int","interger"]:
            self.mysql_type = "int"
            self.MYSQL_TYPE = self.mysql_type.upper()
            self.doc_type = "Integer"
        elif intre:
            length = intre.group(1)
            self.mysql_type = self.name
            self.MYSQL_TYPE = self.mysql_type.upper()
            self.doc_type = "Integer"
        elif name.lower() in ["str", "string", "varchar"]:
            self.mysql_type = "varchar(255)"
            self.MYSQL_TYPE = self.mysql_type.upper()
            self.doc_type = "String"
        elif varcharre:
            length = varcharre.group(1)
            self.mysql_type = self.name
            self.MYSQL_TYPE = self.mysql_type.upper()
            self.doc_type = "String"
        else:
            self.mysql_type = name
            self.MYSQL_TYPE = self.mysql_type.upper()
            self.doc_type = self.Name


        # s = "varchar(1234)"
        # strre = re.match("varchar\((\d+)\)",self.name)
        # if r:
        #     print(r)
        #     print(r.group())
        #     print(r.group(1))