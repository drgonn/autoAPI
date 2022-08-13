import os
import sys
import getopt
from .generatep.apimd2p import apimdload

from generatep.json2p import json2project
from generatep.mysqlmd2p import mysql_md2project_tables

from p2doc.sealan_doc import to_md
from p2doc.p2json import to_json_file
from writefile.go_dapr import write_go_dapr


def work(project, root_dir):
    """"处理工作"""
    # 将json文件生成总对象p
    p = json2project(project, root_dir)

    to_md(p)

def md_work(project, root_dir):
    """"处理工作"""
    # 将mysql.md文件生成总对象p
    p = mysql_md2project_tables(project, root_dir)
    # 将sealan_doc.md的文件内容补充到对象p当中
    # 未完成...
    # p = apimdload(p)

    p.reload()

    # 将p对象生成文件sealan2doc.json
    to_json_file(p)

    # 生成go_dapr项目的相关文件
    write_go_dapr(p)




def main(argv):
    """提取arg参数,将命令参数传递给处理函数"""
    project = ""
    module = "json"
    target_dir = ""
    data_type = "json"
    try:
        opts, args = getopt.getopt(
            argv, "hp:m:d:t:", ["help", "project=", "module=", "target_dir=", "data_type="])
    except getopt.GetoptError:
        print('Error: test_arg.py -p <project> -m <module>')
        print('   or: test_arg.py --project=<project> --module=<module>')
        sys.exit(2)

    # 获取外部参数
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('test_arg.py -p <project> -m <module>')
            print('or: test_arg.py --project=<project> --module=<module>')
            sys.exit()
        elif opt in ("-p", "--project"):
            project = arg
        elif opt in ("-m", "--module"):
            module = arg
        elif opt in ("-d", "--target_dir"):
            target_dir = arg
        elif opt in ("-t", "--data_type"):
            data_type = arg
    print('项目project为 -p：', project)
    print('module为 -m：', module)
    print('\n')
    print('自定义项目目录位置是：', target_dir)
    print('源数据转化类型为：', data_type)


    root_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "projects")
    print('项目目录位置是：', root_dir)
    print('\n')

    # 传递命令参数给具体工作
    if module == "mysql":          # 从md文件生成对象
        md_work(project, root_dir)
    # elif module == "mysqlmd2sql":          # 使用mysql.md文件生成sql的文件
    #     md_work(project, root_dir)
    elif module == "json":
        work(project, root_dir)

    else:
        print("没有传递正确的mode，请传递如下参数：")
        print("-m json  生成顺序：app.json -> project -> sealan_doc.md")
        print("-m mysql 生成顺序：mysql.md -> project -> sealan2doc.json")
        print("-m sealan_doc 生成顺序：sealan_doc.md -> project -> sealan2doc.json")
        # print("               api.md -> project -> sealan2doc.json")
        print("")


    # make_tree(root, project)  # 建立文件夹
    # # project为app名nauth，data_type为数据转换类型
    # p = Project(project, data_type)
    # p.run()


if __name__ == "__main__":
    # sys.argv[1:]为要处理的参数列表，sys.argv[0]为脚本名，所以用sys.argv[1:]过滤掉脚本名。
    main(sys.argv[1:])
