project_json = {
    "app":"oee",                  #文件源，app名
    "dataname":"oee",                   #数据库名称
    "datapassword":"7811175yy",
    "host":"http://localhost:8002",                             #文档中的域名地址
    "testhost":"localhost",                             #  test开头的都被用在postman当中做测试
    "testport":"8002",                             #
    "testprotocol":"http",                             #
    # "anturl":"http://localhost:8002",                               #ant前端访问地址
    "anthost":"localhost",                             #  ant 调试访问地址
    "antport":"8801",                             #ant 调试访问地址
    "antprotocol":"http",                         #ant 调试访问地址
    "auth":None,                             #
    "sql":{                    #数据库详情
        "sql": "mysql",
        "host": "localhost",
        "name" :   'root',
        "pwd" :  '7811175yy',
        "port": 3306,
    },
    # "Flask_APScheduler":{             #flask-apscheduler 的定时任务设置
    #     "jobs":[],
    # },
    "blues":[
            {
                "name":"apiv1",
                "address":"/api/v1/oee",      #其中一个api接口
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
            "default":"'7811175yy'",
        },
        {
            "arg":"SQL_HOST",
            "default":"'127.0.0.1:3306'",
        },
        {
            "arg":"SQL_DATABASE",
            "default":"'oee'",
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
            "table":"Device",
            "api":1,
            "zh": "设备",
            "crud":['post'],
            "parents":[
            ],
            "args":[
                {
                    "name":"symbol",
                    "type":"str",
                    "length":"16",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique":1,
                    "mean": "代号",
                    "filter" : "like",       # precise为精确查找，like，模糊查找
                    "args":[
                        {
                            "name": "index",
                            "value": "True",
                        }
                    ],
                },
                {
                    "name": "name",
                    "type": "str",
                    "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "名称",
                    "filter": "like",
                },
                {
                    "name": "area",
                    "type": "str",
                    "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "地区",
                },

            ],
            "repr":"name",
        },                  #oee
        {
            "table":"Work",
            "api":1,
            "zh": "工作内容",
            "crud":[],
            "parents":[
                {
                    "name": "Device",
                    "index": "id",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "设备id",
                    "show": [        #放在api当中显示的参数
                        {
                            "name":"name",
                            "type": "str",
                            "mean":"股名"
                        },
                    ],
                },
            ],
            "args":[
                {
                    "name": "start_time",
                    "type": "time",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "开始时间",
                },
                {
                    "name": "end_time",
                    "type": "time",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "结束时间",
                },
                {
                    "name": "seconds",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "运行时间（秒）",
                },
                {
                    "name": "type",
                    "type": "int",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "工作类型",
                },

            ],
            "repr":"id",
        },                  #每日数据

    ],
    "routes":[
        {
            "path": "oee",   #上级目录主菜单详情
            "name": "股票详情",
            "icon":"",       #ant的菜单图标，图标列表[]
            "components": [
                {
                    "module":"protable",
                    "table": "Device",
                },
                {
                    "module":"protable",
                    "table": "Work",
                },

            ],
        }
    ],
}







