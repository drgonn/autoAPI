"""生成json文件"""
import os
import pprint
import json


def to_json_file(p):
    md_dir = os.path.join(p.doc_dir, f"sealan2doc.json")
    md = open(md_dir, "w")
    j = {}
    tables = []
    for table in p.tables:
        args = []
        for col in table.columns:
            column_dic = {
            "name": col.name,
            "type": col.type.name,
            "zh": col.zh_name,
            "about": col.about,
            "post": 0,
            "put": 0,
            "list": 0,
            }
            args.append(column_dic)
       
        table_dic = {
            "name": table.name,
            "zh": table.zh_name,
            "args":args
        }
            

        tables.append(table_dic)

    j["databases"] = tables

    with open(md_dir, "w") as file:
        json.dump(j, file, indent=2, ensure_ascii=False)

