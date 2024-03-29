import os
from tools import Tdb


#建立models
def make_auth(root,ojson):
    appname = ojson.get('app')
    # initdir = os.path.join(root,f'{appname}/src/__init__.py')
    # w = open(initdir,'w+')
    # w.close()

    auth = ojson.get('auth')
    if auth:
        source_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(root))), 'wfront/file/authfile/GlobalHeader')
        target = os.path.join(root, f'src/components/')
        os.system(f'cp -r {source_dir} {target}')

        source_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(root))), 'wfront/file/authfile/authority.ts')
        target = os.path.join(root, f'src/utils/authority.ts')
        os.system(f'cp {source_dir} {target}')

        source_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(root))), 'wfront/file/authfile/SecurityLayout.tsx')
        target = os.path.join(root, f'src/layouts/SecurityLayout.tsx')
        os.system(f'cp {source_dir} {target}')

        source_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(root))), 'wfront/file/authfile/user')
        target = os.path.join(root, f'src/pages/')
        os.system(f'cp -r {source_dir} {target}')

        source_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(root))), 'wfront/file/authfile/request.ts')
        target = os.path.join(root, f'src/utils/request.ts')
        os.system(f'cp {source_dir} {target}')

        source_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(root))), 'wfront/file/authfile/login.ts')
        target = os.path.join(root, f'src/models/login.ts')
        os.system(f'cp {source_dir} {target}')

        source_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(root))), 'wfront/file/authfile/user_system')
        target = os.path.join(root, f'src/pages')
        # new_target = os.path.join(root, f'src/pages/user_system/user')
        os.system(f'cp -r {source_dir} {target}')
        print(f'cp -r {source_dir} {target}')
        # os.system(f'mv  {target}/page_user {new_target}')
