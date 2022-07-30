import os




class ResetApiInterface(object):
    def __init__(self, curd, blue_path, path_prefix, index_arg, zh_table_name, table_name):
        self.curd=curd
        self.blue_path=blue_path or ""
        self.path_prefix=path_prefix or ""
        self.index_arg=index_arg or "id"
        self.zh_table_name=zh_table_name
        self.table_name=table_name

        path = os.path.join(self.blue_path,self.path_prefix,self.table_name)

        self.path_args = []
        self.input_args = []
        self.out_args = []

        if curd == "c":
            self.zh_name = f"创建{self.zh_table_name}"
            self.METHOD = "POST"
            self.path = path
        elif curd == "u":
            self.zh_name = f"修改{self.zh_table_name}"
            self.METHOD = "PUT"
            self.path = path+f"/{{{self.index_arg}}}"
        elif curd == "r":
            self.zh_name = f"获取单个{self.zh_table_name}"
            self.METHOD = "GET"
            self.path = path+f"/{{{self.index_arg}}}"
        elif curd == "d":
            self.zh_name = f"删除{self.zh_table_name}"
            self.METHOD = "DELETE"
            self.path = path+f"/{{{self.index_arg}}}"
        elif curd == "rs":
            self.zh_name = f"分页获取{self.zh_table_name}"
            self.METHOD = "GET"
            self.path = path+f"s"
        elif curd == "ds":
            self.zh_name = f"批量删除{self.zh_table_name}"
            self.METHOD = "DELETE"
            self.path = path+"s"

        