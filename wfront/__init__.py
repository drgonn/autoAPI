from .component.data import w_component_data
from .component.index import w_component_index
from .component.service import w_component_service

from .config.package import modify_package_json
from .config.config import w_config_config
import os
import re

def w_front(root,ojson):
    appname = ojson.get('app')
    antport = ojson.get('antport')
    root = os.path.join(root, f'{appname}/front/')
    print(root,'root')
    basedir = os.path.abspath(os.path.dirname(__file__))
    # f = re.match("/mnt/c/Users/(\w*)/",basedir)
    # user = f.group(1)
    # root = f"/mnt/c/Users/{user}/rong/project/stock/front/my-stock"
    w_component_data(root,ojson)
    w_component_index(root,ojson)
    w_component_service(root,ojson)

    modify_package_json(root,ojson)
    w_config_config(root,ojson)


    print(f":--ant前端运行完成，运行地址是:  http://localhost:{antport}")
