project_json = {
    "app":"order-system",                  #文件源，app名
    "name":"order",                  #文件源，app名
    "dataname":"order2",                   #数据库名称
    "datapassword":"781117",
    "host":"http://frp.sealan.tech:20221",                             #文档中的域名地址
    "testhost":"frp.sealan.tech",                             #
    "testport":"20221",                             #
    "testprotocol":"http",                             #
    "anthost":"localhost",                             #  ant 调试访问地址
    "antport":"20305",                             #ant 调试访问地址
    "auth": 1,                                     #是否需要用户登录认证YY
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
            "table": "Pack",
            "api": 1,
            "zh": "流量包",
            "crud":['post','put','delete'],
            "parents": [
            ],
            "many":[
                {
                    "name": "Card",
                    "add_api": 1,       # true时 api 接口当中的put  写上添加对方的ids。
                },
                ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "64",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数,0不需要，1可填，2，必须填写
                    "put": 1,  # 修改时可以修改的参数,0不需要，1可填，2，必须填写
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "名",
                    "filter": "like",
                },
                {
                    "name": "usage",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "流量大小（M）",
                    "filter": "precise",
                },
                {
                    "name": "months",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "周期（月）",
                    "filter": "precise",
                },
                {
                    "name": "price",
                    "type": "float",
                    "post": 1,   # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "价格（元）",
                    "filter": "precise",
                },
                {
                    "name": "operator",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "运营商分类",
                    "filter": "precise",
                    "corres": [
                        {'key':1,'value':"移动"},
                        {'key':2,'value':"联通"},
                        {'key':3,'value':"电信"},
                    ],
                },
                {
                    "name": "about",
                    "type": "text",
                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "介绍",
                    "args": [
                    ],
                },
            ],
            "repr": "id",
        },  # 流量包
        {
            "table": "Cardpack",
            "api": 1,
            "zh": "卡流量包",
            "crud":['post','put','delete'],
            "parents": [
                {
                    "name": "Card",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "卡id",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "iccid",
                            "type": "str",
                            "mean": "卡iccid"
                        },
                    ],
                },
                {
                    "name": "Pack",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "类型id",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "套餐名"
                        },
                    ],
                },

            ],
            "many": [
            ],
            "args": [
                {
                    "name": "status",
                    "type": "bool",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "激活状态",
                    "filter": "precise",
                },
                {
                    "name": "end_date",
                    "type": "date",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "到期时间",
                    "filter": "precise",
                    "sorter": 1,
                },
            ],
            "repr": "id",
        },  # 流量包
    ],
    "routes": [

        {
            "path": "args",  # 上级目录主菜单详情
            "name": "演示接口",
            "icon": "",  # ant的菜单图标，图标列表[]
            "components": [
                {
                    "module": "protable",
                    "table": "Pack",
                },
                {
                    "module": "protable",
                    "table": "Cardpack",
                },

            ],
        },
        {
            "path": "abc",  # 上级目录主菜单详情
            "name": "全部演示接口",
            "icon": "",  # ant的菜单图标，图标列表[]
            "components": "all",
        },

    ],

}



