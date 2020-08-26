import os
import re

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

# run(pjson)
# run(appjson)
stock = stock.project_json
# run(stock,"../stock/backend")
run(stock)

bri = bridge.project_json

basedir = os.path.abspath(os.path.dirname(__file__))
f = re.match("/mnt/c/Users/(\w*)/", basedir)
user = f.group(1)
# run(bri,path=f"/mnt/c/Users/{user}/Documents/mynut")

