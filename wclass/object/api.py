"""api的接口对象
所有的表数据都要生成api接口
api接口包含提交参数和返回参数
地址等等信息

"""



# 接口对象
class ApiInterface(object):
    def __init__(self, zh_name, path, method, input_args, out_args):
        self.zh_name = zh_name           # 接口中文名称
        self.path = path                 # 接口地址
        self.method = method.lower()             # 请求方法,小写
        self.METHOD = method.upper()             # 请求方法,小写
        self.Method = method.capitalize()           # 请求方法,首字母大写

        self.input_args = input_args           # 请求参数
        self.out_args = out_args            # 返回的参数


