project_json = {
    "app":"stock",                  #文件源，app名
    "dataname":"stock",                   #数据库名称
    "datapassword":"7811175yy",
    "host":"http://localhost:8001",                             #文档中的域名地址
    "testhost":"localhost",                             #  test开头的都被用在postman当中做测试
    "testport":"8001",                             #
    "testprotocol":"http",                             #
    "anturl":"http://localhost:8888",                               #ant前端访问地址
    "anthost":"localhost",                             #  ant 调试访问地址
    "antport":"8888",                             #ant 调试访问地址
    "antprotocol":"http",                         #ant 调试访问地址
    "user_url":'http://localhost:20216/api/v3/user',
    "auth":1,                             #
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
                    "name":"name",
                    "type":"str",
                    "length":"64",

                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique":1,
                    "mean": "用户名",
                    "args":[
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
            "repr":"name",
        },                  #User
        {
            "table":"Stock",
            "api":1,
            "zh": "股票",
            "crud":[],
            "parents":[
            ],
            "many":[
                {
                    "name": "Group",
                    "w_model":1,         # 表示用以写model的一方
                    "add_api": 1,       # true时 api 接口当中的put  写上添加对方的ids。
                },
            ],
            "args":[
                {
                    "name":"ts_code",
                    "type":"str",
                    "length":"16",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique":1,
                    "mean": "代号",
                    "filter" : "like",
                    "args":[
                        {
                            "name": "index",
                            "value": "True",
                        }
                    ],
                },
                {
                    "name": "symbol",
                    "type": "str",
                    "length": "16",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "六位代号",
                    # "filter" : "precise",
                    "filter" : "like",
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

                    "post": 2,  # 创建时候必须填写的参数
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

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "地区",
                },
                {
                    "name": "industry",
                    "type": "str",
                    "length": "64",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "sorter": 1,
                    "mean": "行业",
                },
                {
                    "name": "fullname",
                    "type": "str",
                    "length": "64",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "全名",
                },
                {
                    "name": "enname",
                    "type": "str",
                    "length": "64",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "英文名",
                },
                {
                    "name": "market",
                    "type": "str",
                    "length": "64",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "交易板块",
                },
                {
                    "name": "exchange",
                    "type": "str",
                    "length": "64",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "交易所代码",
                },
                {
                    "name": "curr_type",
                    "type": "str",
                    "length": "64",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "交易货币",
                },
                {
                    "name": "list_status",
                    "type": "str",
                    "length": "64",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "上市状态： L上市 D退市 P暂停上市",
                },
                {
                    "name": "list_date",
                    "type": "date",
                    "length": "64",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "上市日期",
                    "sorter": 1,
                },
                {
                    "name": "delist_date",
                    "type": "date",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "退市日期",
                },
                {
                    "name": "is_hs",
                    "type": "str",
                    "length": "8",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "是否沪深港通标的",
                },
                {
                    "name": "price",
                    "type": "float",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "现价",
                    "sorter": 1,
                },
                {
                    "name": "circ_mv",
                    "type": "float",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "流通市值（万元）",
                    "sorter": 1,
                },
                {
                    "name": "pe",
                    "type": "float",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "市盈率（总市值/净利润，亏损的PE为空）",
                    "sorter": 1,
                },
                {
                    "name": "score",
                    "type": "float",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "评分",
                    "sorter": 1,
                },
            ],
            "repr":"name",
        },                  #stock
        {
            "table":"Index",
            "api":1,
            "zh": "指数",
            "crud":['put','delete'],
            "parents":[
            ],
            "many":[
            ],
            "args":[
                {
                    "name":"ts_code",
                    "type":"str",
                    "length":"16",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique":1,
                    "mean": "代号",
                    "filter" : "like",
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
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "名称",
                    "filter": "like",
                },
                {
                    "name": "market",
                    "type": "str",
                    "length": "16",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "市场",
                },
                {
                    "name": "publisher",
                    "type": "str",
                    "length": "64",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "sorter": 1,
                    "mean": "发布方",
                },

                {
                    "name": "category",
                    "type": "str",
                    "length": "64",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "指数类别",
                },
                {
                    "name": "base_date",
                    "type": "date",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "基期",
                },
                {
                    "name": "base_point",
                    "type": "str",
                    "length": "64",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "基点",
                },
                {
                    "name": "list_date",
                    "type": "date",
                    "length": "64",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "发布日期",
                    "sorter": 1,
                },
                {
                    "name": "about",
                    "type": "text",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "描述",
                },
            ],
            "repr":"name",
        },                  #index指数
        {
            "table":"Indexday",
            "api":1,
            "zh": "指数日行情",
            # "crud":[],
            "crud":['post','put','delete'],
            "parents":[
                {
                    "name": "Index",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "日数据id",
                    "show": [        #放在api当中显示的参数
                        {
                            "name":"name",
                            "type": "str",
                            "mean":"指数名"
                        },
                    ],
                },
            ],
            "args":[
                {
                    "name": "trade_date",
                    "type": "date",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "交易日期",
                    "sorter": 1,
                },
                {
                    "name": "score",
                    "type": "float",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "评分",
                    "sorter": 1,
                },
                {
                    "name": "close",
                    "type": "float",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "当日收盘价",
                },
                {
                    "name": "pct_chg",
                    "type": "float",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "涨跌幅（%）",
                },
                {
                    "name": "vol",
                    "type": "float",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "成交量（手）",
                },

                {
                    "name": "amount",
                    "type": "float",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "成交额（千元）",
                },
            ],
            "repr":"trade_date",
        },                  #每日指标
        {
            "table":"Day",
            "api":1,
            "zh": "日行情",
            "crud":['post','put','delete'],
            "parents":[
                {
                    "name": "Stock",
                    "index": "id",
                    "type": "int",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "日数据id",
                    "show": [        #放在api当中显示的参数
                        {
                            "name":"name",
                            "type": "str",
                            "mean":"股名"
                        },
                    ],
                },
                {
                    "name": "Group",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "分组id",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "分组名"
                        },
                    ],
                },
            ],
            "args":[
                {
                    "name": "trade_date",
                    "type": "date",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "交易日期",
                    "sorter": 1,
                },
                {
                    "name": "score",
                    "type": "float",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "评分",
                    "sorter": 1,
                },
                {
                    "name": "close",
                    "type": "float",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "当日收盘价",
                },
                {
                    "name": "pct1",
                    "type": "float",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "单日涨幅",
                    "sorter": 1,
                },
                {
                    "name": "pct3",
                    "type": "float",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "3日涨幅",
                    "sorter": 1,
                },
                {
                    "name": "pct5",
                    "type": "float",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "5日涨幅",
                    "sorter": 1,
                },
                {
                    "name": "pct10",
                    "type": "float",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "10日涨幅",
                    "sorter": 1,
                },
                {
                    "name": "pct20",
                    "type": "float",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "20日涨幅",
                    "sorter": 1,
                },
                {
                    "name": "turnover_rate",
                    "type": "float",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "换手率（%）",
                },

                {
                    "name": "turnover_rate_f",
                    "type": "float",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "换手率（自由流通股）",
                },
                {
                    "name": "volume_ratio",
                    "type": "float",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "量比",
                },
                {
                    "name": "pe",
                    "type": "float",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "市盈率（总市值/净利润，亏损的PE为空）",
                },

                {
                    "name": "pe_ttm",
                    "type": "float",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "市盈率（TTM，亏损的PE为空）",
                },

                {
                    "name": "pb",
                    "type": "float",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "市净率（总市值/净资产）",
                },

                {
                    "name": "ps",
                    "type": "float",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "市销率",
                },

                {
                    "name": "ps_ttm",
                    "type": "float",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "市销率（TTM）",
                    "sorter": 1,
                },

                {
                    "name": "dv_ratio",
                    "type": "float",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "股息率（%）",
                    "sorter": 1,
                },

                {
                    "name": "dv_ttm",
                    "type": "float",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "股息率（TTM）（%）",
                    "sorter": 1,
                },

                {
                    "name": "total_share",
                    "type": "float",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "总股本（万股）",
                    "sorter": 1,
                },

                {
                    "name": "float_share",
                    "type": "bigint",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "流通股本（万股）",
                    "sorter": 1,
                },

                {
                    "name": "free_share",
                    "type": "float",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "自由流通股本（万）",
                    "sorter": 1,
                },

                {
                    "name": "total_mv",
                    "type": "float",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "总市值（万元）",
                    "sorter": 1,
                },
                {
                    "name": "circ_mv",
                    "type": "float",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "流通市值（万元）",
                    "sorter": 1,
                },
            ],
            "repr":"trade_date",
        },                  #每日行情
        {
            "table":"Score_type",
            "api":1,
            "zh": "得分类型",
            "crud":['post','put','delete'],
            "parents":[
            ],
            "args":[
                {
                    "name": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "ID",
                    "sorter": 1,
                },
                {
                    "name": "name",
                    "type": "str",
                    "length":"64",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "名",
                    "sorter": 1,
                },
                {
                    "name": "weight",
                    "type": "float",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "权重",
                    "sorter": 1,
                },
                {
                    "name": "about",
                    "type": "text",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "描述",
                    "sorter": 1,
                },
            ],
            "repr":"name",
        },                  #得分类型
        {
            "table":"Score",
            "api":1,
            "zh": "得分",
            "crud":['post','put','delete'],
            "parents":[
                {
                    "name": "Stock",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "股票id",
                    "show": [        #放在api当中显示的参数
                        {
                            "name":"name",
                            "type": "str",
                            "mean":"股名"
                        },
                        {
                            "name": "id",
                            "type": "int",
                            "mean": "ID"
                        },
                    ],
                },
                {
                    "name": "Score_type",
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
                            "mean": "类型名"
                        },
                    ],
                },
            ],
            "args":[
                {
                    "name": "trade_date",
                    "type": "date",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "日期",
                    "filter": "precise",
                    "sorter": 1,
                },
                {
                    "name": "score",
                    "type": "float",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "评分",
                    "sorter": 1,
                },
            ],
            "repr":"trade_date",
        },                  #得分数据

        {
            "table": "Group",
            "api": 1,
            "zh": "自选",
            "crud":['post','put','delete'],
            "parents": [
            ],
            "many":[
                {
                    "name": "Stock",
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
                    "mean": "名称",
                    "filter": "like",
                },
                {
                    "name": "type",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "分组类型",
                    "filter": "precise",
                    "mapping": [
                        {'key':1,'value':"自选"},
                        {'key':2,'value':"行业"},
                        {'key':3,'value':"概念"},
                    ],
                },
            ],
            "repr": "name",
        },  # 自选分组
    ],
    "routes":[
        {
            "path": "stock",   #上级目录主菜单详情
            "name": "股票详情",
            "icon":"",       #ant的菜单图标，图标列表[]
            "components": [
                {
                    "module":"protable",
                    "table": "Stock",
                },
                {
                    "module": "protable",
                    "table": "Group",
                },
                {
                    "module": "protable",
                    "table": "Score",
                },
                {
                    "module":"protable",
                    "table": "Day",
                },
                {
                    "module":"protable",
                    "table": "Index",
                },
                {
                    "module": "protable",
                    "table": "Indexday",
                },
            ],
        },
        {
            "path": "arg",  # 上级目录主菜单详情
            "name": "设置",
            "icon": "",  # ant的菜单图标，图标列表[]
            "components": [
                {
                    "module": "protable",
                    "table": "Score_type",
                },
            ],
        },
    ],
}







