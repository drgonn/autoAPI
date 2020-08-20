import os
from tools import Tdb


#建立models
def make_models(appdir,ojson):
    appname = ojson.get('app')
    initdir = os.path.join(root,f'{appname}/src/__init__.py')
    modeldir = os.path.join(appdir,'models.py')
    w = open(modeldir,'w+')
    w.write(packages)
    for table in app.get('databases'):
        tableclass = table.get('table')
        tablename  = table.get('table').lower()
        tablenames = tablename + 's'
        if table.get("many"):
            for many in table.get('many'):
                manyclass = many.get('name')
                manyname = many.get('name').lower()
