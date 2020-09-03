from .api_many import write_many_apis
import os
import re

def w_python_file(root,ojson):
    appname = ojson.get('app')
    # root = os.path.join(root, f'{appname}/front/')

    basedir = os.path.abspath(os.path.dirname(__file__))
    f = re.match("/mnt/c/Users/(\w*)/",basedir)
    user = f.group(1)
    root = f"/mnt/c/Users/{user}/rong/project/autoAPI/work/"
    write_many_apis(root,ojson)
