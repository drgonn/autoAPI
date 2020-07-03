project_json = {
    "app":"bridge",                  #文件源，app名
    "dataname":"bridge",                   #数据库名称
    "datapassword":"781117",
    "host":"http://frp.sealan.tech:20303",                             #文档中的域名地址
    "testhost":"frp.sealan.tech",                             #
    "testport":"20303",                             #
    "testprotocol":"http",                             #
    "blues":[
            {
                "name":"apiv1",
                "address":"/api/v1/bridge",      #其中一个api接口
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
            "table":"User",
            "api":False,
            "zh": "用户",
            "parents":[
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
            "table":"Province",
            "api":1,
            "zh": "省",
            "parents":[
            ],
            "args":[
                {
                    "name":"name",
                    "type":"str",
                    "length":"64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique":1,
                    "mean": "省名",
                    "args":[
                    ],
                },
            ],
            "repr":"name",
        },                  #省
        {
            "table":"City",
            "api":1,
            "zh": "市",
            "parents":[
                {
                    "name": "Province",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "省份id",
                },
            ],
            "args":[
                {
                    "name":"name",
                    "type":"str",
                    "length":"64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "市名",
                    "unique":1,
                    "args":[
                    ],
                },
            ],
            "repr":"name",
        },                  #市
        {
            "table":"Area",
            "api":1,
            "zh": "行政区",
            "parents":[
                {
                    "name": "City",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "市id",
                },
            ],
            "args":[
                {
                    "name":"name",
                    "type":"str",
                    "length":"64",
                    "unique":1,
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "行政区名",
                    "args":[
                    ],
                },
            ],
            "repr":"name",
        },                  #area
        {
            "table":"Bridgetype",
            "api":1,
            "zh": "桥梁种类",
            "parents":[
            ],
            "args":[
                {
                    "name":"name",
                    "type":"str",
                    "length":"64",
                    "unique":1,
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "桥梁种类名",
                    "args":[
                    ],
                },
            ],
            "repr":"name",
        },                  #桥梁种类
        {
            "table": "Bridge",
            "api": 1,
            "zh": "桥梁",
            "parents": [
                {
                    "name": "Bridgetype",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "桥梁种类id",
                    "tojson": "name",    #在json字段当中显示的参数
                },
                {
                    "name": "Province",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "省份id",
                    "tojson": "name",
                },
                {
                    "name": "City",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "市id",
                    "tojson": "name",
                },
                {
                    "name": "Area",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "行政区id",
                    "tojson": "name",
                },
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 1,  # 是否支持模糊查找
                    "mean": "桥梁名",
                    "unique":1,
                    "args": [
                    ],
                },
                {
                    "name": "safe_score",
                    "type": "float",
                    "length": "",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "安全分数",
                    "args": [
                    ],
                },
                {
                    "name": "advice",
                    "type": "text",
                    "length": "",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 0,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "管养建议",
                    "args": [
                    ],
                },
                {
                    "name": "monit_about",
                    "type": "text",
                    "length": "",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 0,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "监测框架介绍",
                    "args": [
                    ],
                },
                {
                    "name": "update_time",
                    "type": "time",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "更新时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.now",
                        },
                    ],
                },
                {
                    "name": "create_time",
                    "type": "time",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "创建时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.now",
                        },
                    ],
                },

            ],
            "repr": "name",
        },  # 桥梁
        {
            "table": "Property",
            "api": 1,
            "zh": "桥梁属性名",
            "parents": [
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "桥梁属性名",
                    "args": [
                    ],
                },
                {
                    "name": "about",
                    "type": "text",
   #                 "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "简介",
                    "args": [
                    ],
                },
            ],
            "repr": "name",
        },  # 桥梁属性名
        {
            "table": "Propertyvalue",
            "api": 1,
            "zh": "桥梁属性值",
            "parents": [
                {
                    "name": "Property",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "桥梁属性名id",
                },
                {
                    "name": "Bridge",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "桥梁id",
                },
            ],
            "args": [
                {
                    "name": "value",
                    "type": "float",
                    #                 "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "桥梁属性名",
                    "args": [
                    ],
                },
                {
                    "name": "create_time",
                    "type": "time",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "创建时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.now",
                        },
                    ],
                },

            ],
            "repr": "id",
        },  # 桥梁属性值
        {
            "table": "Filetype",
            "api": 1,
            "zh": "文件类型",
            "parents": [
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "文件类型名",
                    "args": [
                    ],
                },
                {
                    "name": "type",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "文件的种类：1图片，2excel，3pdf",
                    "args": [
                    ],
                },
            ],
            "repr": "name",
        },  # 文件类型
        {
            "table": "File",
            "api": 1,
            "zh": "文件",
            "parents": [
                {
                    "name": "Filetype",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "文件类型id",
                },
                {
                    "name": "Bridge",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "桥梁id",
                },
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "64",
                    "need": 0,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表必须post的参数
                    "like": 1,  # 是否支持模糊查找
                    "mean": "文件名",
                    "args": [
                    ],
                },
                {
                    "name": "page",
                    "type": "int",
                    # "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "分册",
                    "args": [
                    ],
                },
                {
                    "name": "update_time",
                    "type": "time",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "更新时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.now",
                        },
                    ],
                },
                {
                    "name": "create_time",
                    "type": "time",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "创建时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.now",
                        },
                    ],
                },

            ],
            "repr": "name",
        },  # 文件
        {
            "table": "Product",
            "api": 1,
            "zh": "产品",
            "parents": [
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "产品名",
                    "args": [
                    ],
                },

            ],
            "repr": "name",
        },  # 产品
        {
            "table": "Productimg",
            "api": 1,
            "zh": "产品图片",
            "parents": [
                {
                    "name": "Product",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "产品id",
                },
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "256",
                    "need": 0,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "图片名",
                    "args": [
                    ],
                },

            ],
            "repr": "name",
        },  # 产品图片
        {
            "table": "Location",
            "api": 1,
            "zh": "桥梁位置",
            "parents": [
                {
                    "name": "Bridge",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "桥梁id",
                },
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "256",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "位置名称",
                    "args": [
                    ],
                },
                {
                    "name": "latitude",
                    "type": "float",
                    # "length": "128",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "纬度",
                    "args": [
                    ],
                },
                {
                    "name": "longitude",
                    "type": "float",
                    # "length": "128",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "经度",
                    "args": [
                    ],
                },
            ],
            "repr": "name",
        },  # 桥梁位置
        {
            "table": "Device",
            "api": 1,
            "zh": "设备",
            "many":[
                {
                    "name": "Monitarg",
                },
            ],
            "parents": [
                {
                    "name": "Product",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "产品id",
                },
                {
                    "name": "Bridge",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "桥梁id",
                },
                {
                    "name": "Location",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "位置id"
                },
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "设备名",
                    "args": [
                    ],
                },
                {
                    "name": "sn",
                    "type": "str",
                    "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 1,  # 是否支持模糊查找
                    "mean": "序列号",
                    "args": [
                    ],
                },
                {
                    "name": "exception",
                    "type": "bool",
                    "need": 0,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 1,
                    "like": 0,  # 是否支持模糊查找
                    "mean": "是否异常",
                    "args": [
                        {
                            "name": "default",
                            "value": 0,
                        },
                    ],
                },
                {
                    "name": "fault",
                    "type": "bool",
                    "need": 0,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 1,
                    "like": 0,  # 是否支持模糊查找
                    "mean": "是否故障",
                    "args": [
                        {
                            "name": "default",
                            "value": 0,
                        },
                    ],
                },
                {
                    "name": "update_time",
                    "type": "time",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "更新时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.now",
                        },
                    ],
                },
                {
                    "name": "create_time",
                    "type": "time",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "创建时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.now",
                        },
                    ],
                },

            ],
            "repr": "name",
        },  # 设备
        {
            "table": "Devicelog",
            "api": 1,
            "zh": "设备日志",
            "parents": [
                {
                    "name": "Device",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "设备id",
                },
            ],
            "args": [
                {
                    "name": "position",
                    "type": "int",
                    # "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "设备位置代号",
                    "args": [
                    ],
                },
                {
                    "name": "exception",
                    "type": "bool",
                    "need": 0,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 1,
                    "like": 0,  # 是否支持模糊查找
                    "mean": "是否异常",
                    "args": [
                    ],
                },
                {
                    "name": "fault",
                    "type": "bool",
                    "need": 0,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 1,
                    "like": 0,  # 是否支持模糊查找
                    "mean": "是否故障",
                    "args": [
                    ],
                },
                {
                    "name": "create_time",
                    "type": "time",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "创建时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.now",
                        },
                    ],
                },

            ],
            "repr": "name",
        },  # 设备日志
        {
            "table": "Monitgroup",
            "api": 1,
            "zh": "监控分组",
            "parents": [
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "监控分组名",
                    "args": [
                    ],
                },
            ],
            "repr": "name",
        },  # 监控分组
        {
            "table": "Monittype",
            "api": 1,
            "zh": "监控类型",
            "parents": [
                {
                    "name": "Monitgroup",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "监控分组id",
                },
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "监控类型名",
                    "args": [
                    ],
                },
            ],
            "repr": "name",
        },  # 监控类型
        {
            "table": "Monitarg",
            "api": 1,
            "zh": "监控参数",
            "parents": [
                {
                    "name": "Monittype",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "监控类型id",
                },
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "监控参数名",
                    "args": [
                    ],
                },
            ],
            "repr": "name",
        },  # 监控参数
        {
            "table": "Monitvalue",
            "api": 1,
            "zh": "监控参数值",
            "parents": [
                {
                    "name": "Monitarg",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "监控类型id",
                },
                {
                    "name": "Device",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "设备id",
                },
            ],
            "args": [
                {
                    "name": "value",
                    "type": "float",
                    # "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "监控参数值",
                    "args": [
                    ],
                },
            ],
            "repr": "value",
        },  # 监控参数值
        {
            "table": "Excepttrigger",
            "api": 1,
            "zh": "监控参数异常条件",
            "parents": [
                {
                    "name": "Monitvalue",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "监控类型id",
                },
            ],
            "args": [
                {
                    "name": "value",
                    "type": "float",
                    # "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "监控参数值",
                    "args": [
                    ],
                },
                {
                    "name": "compare",
                    "type": "int",
                    # "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "取值执行条件，1:<,2:>,3:=",
                    "args": [
                    ],
                },
                {
                    "name": "logic",
                    "type": "int",
                    # "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "取值判断条件，1: and, 0: or",
                    "args": [
                    ],
                },
            ],
            "repr": "id",
        },  # 监控异常范围
        {
            "table": "Valuelog",
            "api": 1,
            "zh": "监控值日志",
            "parents": [
                {
                    "name": "Monitvalue",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "监控值id",
                },
            ],
            "args": [
                {
                    "name": "value",
                    "type": "float",
                    # "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "监控参数名",
                    "args": [
                    ],
                },
                {
                    "name": "create_time",
                    "type": "time",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "创建时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.now",
                        },
                    ],
                },
            ],
            "repr": "id",
        },  # 监控参数值日志
        {
            "table": "Warn",
            "api": 1,
            "zh": "预警",
            "parents": [
                {
                    "name": "Bridge",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "桥梁id",
                },
                {
                    "name": "Device",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "设备id",
                },
            ],
            "args": [
                {
                    "name": "statu",
                    "type": "bool",
                    # "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数int
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "处理状态，1已处理，0未处理",
                    "args": [
                        {
                            "name": "default",
                            "value": 0,
                        },
                    ],
                },
                {
                    "name": "about",
                    "type": "text",
   #                 "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "预警处理结果",
                    "args": [
                    ],
                },
            ],
            "repr": "id",
        },  # 预警信息
        {
            "table": "Contact",
            "api": 1,
            "zh": "应急联络网",
            "parents": [
                {
                    "name": "Bridge",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "桥梁id",
                },
            ],
            "args": [
                {
                    "name": "about",
                    "type": "text",
   #                 "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "简介",
                    "args": [
                    ],
                },
            ],
            "repr": "id",
        },  # 应急联络网
        {
            "table": "Plan",
            "api": 1,
            "zh": "应急预案模板",
            "parents": [
                {
                    "name": "Bridge",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "桥梁id",
                },
            ],
            "args": [
                {
                    "name": "about",
                    "type": "text",
   #                 "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "预警处理结果",
                    "args": [
                    ],
                },
            ],
            "repr": "id",
        },  # 应急预案模板
        {
            "table": "Material",
            "api": 1,
            "zh": "应急物资管理",
            "parents": [
                {
                    "name": "Bridge",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "桥梁id",
                },
            ],
            "args": [
                {
                    "name": "about",
                    "type": "text",
   #                 "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "预警处理结果",
                    "args": [
                    ],
                },
            ],
            "repr": "id",
        },  # 应急物资管理
        {
            "table": "Emergency",
            "api": 1,
            "zh": "应急抢险队伍管理",
            "parents": [
                {
                    "name": "Bridge",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "桥梁id",
                },
            ],
            "args": [
                {
                    "name": "about",
                    "type": "text",
   #                 "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 0,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "预警处理结果",
                    "args": [
                    ],
                },
            ],
            "repr": "id",
        },  # 应急抢险队伍管理
        {
            "table": "Emgreport",
            "api": 1,
            "zh": "应急报告管理",
            "parents": [
                {
                    "name": "Bridge",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "桥梁id",
                },
            ],
            "args": [
                {
                    "name": "about",
                    "type": "text",
   #                 "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust":0,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "预警处理结果",
                    "args": [
                    ],
                },
            ],
            "repr": "id",
        },  # 应急报告管理

    ]
}







