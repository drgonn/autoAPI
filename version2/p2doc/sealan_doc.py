"""使用p对象生成思连的文档 markdown格式"""
import os
from xml.dom.minidom import Element


def align_table(table):
    """将二维table中的数据调到一样长度，好让数据生成表格时候一样长"""
    maxMap = {}
    for r in table:
        for i, element in enumerate(r):
            if not maxMap.get(i):
                maxMap[i] = len(element)
            elif len(element) > maxMap[i]:
                maxMap[i] = len(element)

    for r in table:
        for i, element in enumerate(r):
            spaces = maxMap[i] - len(element) 
            if spaces > 0:
                r[i] += " "*spaces






def make_table(md, table_list):
    """
    生成一张表格,还必须是格式对齐的
    table_list: 表结构二维数组,如[[1,2],[3,4]]
    merge_case: 需要合并的单元格
    """
    align_table(table_list)
    columns = len(table_list[0])
    md.write("| "+" | ".join(table_list[0])+" |\n")
    md.write("|----"*columns + "----|\n")
    for r in table_list[1:]:
        md.write("| "+" | ".join(r)+" |\n")
    md.write("\n")


def make_title(doc, title, level):
    doc.write("#"*level + " " + title+"\n")




def to_md(p):
    """将对象生成md文档
    p: 有关项目的整个对象
    """

    md_dir = os.path.join(p.doc_dir, f"sealan_doc.md")
    md = open(md_dir, "w")
    md.write("")
    print("生成md文档中...")
    # 设置字体
    make_title(md, f'{p.zh}功能设计说明书', 1)

    make_title(md, '修订记录', 1)
    # make_table(md, [
    #     ["日期", "版本", "概述", "修订人", "审核人"],
    #     [p.now_date, "0.1.0", "初稿设计", "谌榕", ""],
    #     ["", "", "", "", ""],
    # ])

    # md.write("#"*1 + " " + "一、功能说明" + "\n")
    # md.write("#"*1 + " " + "二、数据库设计\n")
    # md.write("mysql数据库设计说明\n\n")
    # table_list = [
    #     ["表名", "字段", "类型", "说明"],
    # ]
    # for t in p.tables:
    #     table_list.append([t.names, "", "", t.zh_name+t.about])
    #     for c in t.columns:
    #         table_list.append(["", c.name, c.sql_type, c.zh])
    # make_table(md, table_list)

    md.write("#"*1 + " " + "三、HTTP接口说明\n")
    for i, api in enumerate(p.apis):
        md.write("#"*2 + " " + f"3.{i+1} {api.zh_name}接口\n\n")
        md.write(f"接口地址：{api.path}\n\n")
        md.write("YAPI测试地址：\n\n")
        md.write(f"请求方式：{api.METHOD}\n\n")

        if api.path_args:
            md.write("**路径参数说明**\n\n")
            table_list = [
                ["参数", "类型", "必须", "含义", "说明"],
            ]
            for arg in api.path_args:
                table_list.append([arg.name, arg.type.doc_type, arg.zh_required, arg.zh_name, arg.about])
            make_table(md, table_list)


        if api.input_args:
            md.write("**请求参数说明**\n\n")
            table_list = [
                ["参数", "类型", "必须", "含义", "说明"],
            ]
            for arg in api.input_args:
                table_list.append([arg.name, arg.type.doc_type, arg.zh_required, arg.zh_name, arg.about])
            make_table(md, table_list)


        md.write("**返回参数说明**\n\n")
        table_list = [
                ["参数", "类型", "必须", "含义", "说明"],
        ]
        for arg in api.out_args:
            table_list.append([arg.name, arg.type.doc_type, arg.zh_required, arg.zh_name, arg.about])
        make_table(md, table_list)


    md.write("#"*1 + " " + "四、影响分析\n\n")
    md.write("#"*1 + " " + "五、计划\n\n")
    md.write("#"*1 + " " + "六、质量目标\n\n")
    md.write("#"*1 + " " + "七、测试建议\n\n")
    md.write("#"*1 + " " + "八、其他信息\n\n")
    md.write("#"*1 + " " + "九、参考资料\n\n")

    print("生成markdown成功", md_dir)
    md.close()
    return md_dir
