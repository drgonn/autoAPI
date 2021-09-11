import os
from tools import  name_convert





class Mapping(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value


    # def format_str(self, fm, tab_num):
    #     t = "    "
    #     s = ""
    #     if fm == "list_commit":
    #         if self.list:
    #             s = f"{t*tab_num}{self.name}_id (int optional): {self.mean}主键ID\n"
    #     elif fm == "return_commit":
    #         s = f"{t*tab_num}{self.name} ({self.type} optional): {self.mean}\n"        
