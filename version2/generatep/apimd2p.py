"""使用sealan_doc.md文件对p对象加载更多信息"""
import os
import json
import re


from allobject.project import Project
from allobject.api import ResetApiInterface
from allobject.arg import ApiArg, data_arg, status_out_args, list_arg, page_query_args, page_return_args
from allobject.data_type import DataType
from allobject.column import Column
from allobject.table import MysqlTable


# from allobject. import 

              

def apimdload(p):
    """使用文档生成对象p
    """
    
    sealan_doc_dir = os.path.join(p.app_root_dir, "doc", f"sealan_doc.md")
    print("mysql数据结构markdown位置是：", sealan_doc_dir)
    # 查询该目录下的json文件
    if not os.path.exists(sealan_doc_dir):
        print(sealan_doc_dir, "sealan_doc.md文件不存在")
        os.abort()

    # 将源json文件读取出来为一个对象 project_json
    file_lines = []
    with open(sealan_doc_dir, encoding='utf-8') as ff:
        for line in ff.readlines():
            file_lines.append(line)


    apiInterfaces = []    # 所有接口对象列表
    for line in file_lines:
        if line[:3] == "## ":
            interface_name = line.split(" ")[2]
            

        pass
        

     


    p.apis += apiInterfaces

    return p



