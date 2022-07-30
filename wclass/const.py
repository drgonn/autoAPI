"""存放一些常量"""


class Api(object):
    def __init__(self, zh, method, index=False):
        self.zh = zh
        self.method = method
        self.METHOD = method.upper()
        self.index = index
              

ResetAPI = (
    Api('创建', 'post'),
    Api('修改', 'put', index=True),
    Api('单个查询', 'get', index=True),
    Api('列表查询', 'get'),
    Api('单个删除', 'delete', index=True),
    Api('批量删除', 'delete'),
    )
