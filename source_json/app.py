project_json = {
    "app":"developer",                  #文件源，app名
    "dataname":"developer",                   #数据库名称
    "datapassword":"781117",
    "host":"未知",                             #文档中的域名地址
    "testhost":"http://frp.sealan.tech:20223",                             #
    "testport":"20221",                             #
    "testprotocol":"http",                             #
    "blues":[
            {
                "name":"apiv1",
                "address":"/api/v1/order",      #其中一个api接口  
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
            "api":1,
            "zh": "开发者",
            "parents":[
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
                    "name":"super",
                    "type":"bool",
                    "mean": "超级用户",
                    "listneed": 1,  # 请求列表可以用来筛选的参数
                    "args":[
                        {
                            "name":"default",
                            "value":0,
                        },
                    ],
                },
                {
                    "name":"createTime",
                    "type":"time",


                    "listneed": 1,  # 请求列表可以用来筛选的参数
                    "mean": "创建时间",
                    "args":[
                        {
                            "name":"default",
                            "value":"datetime.utcnow",
                        },
                    ],
                },
                {
                    "name": "password_hash",
                    "length": "64",
                    "type": "str",
                    "need": 0,      # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,   # 修改时可以修改的参数
                    "listneed": 0,  # 请求列表可以用来筛选的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "密码hash",
                },
                {
                    "name": "username",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 1,
                    "mean": "组件名",

                    "args": [
                    ],
                },
                {
                    "name": "phone",
                    "length": "64",
                    "type": "str",
                    "post": 1,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "手机号",
                },
                {
                    "name": "email",
                    "length": "64",
                    "type": "str",
                    "post": 1,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "邮箱",
                },
                {
                    "name": "emailbind",
                    "type": "bool",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "邮箱是否绑定",
                },
                {
                    "name": "company",
                    "length": "64",
                    "type": "str",
                    "post": 1,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 0,  # 请求列表可以用来筛选的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "公司名称",
                },
                {
                    "name": "address",
                    "length": "64",
                    "type": "str",
                    "post": 1,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 0,  # 请求列表可以用来筛选的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "公司地址",
                },
                {
                    "name": "url",
                    "length": "128",
                    "type": "str",
                    "post": 1,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 0,  # 请求列表可以用来筛选的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "公司网址",
                },
                {
                    "name": "openid",
                    "length": "64",
                    "type": "str",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "openid",
                },
                {
                    "name": "unionid",
                    "length": "64",
                    "type": "str",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 0,  # 请求列表可以用来筛选的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "unionid",
                },
                {
                    "name": "nickname",
                    "length": "64",
                    "type": "str",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "微信昵称",
                },
                {
                    "name": "headimgurl",
                    "length": "64",
                    "type": "str",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "微信头像地址",
                },
            ],
            "repr":"uid",
        },                  #User
        {
            "table":"UserLog",
            "api":1,
            "zh": "开发者日志",
            "parents":[
                {
                    "name": "User",
                    "index": "id",
                    "type": "int",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "开发者ID",
                },
            ],
            "args":[
                {
                    "name":"ip",
                    "type":"str",
                    "length":"128",
                    "mean": "登录IP",
                    "args":[
                    ],
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选的参数
                    "listmust": 0,  # 请求列表必须post的参数
                },
                {
                    "name":"userAgent",
                    "type":"str",
                    "length":"512",
                    "mean": "Agent",
                    "args":[
                    ],
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选的参数
                    "listmust": 0,  # 请求列表必须post的参数
                },
                {
                    "name":"msg",
                    "type":"text",
                    "mean": "登录信息",
                    "args":[
                    ],
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选的参数
                    "listmust": 0,  # 请求列表必须post的参数
                },
                {
                    "name":"time",
                    "type":"time",
                    "mean": "登录时间",
                    "args":[
                        {
                            "name":"default",
                            "value":"datetime.utcnow",
                        },
                    ],
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选的参数
                    "listmust": 0,  # 请求列表必须post的参数
                },
            ],
            "repr":"uid",
        },                  #UserLog
        {
            "table":"App",
            "api":1,
            "zh": "应用",
            "repr":'name',
            "userfilter":1,        #list是否需做单独用户筛选
            "parents":[
                {
                    "name": "User",
                    "index": "id",
                    "type": "int",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "开发者ID",
                },
            ],
            "args":[
                {
                    "name":"name",
                    "type":"str",
                    "length":"64",
                    "mean": "app名",
                    "args":[
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
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选的参数
                    "listmust": 0,  # 请求列表必须post的参数
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
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选的参数
                    "listmust": 0,  # 请求列表必须post的参数
                },
                {
                    "name": "about",
                    "type": "str",
                    "length": "128",
                    "post": 1,
                    "putneed": 1,
                    "mean": "应用描述",

                    "args": [
                    ],
                },
                {
                    "name": "createTime",
                    "type": "time",
                    "need": 0,
                    "mean": "创建时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.utcnow",
                        },
                    ],
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选的参数
                    "listmust": 0,  # 请求列表必须post的参数
                },
            ],
        },                  #App
        {
            "table": "Module",
            "api":True,
            "zh":"组件",
            "userfilter":1,        #list是否需做单独用户筛选
            "appfilter":0,        #当为管理员时，请求列表需要筛选列表,创建时也要使用
            "many":[
                # {
                #     "name": "App",
                #     "index": "id",
                #     "type": "int",
                #     "post": 1,  # 创建时候可以填写的参数
                #     "post": 2,  # 创建时候必须填写的参数
                #     "putneed": 0,  # 修改时可以修改的参数
                #     "listmust": 0,  # 请求列表必须post的参数
                #     "mean": "规格id",
                # },
            ],
            "parents":[
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 0,
                    "mean": "组件名",
                    "post": 2,
                    "args": [
                    ],
                },
                {
                    "name": "url",
                    "type": "str",
                    "length": "128",

                    "putneed": 1,
                    "mean": "组件调用地址",
                    "post": 2,
                    "args": [
                    ],
                },
                {
                    "name": "about",
                    "type": "str",
                    "length": "128",
                    "post": 1,
                    "putneed": 1,
                    "mean": "组件描述",

                    "args": [
                    ],
                },
                {
                    "name": "createTime",
                    "type": "time",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "创建时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.utcnow",
                        },
                    ],
                },
            ],
        },                  #Module
        {
            "table": "Service",
            "api": True,
            "zh": "拥有的服务",
            "userfilter": 1,  # list是否需做单独用户筛选
            "appfilter": 0,  # 当为管理员时，请求列表需要筛选列表,创建时也要使用
            "many": [
                {
                    "name": "Package",
                    # "index": "id",
                    # "type": "int",
                    # "post": 1,  # 创建时候可以填写的参数
                    # "post": 2,  # 创建时候必须填写的参数
                    # "putneed": 0,  # 修改时可以修改的参数
                    # "listmust": 0,  # 请求列表必须post的参数
                    # "mean": "规格id",
                },
            ],
            "parents": [
                {
                    "name": "App",
                    "index": "id",
                    "type": "int",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 0,  # 请求列表可以用来筛选的参数
                    "mean": "appid",
                },
                {
                    "name": "Module",
                    "index": "id",
                    "type": "int",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "规格id",
                },
                {
                    "name": "User",
                    "index": "id",
                    "type": "int",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "开发者ID",
                },
            ],
            "args": [
                {
                    "name": "payType",
                    "type": "int",
                    "post": 1,
                    "putneed": 1,
                    "mean": "付费类型，1按时间，2按次",

                    "args": [
                    ],
                },
                {
                    "name": "activate",
                    "type": "bool",
                    "post": 1,
                    "putneed": 1,
                    "mean": "启用状态",

                    "args": [
                        {
                            "name": "default",
                            "value": 0,
                        },
                    ],
                },
                {
                    "name": "expireTime",
                    "type": "time",
                    "need": 0,
                    "postneed": 1,
                    "mean": "到期时间",
                    "args": [
                    ],
                },
                {
                    "name": "maxTime",
                    "type": "int",
                    "post": 1,
                    "putneed": 1,
                    "mean": "最多调用次数",
                    "postneed": 1,
                    "args": [
                    ],
                },
                {
                    "name": "createTime",
                    "type": "time",
                    "need": 0,
                    "mean": "创建时间",
                    "postneed": 1,
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.utcnow",
                        },
                    ],
                },
            ],
        },  # service
        {
            "table": "Package",
            "api": True,
            "zh": "服务套餐",
            "userfilter": 1,  # list是否需做单独用户筛选
            "appfilter": 0,  # 当为管理员时，请求列表需要筛选列表,创建时也要使用
            "many": [
            ],
            "parents": [
                {
                    "name": "Module",
                    "index": "id",
                    "type": "int",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "组件id",
                },
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 1,
                    "mean": "套餐名",

                    "args": [
                    ],
                },
                {
                    "name": "gid",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 0,
                    "mean": "规格gid",

                    "args": [
                    ],
                },
                {
                    "name": "price",
                    "type": "float",
                    "post": 1,
                    "putneed": 1,
                    "mean": "套餐名",

                    "args": [
                    ],
                },
                {
                    "name": "type",
                    "type": "int",
                    "post": 1,
                    "putneed": 1,
                    "mean": "套餐类型，1按天，2按月，3按年，4，按次",
                    "postneed": 1,
                    "args": [
                    ],
                },
                {
                    "name": "times",
                    "type": "int",
                    "post": 1,
                    "putneed": 1,
                    "mean": "付费类型的数量",
                    "postneed": 1,
                    "args": [
                    ],
                },
                {
                    "name": "about",
                    "type": "str",
                    "length": "128",
                    "post": 1,
                    "putneed": 1,
                    "mean": "描述",

                    "args": [
                    ],
                },
                {
                    "name": "createTime",
                    "type": "time",
                    "need": 0,
                    "postneed": 1,
                    "mean": "创建时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.utcnow",
                        },
                    ],
                },
            ],
        },  # package
        {
            "table": "AppLog",
            "api": 1,
            "zh": "应用日志",
            "repr": 'name',
            "parents": [
                {
                    "name": "App",
                    "index": "id",
                    "type": "int",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "APP",
                },
                {
                    "name": "User",
                    "index": "id",
                    "type": "int",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "开发者ID",
                },
            ],
            "args": [
                {
                    "name": "type",
                    "type": "int",
                    "post": 1,
                    "listneed": 1,
                    "mean": "类型，1创建，2修改，3添加服务，4，删除服务，5到期关闭服务",
                    "args": [
                    ],
                },
                {
                    "name":"msg",
                    "type":"text",
                    "mean": "修改信息",
                    "listneed": 1,
                    "args":[
                    ],
                },
                {
                    "name":"createTime",
                    "type":"time",
                    "mean": "创建时间",
                    "listneed": 1,
                    "args":[
                        {
                            "name":"default",
                            "value":"datetime.utcnow",
                        },
                    ],
                },
            ],
        },  # AppLog
        {
            "table": "ServiceLog",
            "api": 1,
            "zh": "服务日志",
            "repr": 'name',
            "parents": [
                {
                    "name": "Service",
                    "index": "id",
                    "type": "int",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "listneed": 1,
                    "mean": "服务ID",
                },
                {
                    "name": "App",
                    "index": "id",
                    "type": "int",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "listneed": 1,
                    "mean": "appid",
                },
            ],
            "args": [
                {
                    "name": "type",
                    "type": "int",
                    "mean": "类型，1开通，2续费，3停用",
                    "listneed": 1,
                    "args": [
                    ],
                },
                {
                    "name": "msg",
                    "type": "text",
                    "mean": "修改信息",
                    "listneed": 1,
                    "args": [
                    ],
                },
                {
                    "name": "createTime",
                    "type": "time",
                    "mean": "创建时间",
                    "listneed": 1,
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.utcnow",
                        },
                    ],
                },
            ],
        },  # ServiceLog
    ],
    "configs": [
        {
            "arg": "SQL_NAME",
            "default": "root",
            'deploy': 1,
        },
        {
            "arg": "SQL_HOST",
            "default": "db",
            'deploy': 1,
        },
        {
            "arg": "SQL_PASSWORD",
            "default": "668899",
            'deploy': 1,
        },
        {
            "arg": "SQL_DATABASE",
            "default": "pay",
            'deploy': 1,
        },
        {
            "arg": "REDIS_PORT",
            "default": "6379",
        },
        {
            "arg": "SQL_NAME",
            "default": "'root'",
        },
        {
            "arg": "SQL_PASSWORD",
            "default": "'781117'",
        },
        {
            "arg": "SQL_HOST",
            "default": "'127.0.0.1:3306'",
        },
        {
            "arg": "SQL_DATABASE",
            "default": "'order1'",
        },
        {
            "arg": "SQLALCHEMY_DATABASE_URI",
            "default": "f'mysql+pymysql://{SQL_NAME}:{SQL_PASSWORD}@{SQL_HOST}/{SQL_DATABASE}'",
        },
    ],  #
}



