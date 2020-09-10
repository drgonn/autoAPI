project_json = {
    "app":"pay",                  #文件源，app名
    "dataname":"pay",                   #数据库名称
    "datapassword":"781117",
    "host":"http://frp.sealan.tech:20222",                             #文档中的域名地址
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
                    "mean": "app名",
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
                    "mean": "app key",
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
                    "mean": "app secret",
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
                    "mean": "用户UID",
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
                    "name": "money",
                    "type": "float",
                    "post": 1,
                    "putneed": 1,
                    "mean": "账户金额",

                    "args":[
                        {
                            "name":"default",
                            "value":0,
                        },
                    ],
                },
                {
                    "name":"createDate",
                    "type":"time",
                    "mean": "创建时间",
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
            "table": "Pay",
            "api":True,
            "zh":"支付记录",
            "userfilter":1,        #list是否需做单独用户筛选
            "appfilter":1,        #当为管理员时，请求列表需要筛选列表,创建时也要使用
            "parents":[
                {
                    "name": "User",
                    "index": "uid",
                    "type": "int",
                    "post": 1,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "所属用户uid",
                },
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
                    "name": "money",
                    "type": "float",

                    "putneed": 1,
                    "mean": "交易金额",
                    "post": 2,
                    "args":[
                        {
                            "name":"default",
                            "value":0,
                        },
                    ],
                },
                {
                    "name": "gid",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 1,
                    "mean": "交易具体商品的gid",

                    "args": [
                    ],
                },
                {
                    "name": "about",
                    "type": "str",
                    "length": "128",
                    "post": 1,
                    "putneed": 1,
                    "mean": "交易用途",

                    "args": [
                    ],
                },
                {
                    "name": "activateUrl",
                    "type": "str",
                    "length": "128",
                    "post": 1,
                    "putneed": 1,
                    "mean": "生效链接",

                    "args": [
                    ],
                },
                {
                    "name": "time",
                    "type": "time",
                    "need": 0,
                    "mean": "交易时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.utcnow",
                        },
                    ],
                },
            ],
        },                  #pay
    ]

}



