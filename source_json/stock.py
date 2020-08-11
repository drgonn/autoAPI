project_json = {
    "app":"stock",                  #文件源，app名
    "dataname":"stock",                   #数据库名称
    "datapassword":"781117",
    "host":"http://localhost:8001",                             #文档中的域名地址
    "testhost":"localhost",                             #
    "testport":"8001",                             #
    "testprotocol":"http",                             #
    "blues":[
            {
                "name":"apiv1",
                "address":"/api/v1/stock",      #其中一个api接口
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
            "default":"'stock'",
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
            "table":"Province",
            "api":1,
            "zh": "省",
            "parents":[
            ],
            "args":[
                {
                    "name":"ts_code",
                    "type":"str",
                    "length":"16",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique":1,
                    "mean": "代号",
                    "args":[
                    ],
                },
            ],
            "repr":"name",
        },                  #stock

    ]
}







