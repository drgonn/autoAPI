project_json = {
    "app":"oee",                  #文件源，app名
    "dataname":"oee",                   #数据库名称
    "mean":"智能点胶系统",
    "datapassword":"7811175yy",
    "host":"http://localhost:8002",                             #文档中的域名地址
    "testhost":"localhost",                             #  test开头的都被用在postman当中做测试
    "testport":"8002",                             #
    "testprotocol":"http",                             #
    # "anturl":"http://localhost:8002",                               #ant前端访问地址
    "anthost":"localhost",                             #  ant 调试访问地址
    "antport":"8705",                             #ant 调试访问地址
    "antprotocol":"http",                         #ant 调试访问地址
    "auth":1 ,                             #  是否有用户系统
    "user_url":'http://localhost:20216/api/v3/user',
    "login_about":"数据采集边缘计算产品与OEE,试用账号：18666821287，密码：123123",              #登录界面描述
    "login_title":"marco",                             #登录界面标题
    "produce":"MARCO(北京)自动控制系统开发有限公司出品",                             #出品
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
            "table":"User",
            "api":False,
            "zh": "用户",
            "crud":['post','put','delete'],
            "parents":[
            ],
            "args":[
                {
                    "name":"uid",
                    "type":"str",
                    "length":"64",
                    "mean": "UID",
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
                    "mean": "注册时间",
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
            "table":"Device",
            "api":1,
            "zh": "机器",
            "crud":['post','put','delete'],
            "parents":[
            ],
            "args":[
                {
                    "name":"sn",
                    "type":"str",
                    "length":"16",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique":1,
                    "mean": "编号",
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

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "名称",
                    "filter": "like",
                },
                {
                    "name": "type",
                    "type": "str",
                    "length": "64",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "filter": "precise",
                    "corres": [
                        {'key': 1, 'value': "三轴"},
                        {'key': 2, 'value': "五轴"},
                    ],
                    "mean": "类型",
                },

            ],
            "repr":"name",
        },                  #机台
        {
            "table":"Worktime",
            "api":1,
            "zh": "机台工作时间",
            "crud":['post','put','delete'],
            "parents":[
                {
                    "name": "Device",
                    "index": "id",
                    "type": "int",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "机台id",
                    "show": [        #放在api当中显示的参数
                        {
                            "name":"name",
                            "type": "str",
                            "mean":"设备名"
                        },
                    ],
                },
            ],
            "args":[
                {
                    "name": "start_time",
                    "type": "time",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "开始时间",
                },
                {
                    "name": "end_time",
                    "type": "time",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "结束时间",
                },
                {
                    "name": "seconds",
                    "type": "int",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "运行时间（秒）",
                },
                {
                    "name": "type",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "时间类型",
                    "filter": "precise",
                    "corres": [
                        {'key': 1, 'value': "休息时间"},
                        {'key': 2, 'value': "日常管理时间"},
                        {'key': 5, 'value': "计划停止时间"},
                        {'key': 6, 'value': "日常管理时间"},
                        {'key': 3, 'value': "停机时间"},
                        {'key': 4, 'value': "运转时间"},
                    ],
                },
                {
                    "name": "amount",
                    "type": "int",
                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "加工数量",
                },
                {
                    "name": "good",
                    "type": "int",
                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "良品数量",
                },
                {
                    "name": "glue",
                    "type": "float",
                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "使用胶量",
                },
            ],
            "repr":"id",
        },                  #worktime
        {
            "table":"Valvetime",
            "api":1,
            "zh": "阀工作时间",
            "crud":['post','put','delete'],
            "parents":[
                {
                    "name": "Device",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "机台id",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "机台名"
                        },
                    ],
                },
                {
                    "name": "Valve",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "阀id",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "阀名"
                        },
                        {
                            "name": "sn",
                            "type": "str",
                            "mean": "阀序列号"
                        },
                    ],
                },
            ],
            "args":[
                {
                    "name": "start_time",
                    "type": "time",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "开始时间",
                },
                {
                    "name": "end_time",
                    "type": "time",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "结束时间",
                },
                {
                    "name": "seconds",
                    "type": "float",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "运行时间（秒）",
                },
                {
                    "name": "volt",
                    "type": "float",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "工作电压（v）",
                },
                {
                    "name": "amount",
                    "type": "int",
                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "加工数量",
                },
                {
                    "name": "good",
                    "type": "int",
                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "良品数量",
                },
                {
                    "name": "glue",
                    "type": "float",
                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "使用胶量",
                },
            ],
            "repr":"id",
        },                  #阀工作时间
        {
            "table": "Valvetype",
            "api": 1,
            "zh": "阀类型",
            "crud": ['post', 'put', 'delete'],
            "parents": [
            ],
            "args": [
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
            ],
            "repr": "id",
        },  # 阀类型
        {
            "table": "Valve",
            "api": 1,
            "zh": "点胶阀",
            "crud": ['post', 'put', 'delete'],
            "parents": [
                {
                    "name": "Valvetype",
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
                {
                    "name": "Device",
                    "index": "id",
                    "type": "int",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "设备id",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "设备名"
                        },
                    ],
                },
            ],
            "args": [
                {
                    "name": "sn",
                    "type": "str",
                    "length": "16",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "编号",
                    "filter": "like",  # precise为精确查找，like，模糊查找
                    "args": [
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
            ],
            "repr": "id",
        },  # 阀

        {
            "table": "Bug",
            "api": 1,
            "zh": "故障",
            "crud": ['post', 'put', 'delete'],
            "parents": [
                {
                    "name": "Device",
                    "index": "id",
                    "type": "int",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "设备id",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "设备名"
                        },
                    ],
                },
                {
                    "name": "Bugtype",
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
            "args": [
                {
                    "name": "reason",
                    "type": "text",

                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "原因",
                    "filter": "like",
                },

                {
                    "name": "start_time",
                    "type": "time",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "时间",
                },
                {
                    "name": "end_time",
                    "type": "time",

                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "修好时间",
                },
            ],
            "repr": "id",
        },  #  故障
        {
            "table": "Bugtype",
            "api": 1,
            "zh": "故障类型",
            "crud": ['post', 'put', 'delete'],
            "parents": [
            ],
            "args": [
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
                    "name": "sn",
                    "type": "str",
                    "length": "64",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "代码",
                    "filter": "like",
                },
                {
                    "name": "about",
                    "type": "text",
                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "描述",
                },
            ],
            "repr": "id",
        },  # 故障类型
        {
            "table": "Alarmtype",
            "api": 1,
            "zh": "报警",
            "crud": ['post', 'put', 'delete'],
            "parents": [
            ],
            "args": [
                {
                    "name": "code",
                    "type": "str",
                    "length": "64",
                    "post": 2,  # 创建时候必须填写的参数int
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "报警代码",
                    "args": [
                    ],
                },
                {
                    "name": "mean",
                    "type": "text",
                    "post": 1,  # 创建时候必须填写的参数int
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "含义",
                    "args": [
                    ],
                },
                {
                    "name": "cause",
                    "type": "text",
                    "post": 1,  # 创建时候必须填写的参数int
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "可能原因",
                    "args": [
                    ],
                },
                {
                    "name": "solution",
                    "type": "text",
                    "post": 1,  # 创建时候可以填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "解决方案",
                    "args": [
                    ],
                },
            ],
            "repr": "code",
        },  # 报警类型
        {
            "table": "Alarm",
            "api": 1,
            "zh": "报警",
            "crud": ['post', 'put', 'delete'],
            "parents": [
                {
                    "name": "Alarmtype",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "阀id",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "code",
                            "type": "str",
                            "mean": "代码"
                        },
                        {
                            "name": "mean",
                            "type": "str",
                            "mean": "含义"
                        },
                        {
                            "name": "cause",
                            "type": "str",
                            "mean": "可能原因"
                        },
                        {
                            "name": "solution",
                            "type": "str",
                            "mean": "解决方案"
                        },
                    ],
                },
                {
                    "name": "Valve",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "阀id",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "阀名"
                        },
                        {
                            "name": "id",
                            "type": "int",
                            "mean": "id"
                        },
                    ],
                },
                {
                    "name": "Device",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "机台id",
                },
            ],
            "args": [
                {
                    "name": "create_time",
                    "type": "time",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.now",
                        },
                    ],
                },
            ],
            "repr": "id",
        },  # 报警



        {
            "table": "Project",
            "api": 1,
            "zh": "项目分类",
            "crud": ['post', 'put', 'delete'],
            "parents": [
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "256",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "工作事项",
                    "filter": "like",
                },

            ],
            "repr": "name",
        },  # 项目名
        {
            "table": "Plan",
            "api": 1,
            "zh": "项目进度",
            "crud": ['post', 'put', 'delete'],
            "parents": [
                {
                    "name": "Project",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "项目id",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "项目名"
                        },
                    ],
                },
                {
                    "name": "User",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "用户id",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "用户名"
                        },
                    ],
                },
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "256",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "工作事项",
                    "filter": "like",
                },
                {
                    "name": "week",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "周",
                    "filter": "precise",
                },
                {
                    "name": "current",
                    "type": "text",
                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "当前进度及完成情况",
                    "args": [
                    ],
                },
                {
                    "name": "follow",
                    "type": "text",
                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "后续计划",
                    "args": [
                    ],
                },

                {
                    "name": "time",
                    "type": "time",
                    "mean": "提交时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.utcnow",
                        },
                    ],
                },

            ],
            "repr": "id",
        },  # 项目计划
    ],
    "routes":[
        {
            "path": "oee",   #上级目录主菜单详情
            "name": "OEE时间分析",
            "icon":"",       #ant的菜单图标，图标列表[]
            "components": [
                {
                    "module":"protable",
                    "table": "Device",
                },
                {
                    "module":"protable",
                    "table": "Worktime",
                },
                {
                    "module": "protable",
                    "table": "Valve",
                },
                {
                    "module":"protable",
                    "table": "Valvetime",
                },


            ],
        },
        {
            "path": "warn",  # 上级目录主菜单详情
            "name": "故障报警",
            "icon": "",  # ant的菜单图标，图标列表[]
            "components": [
                {
                    "module": "protable",
                    "table": "Bug",
                },
                {
                    "module": "protable",
                    "table": "Alarm",
                },
            ],
        },
        {
            "path": "plan",  # 上级目录主菜单详情
            "name": "项目管理",
            "icon": "",  # ant的菜单图标，图标列表[]
            "components": [
                {
                    "module": "protable",
                    "table": "Plan",
                },
                {
                    "module": "protable",
                    "table": "Project",
                },
            ],
        },
        {
            "path": "arg",  # 上级目录主菜单详情
            "name": "参数设置",
            "icon": "",  # ant的菜单图标，图标列表[]
            "components": [
                {
                    "module": "protable",
                    "table": "Valvetype",
                },
                {
                    "module": "protable",
                    "table": "Bugtype",
                },

                {
                    "module": "protable",
                    "table": "Alarmtype",
                },
            ],
        },
        # {
        #     "path": "user_system",  # 上级目录主菜单详情
        #     "name": "用户管理",
        #     "icon": "",  # ant的菜单图标，图标列表[]
        #     "components": [
        #         {
        #             "module": "protable",
        #             "table": "User",
        #         },
        #         {
        #             "module": "protable",
        #             "table": "Role",
        #         },
        #         {
        #             "module": "protable",
        #             "table": "Userlog",
        #         },
        #
        #     ],
        # }
    ],
}







