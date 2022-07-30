import os
import re
import sys
import getopt
import json

from tools import make_tree

from wfile.goapi import write_goapis, write_goapi_init
from wfile.gomodel import make_gomodels

from wfile.postman import write_postman
from wfile.yapi import write_yapi
from wfile.structure import write_deploy, write_model_doc_plant
from wfile.xmind import write_xmind
from wtest import write_test
from wfile.doc import write_docs as w_docs
from wfile.sql import sql_start


from wclass.wclass import Project


# ojson = order.temp_json
"""将要生成的代码模块化，可以选择生成代码模块"""
module_dir = {
    # 'flask': w_flask,
    'doc': w_docs,
    'postman': write_postman,
    'yapi': write_yapi,
    # 'ant': w_front,  #编写前端的接口，暂时注释

}
default_modules = ['flask', 'go', 'postman', 'doc', 'ant', 'yapi']



basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
f = re.match("/mnt/c/Users/(\w*)/", basedir)
# user = f.group(1)
# run(bri,path=f"/mnt/c/Users/{user}/Documents/mynut")


def run(ojson, path=False, modules=default_modules):
    """
    :param ojson:
    :param path: 要更新的文件夹位置，也就是app：stock或bridge的上级目录，不填默认False时，代表的既是内部的work文件夹
    :param modules:  要更新的模块
    :return:
    """
    if not path:
        root = os.path.abspath(os.path.dirname(__file__))
        new_root = os.path.join(root, 'projects')
        root = os.path.join(root, 'work')
    else:
        root = path
    app = ojson.get('app')
    blues = ojson.get('blues')

    print("xxxxxxxxxxx")
    make_tree(new_root, app, blues)  # 建立文件夹



# try:
#     sql_start(ojson)
# except:
#     print("沒有安裝pysql，不自动创建数据库，想要创建数据库请填入正确数据库信息并安装pysql")




def main(argv):
    """提取arg参数"""
    project = ""
    module = ""
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
    print('project为：', project)
    print('module为：', module)
    print('target_dir为：', target_dir)
    print('源数据转化类型为：', data_type)


    root = os.path.join(os.path.abspath(os.path.dirname(__file__)), "projects")
    make_tree(root, project)  # 建立文件夹
    # project为app名nauth，data_type为数据转换类型
    p = Project(project, data_type)
    p.run()

    # path = False if target_dir == '' else target_dir
    # args = args or default_modules
    # with open(f"project_json/{project}.json", encoding='utf-8') as ff:
    #     project_json = json.load(ff)

    # if project_json is None:
    #     print('Error: project json 不存在')
    # else:
    #     run(project_json, path, args)


if __name__ == "__main__":
    # sys.argv[1:]为要处理的参数列表，sys.argv[0]为脚本名，所以用sys.argv[1:]过滤掉脚本名。
    main(sys.argv[1:])
