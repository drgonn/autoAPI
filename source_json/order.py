source_json = {
    "app":"order-system",                  #文件源，app名
    "name":"order",                  #文件源，app名
    "dataname":"order2",                   #数据库名称
    "datapassword":"781117",
    "host":"http://frp.sealan.tech:20221",                             #文档中的域名地址
    "testhost":"frp.sealan.tech",                             #
    "testport":"20221",                             #
    "testprotocol":"http",                             #
    "blues":[
            {
                "name":"apiv1",
                "address":"/api/v1/order",      #其中一个api接口  
            }, 
        ],                             #
    "configs":[
        {
            "arg":"REDIS_HOST",
            "default":"'localhost'",
        },
        {
            "arg":"REDIS_PORT",
            "default":"6379",
        },
        {
            "arg":"SQL_NAME",
            "default":"'root'",
        },
        {
            "arg":"SQL_PASSWORD",
            "default":"'781117'",
        },
        {
            "arg":"SQL_HOST",
            "default":"'127.0.0.1:3306'",
        },
        {
            "arg":"SQL_DATABASE",
            "default":"'order1'",
        },
        {
            "arg":"SQLALCHEMY_DATABASE_URI",
            "default":"f'mysql+pymysql://{SQL_NAME}:{SQL_PASSWORD}@{SQL_HOST}/{SQL_DATABASE}'",
        },
    ],                             #
    "packages":[
        {
            "name":"REDIS_HOST",
            "version":"'localhost'",
        },
    ],                             #
    "databases":[                   #数据库表
        {
            "table":"App",
            "api":False,
            "zh": "应用",
            "parents":[],
            "repr":'name',
            "args":[
                {
                    "name":"name",
                    "type":"str",
                    "length":"64",
                    "args":[
                        {
                            "name":"index",
                            "value":"True",
                        },
                        {
                            "name":"nullable",
                            "value":"False",
                        },
                    ],
                },
                {
                    "name": "key",
                    "type": "str",
                    "length": "64",
                    "args": [
                        {
                            "name": "unique",
                            "value": "True",
                        },
                        {
                            "name": "index",
                            "value": "True",
                        },
                    ],
                },
                {
                    "name": "secret",
                    "type": "str",
                    "length": "64",
                    "args": [
                        {
                            "name": "unique",
                            "value": "True",
                        },
                    ],
                },
            ],
        },                  #App
        {
            "table":"User",
            "api":False,
            "zh": "用户",
            "parents":[
                {
                    "name": "App",
                    "index": "key",
                    "type": "str",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "应用KEY,由开发者注册应用生成，向开发者获取。",
                },
            ],
            "args":[
                {
                    "name":"uid",
                    "type":"str",
                    "length":"64",
                    "args":[
                        {
                            "name":"unique",
                            "value":"True",
                        },
                        {
                            "name":"index",
                            "value":"True",
                        },
                        {
                            "name":"nullable",
                            "value":"False",
                        },
                    ],
                },
                {
                    "name":"createDate",
                    "type":"time",
                    "args":[
                        {
                            "name":"default",
                            "value":"datetime.utcnow",
                        },
                    ],
                },
            ],
            "repr":"uid",
        },                  #User
        {
            "table": "Stuff",
            "api":True,
            "zh":"商品",
            "appfilter":1,        #当为管理员时，请求列表需要筛选列表,创建时也要使用
            "userfilter":0,        #list是否需做单独用户筛选
            "detail_sons":['Style',],
            "parents":[
                {
                    "name":"App",
                    "index": "key",
                    "type": "str",
                    "need": 0,           # 创建时候可以填写的参数
                           # 创建时候必须填写的参数
                    "putneed": 0,        # 修改时可以修改的参数
                    "listmust": 0,       # 请求列表必须post的参数
                    "mean": "应用KEY,由开发者注册应用生成，向开发者获取。",
                },
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "64",

                    "putneed": 1,
                    "mean": "商品名",
                    "post": 2,
                    "args": [
                    ],
                },
                {
                    "name": "createDate",
                    "type": "time",
                    "need": 0,
                    "mean": "商品创建时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.utcnow",
                        },
                    ],
                },
            ],
        },                  #Stuff
        {
            "table": "Style",
            "api": True,       #要不要api接口
            "zh": "商品属性",
            "repr": 'name',
            "detail_sons":['StyleValue',],
            "parents": [
                {
                    "name": "Stuff",
                    "index": "id",
                    "type": "int",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "商品id",
                },
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "64",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "商品属性名",
                    "args": [
                    ],
                },
                # {
                #     "name": "value",
                #     "type": "str",
                #     "length": "64",
                #       # 创建时候可以填写的参数
                #     "post": 2,  # 创建时候必须填写的参数
                #     "putneed": 1,  # 修改时可以修改的参数
                #     "listmust": 0,  # 请求列表必须post的参数
                #     "mean": "商品属性值",
                #     "args": [
                #     ],
                # },
            ],
        },
        {
            "table": "Good",
            "api": True,  # 要不要api接口
            "zh": "规格",
            "detail_sons":['Price','Bill'],
            "many":[
                {
                    "name": "StyleValue",
                    # "index": "id",
                    # "type": "int",
                    #   # 创建时候可以填写的参数
                    # "post": 2,  # 创建时候必须填写的参数
                    # "putneed": 0,  # 修改时可以修改的参数
                    # "listmust": 0,  # 请求列表必须post的参数
                    # "mean": "规格id",
                },
            ],
            "parents": [
                {
                    "name": "Stuff",
                    "index": "id",
                    "type": "int",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "商品id",
                },
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "64",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "规格名",
                    "args": [
                    ],
                },
                {
                    "name": "on",
                    "type": "bool",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "是否上架",
                    "args": [
                        {
                            "name": "default",
                            "value": 0,
                        },
                    ],
                },
            ],
        },             #Good
        {
            "table": "StyleValue",
            "api": True,  # 要不要api接口
            "zh": "商品属性值",
            "detail_sons":[],
            "parents": [
                {
                    "name": "Style",
                    "index": "id",
                    "type": "int",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "规格id",
                },
            ],
            "args": [
                # {
                #     "name": "name",
                #     "type": "str",
                #     "length": "64",
                #     "post": 1,  # 创建时候可以填写的参数
                #     "post": 2,  # 创建时候必须填写的参数
                #     "putneed": 1,  # 修改时可以修改的参数
                #     "listmust": 0,  # 请求列表必须post的参数
                #     "mean": "商品属性名",
                #     "args": [
                #     ],
                # },
                {
                    "name": "value",
                    "type": "str",
                    "length": "64",
                    "post": 1,  # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "商品属性值",
                    "args": [
                    ],
                },
            ],
        },             #stylevalue
        {
            "table": "Price",
            "api": True,  # 要不要api接口
            "zh": "价格",
            "detail_sons":[],
            "userfilter":1,        #是否需做单独用户筛选
            "parents": [
                {
                    "name": "Good",
                    "index": "id",     #用来反向查找关联的post参数
                    "type": "int",
                    "post": 1,  # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "规格id",
                },
                {
                    "name": "User",
                    "index": "id",
                    "type": "int",
                    "post": 1,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "所属用户id",
                },
            ],
            "args": [
                {
                    "name": "basePrice",
                    "type": "float",
                    "length": "",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "定价",
                    "args": [
                    ],
                },
                {
                    "name": "sales",
                    "type": "float",
                    "length": "",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "特价",
                    "args": [
                    ],
                },
            ],
        },             #price
        {
            "table": "Order",
            "api": True,  # 要不要api接口
            "zh": "订单",
            "repr": 'oid',
            "appfilter":1,        #当为管理员时，请求列表需要筛选列表,创建时也要使用
            "userfilter":1,        #是否需做单独用户筛选
            "detail_sons":['Bill','StatuLog'],
            "parents": [
                {
                    "name": "App",
                    "index": "name",  # 用来反向查找关联的post参数
                    "type": "str",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "所属应用名",
                },
                {
                    "name": "User",
                    "index": "id",
                    "type": "int",
                    "post": 1,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "所属用户id",
                },
            ],
            "args": [
                {
                    "name": "oid",
                    "type": "str",
                    "length": "64",
                    "need": 0,      # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,   # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 1,      # 是否支持模糊查找
                    "mean": "订单号",
                    "args": [
                        {
                            "name": "unique",
                            "value": "True",
                        },
                    ],
                },
                {
                    "name": "status",
                    "type": "int",
                    "length": "",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "订单状态：1等待支付，2等待发货，3等待验收，4完成",
                    "args": [
                        {
                            "name": "default",
                            "value": "1",
                        },
                    ],
                },
                {
                    "name": "cart",
                    "type": "bool",
                    "length": "",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 1,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "是否在购物车中",
                    "args": [
                        {
                            "name": "default",
                            "value": "1",
                        },
                    ],
                },
                {
                    "name": "time",
                    "type": "time",
                    "length": "",
                    "need": 0,      # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,   # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,      # 是否支持模糊查找
                    "mean": "创建时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.utcnow",
                        },
                    ],
                },
                {
                    "name": "totalprice",
                    "type": "float",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 0,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "订单总价格",
                    "args": [
                        {
                            "name": "default",
                            "value": 0,
                        },
                    ],
                },
                {
                    "name": "address",
                    "type": "str",
                    "length": "256",
                    "post": 1,      # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 1,   # 修改时可以修改的参数
                    "listneed": 0,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 1,      # 是否支持模糊查找
                    "mean": "收货地址",
                    "args": [
                    ],
                },
                {
                    "name": "about",
                    "type": "text",
                    "length": "",
                    "post": 1,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 0,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "订单备注",
                    "args": [
                        {
                            "name": "default",
                            "value": 0,
                        },
                    ],
                },
            ],
        },             #order
        {
            "table": "Bill",
            "api": 1,  # 要不要api接口
            "zh": "订单内的商品标签",
            "repr": 'id',
            "detail_sons":[],
            # "userfilter":1,        #是否需做单独用户筛选
            "parents": [
                {
                    "name": "Order",
                    "index": "id",  # 用来反向查找关联的post参数
                    "type": "int",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 1,  # 请求列表必须post的参数
                    "mean": "所属订单id",
                },
                {
                    "name": "Good",
                    "index": "id",
                    "type": "int",
                          # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 0,   # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "所属用户id",
                },
                # {
                #     "name": "User",
                #     "index": "id",
                #     "type": "int",
                #     "post": 1,  # 创建时候可以填写的参数
                #       # 创建时候必须填写的参数
                #     "putneed": 0,  # 修改时可以修改的参数
                #     "listmust": 0,  # 请求列表必须post的参数
                #     "mean": "所属用户id",
                # },
            ],
            "args": [
                {
                    "name": "count",
                    "type": "int",
                    "length": "",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "订单状态：1等待支付，2等待发货，3等待验收，4完成",
                    "args": [
                        {
                            "name": "default",
                            "value": 0,
                        },
                    ],
                },
                {
                    "name": "price",
                    "type": "float",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 0,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "订单总价格",
                    "args": [
                        {
                            "name": "default",
                            "value": 0,
                        },
                    ],
                },
            ],
        },             #bill
        {
            "table": "StatuLog",
            "api": False,  # 要不要api接口
            "zh": "订单状态变更日志",
            "repr": 'id',
            "detail_sons":[],
            "parents": [
                {
                    "name": "Order",
                    "index": "id",  # 用来反向查找关联的post参数
                    "type": "int",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 1,  # 请求列表必须post的参数
                    "mean": "所属订单id",
                },
            ],
            "args": [
                {
                    "name": "status",
                    "type": "int",
                    "length": "",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "订单状态：1等待支付，2等待发货，3等待验收，4完成",
                    "args": [
                        {
                            "name": "default",
                            "value": "1",
                        },
                    ],
                },
                {
                    "name": "time",
                    "type": "bool",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "创建时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.utcnow",
                        },
                    ],
                },
            ],
        },
    ]

}



