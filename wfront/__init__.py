from .component.data import w_component_data
from .component.index import w_component_index
from .component.service import w_component_service
import os


def w_front(root,ojson):
    appname = ojson.get('app')
    # root = os.path.join(root, f'{appname}/front/')
    root = "/mnt/c/Users/dronn/rong/project/stock/front/my-stock"
    print('root',root)
    w_component_data(root,ojson)
    w_component_index(root,ojson)
    w_component_service(root,ojson)
