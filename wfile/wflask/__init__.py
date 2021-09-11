
from wfile.wflask.auth import write_auth
from wfile.wflask.config import write_config
from wfile.wflask.init import make_init
from wfile.wflask.init_manage import write_init
from wfile.wflask.model import write_models
from wfile.wflask.admin import write_admin
from wfile.structure import write_deploy
from wfile.wflask.api import write_apis, write_api_init

import os
import re

def w_flask(root,ojson):
    make_init(root,ojson)
    write_config(root, ojson)
    write_deploy(root, ojson)
    write_admin(root,ojson)
    write_init(root,ojson)
    write_auth(root,ojson)
    write_apis(root,ojson)
    write_models(root,ojson)
    #生成文件后做的事情,要放在最后做
    write_api_init(root, ojson)

    print(":--flask运行完成")
