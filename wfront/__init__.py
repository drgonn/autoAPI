from .component.data import w_component_data
from .component.index import w_component_index
from .component.service import w_component_service

from .config.package import modify_package_json
from .config.config import w_config_config
from .config.proxy import w_config_proxy
import os
import re
import shutil



def w_front(root,ojson):
    appname = ojson.get('app')
    antport = ojson.get('antport')

    ant_dir = os.path.join(os.path.dirname(root),'front')

    root = os.path.join(root, f'{appname}/front')
    if not os.path.exists(root):
        os.system(f'cp -R {ant_dir} {root}')


    w_component_data(root,ojson)
    w_component_index(root,ojson)
    w_component_service(root,ojson)

    modify_package_json(root,ojson)
    w_config_config(root,ojson)
    w_config_proxy(root,ojson)

    print(f":--ant前端运行完成，运行地址是:  http://localhost:{antport}")
