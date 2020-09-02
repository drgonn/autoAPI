import os
import re
import sys
import getopt

from source_json import pay, app, stock, bridge
from tools import make_tree
from wfile.admin import write_admin
from wfile.api import write_apis, write_api_init
from wfile.auth import write_auth
from wfile.config import write_config
from wfile.doc import write_docs
from wfile.goapi import write_goapis, write_goapi_init
from wfile.gomodel import make_gomodels
from wfile.init import make_init
from wfile.init_manage import write_init
from wfile.model import make_models
from wfile.postman import write_postman
from wfile.structure import write_deploy, write_model_doc_plant
from wfile.xmind import write_xmind
from wtest import write_test

from wfront import w_front


# ojson = order.temp_json

def run(ojson,path=False):
    if not path:
        root = os.path.dirname(__file__)
        root = os.path.join(root,'work')
    else:
        root = path
    # root = "/mnt/c/Users/dron/OneDrive/work/"
    # res = dict_to_object(ojson)
    # print(res.database[0].table)
    app     = ojson.get('app')
    blues   = ojson.get('blues')

    make_tree(root,app,blues)          #建立文件夹
    appdir = os.path.join(root,f'{app}/src/app')
    make_models(appdir,ojson)
    make_init(root,ojson)
    write_apis(root,ojson)

    write_docs(root,ojson)
    write_config(root,ojson)
    write_deploy(root,ojson)
    write_model_doc_plant(root,ojson)
    write_admin(root,ojson)

    write_test(root,ojson)
    # write_patch(root,ojson)
    write_postman(root,ojson)
    write_xmind(root,ojson)
    write_init(root,ojson)
    write_auth(root,ojson)



    godir = os.path.join(root,f'{app}/go/src')
    make_gomodels(godir,ojson)
    write_goapi_init(root,ojson)
    write_goapis(root,ojson)

    w_front(root,ojson)


    #生成文件后做的事情
    write_api_init(root,ojson)

pjson = pay.project_json         #执行支付系统
appjson = app.project_json         #执行应用



bri = bridge.project_json
stock = stock.project_json

basedir = os.path.abspath(os.path.dirname(__file__))
f = re.match("/mnt/c/Users/(\w*)/", basedir)
user = f.group(1)
# run(bri,path=f"/mnt/c/Users/{user}/Documents/mynut")

source_dir = {
    "bridge":bri,
    "stock":stock,
}
module_dir = {}



def main(argv):
    source = ""
    module = ""
    target_dir = ""
    try:
        opts, args = getopt.getopt(argv, "hs:m:d:", ["help", "source=", "module=","target_dir="])
    except getopt.GetoptError:
        print('Error: test_arg.py -s <source> -m <module>')
        print('   or: test_arg.py --source=<source> --module=<module>')
        sys.exit(2)

    # 处理 返回值options是以元组为元素的列表。
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('test_arg.py -s <source> -m <module>')
            print('or: test_arg.py --source=<source> --module=<module>')
            sys.exit()
        elif opt in ("-s", "--source"):
            source = arg
        elif opt in ("-m", "--module"):
            module = arg
        elif opt in ("-d", "--target_dir"):
            print("opt",opts)
            target_dir = arg
    print('source为：', source)
    print('module为：', module)
    print('target_dir为：', target_dir)

    path = False if target_dir == '' else target_dir


    if source == "all":
        pass
    else:
        source_json = source_dir.get(source)
        if source_json is None:
            print('Error: source json 不存在')
        else:
            run(source_dir.get(source),path)


    # 打印 返回值args列表，即其中的元素是那些不含'-'或'--'的参数。
    for i in range(0, len(args)):
        print('参数 %s 为：%s' % (i + 1, args[i]))
        print(args)


if __name__ == "__main__":
    # sys.argv[1:]为要处理的参数列表，sys.argv[0]为脚本名，所以用sys.argv[1:]过滤掉脚本名。
    main(sys.argv[1:])


