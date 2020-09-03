import os
import re
import sys
import getopt

from source_json import pay, app, stock, bridge
from tools import make_tree

from wfile.goapi import write_goapis, write_goapi_init
from wfile.gomodel import make_gomodels

from wfile.wflask.model import make_models
from wfile.postman import write_postman
from wfile.structure import write_deploy, write_model_doc_plant
from wfile.xmind import write_xmind
from wtest import write_test
from wfile.doc import write_docs as w_docs

from wfront import w_front
from wfile.wflask import w_flask


# ojson = order.temp_json
module_dir = {
    'flask':w_flask,
    'doc': w_docs,

}

def run(ojson,path=False,modules=['flask','go','postman','doc','ant']):
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


    write_model_doc_plant(root,ojson)

    write_test(root,ojson)
    write_postman(root,ojson)
    write_xmind(root,ojson)



    godir = os.path.join(root,f'{app}/go/src')
    make_gomodels(godir,ojson)
    write_goapi_init(root,ojson)
    write_goapis(root,ojson)

    for w in modules:
        m = module_dir.get(w)
        if m:
            m(root,ojson)


    #生成文件后做的事情

pjson   = pay.project_json         #执行支付系统
appjson = app.project_json         #执行应用
bri     = bridge.project_json
stock   = stock.project_json

basedir = os.path.abspath(os.path.dirname(__file__))
f = re.match("/mnt/c/Users/(\w*)/", basedir)
user = f.group(1)
# run(bri,path=f"/mnt/c/Users/{user}/Documents/mynut")

source_dir = {
    "bridge":bri,
    "stock":stock,
}



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
    print('module为：', args)
    print('target_dir为：', target_dir)

    path = False if target_dir == '' else target_dir

    if source == "all":
        pass
    else:
        source_json = source_dir.get(source)
        if source_json is None:
            print('Error: source json 不存在')
        else:
            run(source_dir.get(source),path,args)




if __name__ == "__main__":
    # sys.argv[1:]为要处理的参数列表，sys.argv[0]为脚本名，所以用sys.argv[1:]过滤掉脚本名。
    main(sys.argv[1:])


