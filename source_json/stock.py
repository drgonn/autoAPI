project_json = {
    "app":"stock",                  #文件源，app名
    "dataname":"stock",                   #数据库名称
    "datapassword":"7811175yy",
    "host":"http://localhost:8001",                             #文档中的域名地址
    "testhost":"localhost",                             #  test开头的都被用在postman当中做测试
    "testport":"8001",                             #
    "testprotocol":"http",                             #
    "auth":None,                             #
    "Flask_APScheduler":{             #flask-apscheduler 的定时任务设置
        "jobs":[],
    },
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
            "table":"Stock",
            "api":1,
            "zh": "股票",
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
                {
                    "name": "symbol",
                    "type": "str",
                    "length": "16",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "六位代号",
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
                    "name": "name",
                    "type": "str",
                    "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "名称",
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
                {
                    "name": "industry",
                    "type": "str",
                    "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "行业",
                },
                {
                    "name": "fullname",
                    "type": "str",
                    "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "全名",
                },
                {
                    "name": "enname",
                    "type": "str",
                    "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "英文名",
                },
                {
                    "name": "market",
                    "type": "str",
                    "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "交易板块",
                },
                {
                    "name": "exchange",
                    "type": "str",
                    "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "交易所代码",
                },
                {
                    "name": "curr_type",
                    "type": "str",
                    "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "交易货币",
                },
                {
                    "name": "list_status",
                    "type": "str",
                    "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "上市状态： L上市 D退市 P暂停上市",
                },
                {
                    "name": "list_date",
                    "type": "str",
                    "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "上市日期",
                },
                {
                    "name": "delist_date",
                    "type": "str",
                    "length": "64",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "退市日期",
                },
                {
                    "name": "is_hs",
                    "type": "str",
                    "length": "8",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "是否沪深港通标的",
                },
                {
                    "name": "price",
                    "type": "float",
                    "need": 1,  # 创建时候可以填写的参数
                    "postmust": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "现价",
                },
            ],
            "repr":"name",
        },                  #stock

    ]
}







