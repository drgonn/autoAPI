"""
输入和输出参数对象

"""
from version2.allobject.data_type import DataType 



# 参数对象
class Arg(object):
    def __init__(self, zh_name, name, type, index, about, unique, sql_not_null, default):
        self.zh_name = zh_name    # 参数中文名               
        self.name = name          # 参数名  ,如： date_time                 
        self.type = DataType(type)          # type对象类型

        self.about = about or ""
        self.index = index      # 用来做唯一辨识符的标签，为true时候，get和delete请求不再使用id，而使用它
        self.unique = unique    # 用来判断该值在哪个范围内唯一，global则是全局唯一
        self.not_null = sql_not_null
        self.default = default

