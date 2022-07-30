import os

from allobject.data_type import DataType




class ApiArg(object):
    def __init__(self, name, zh_name, type, required, about="", default=""):
        self.zh_name=zh_name
        self.name=name
        self.type=DataType(type)
        self.about=about or ""
        self.default=default or ""
        self.required=required

        self.zh_required = "是" if self.required else "否"


data_arg = ApiArg('data', '详细信息','object',True) 
# 返回的状态参数
status_out_args = [
    ApiArg('status', '状态','Boolean',True),
    ApiArg('code', '状态码','Integer',True),
    ApiArg('message', '错误信息','String',False),
]
list_arg = ApiArg('list', '分页信息','list',True)
page_query_args  = [
    ApiArg('per_page', '分页条数','Integer',False),
    ApiArg('current', '当前页数','Integer',False),
]
page_return_args = [
    ApiArg('per_page', '分页条数','Integer',True),
    ApiArg('current', '当前页数','Integer',True),
    ApiArg('size', '当前页数据条数','Integer',True),
    ApiArg('total', '数据总数','Integer',True),
]