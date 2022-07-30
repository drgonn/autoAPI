"""使用json文件生成总对象p"""
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

              

def mysql_md2project_tables(appName, projects_dir):
    """使用文档生成对象p
    """
    # 读取文档文件
    root_dir = os.path.join(projects_dir, appName)
    print("项目目录是：", root_dir)
    
    sealan_doc_dir = os.path.join(root_dir, "doc", f"mysql.md")
    print("mysql数据结构markdown位置是：", sealan_doc_dir)
    # 查询该目录下的json文件
    if not os.path.exists(sealan_doc_dir):
        print(sealan_doc_dir, "mysql.md文件不存在")
        os.abort()

    # 将源json文件读取出来为一个对象 project_json
    file_lines = []
    with open(sealan_doc_dir, encoding='utf-8') as ff:
        for line in ff.readlines():
            file_lines.append(line)
    tables = []

    table = None
    for line in file_lines:
        if line[:4] == "####":
            tabke_name_data = line.split(" ")
            table = MysqlTable(tabke_name_data[2],tabke_name_data[3].strip())
            md_table_index = 0
            tables.append(table)
        elif table:
            md_table_row = line.split("|")
            if len(md_table_row) >= 10:
                md_table_index += 1
                if md_table_index > 2:
                    # print("表内参数",md_table_row, len(md_table_row))
                    column_name = md_table_row[2].strip(" `")
                    column_zh_name = md_table_row[3].split("，")[0].strip()
                    column_type = md_table_row[4].strip()
                    column = Column(name= column_name, zh_name=column_zh_name, type=column_type)

                    if md_table_row[6].strip().lower() in ["no", "否", "n"]:
                        column.can_empty = False
                    else:
                        column.can_empty = True
                    # print("表内参数",md_table_row[6].strip().lower(),column.name,column.can_empty)

                    
                    table.columns.append(column)

            


    p = Project(
        name= appName,
        zh="未命名",
        app_root_dir=root_dir)
    
    p.tables = tables

    return p



