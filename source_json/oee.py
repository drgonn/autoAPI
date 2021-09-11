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
    "login_about":"智能点胶系统（SDS）,试用账号：18666821287，密码：123123",              #登录界面描述
    "login_title":"MARCO",                             #登录界面标题
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
            "table":"Project",
            "api":1,
            "zh": "项目名",
            "parents":[
            ],
            "args":[
                {
                    "name":"name",
                    "type":"str",
                    "length":"64",
                    "post": 2,  # 创建时候必须填写的参数
                    "put": 1,  # 修改时可以修改的参数
                    "list": 0,  # 请求列表必须post的参数
                    "mean": "项目名",
                    "args":[
                    ],
                },
                {
                    "name":"zh_name",
                    "type":"str",
                    "length":"64",
                    "post": 2,  # 创建时候必须填写的参数
                    "put": 1,  # 修改时可以修改的参数
                    "list": 0,  # 请求列表必须post的参数
                    "mean": "项目名",
                    "args":[
                    ],
                },
            ],
            "repr":"name",
        },                  #项目名
        {
            "table":"Table",
            "api":1,
            "zh": "表",
            "repr":"name",
            "parents":[
                {
                    "name": "Project",
                    "index": "id",
                    "type": "int",
                    "post": 1,  # 创建时候可以填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "项目id",
                },
            ],
            "args":[
                {
                    "name":"name",
                    "type":"str",
                    "length":"64",
                    "post": 1,  # 创建时候可以填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "表名",
                    "args":[
                    ],
                },
                {
                    "name":"zh",
                    "type":"str",
                    "length":"64",
                    "post": 1,  # 创建时候可以填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "中文表名",
                    "args":[
                    ],
                },
                {
                    "name": "url_prefix",
                    "type":"str",
                    "length":"128",
                    "post": 1,  # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "api前缀",
                    "args":[
                    ],
                },
                {
                    "name":"about",
                    "type":"text",
                    "length":"64",
                    "post": 1,  # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "about",
                    "args":[
                    ],
                },
            ],
        },                  #表
        {
            "table": "Column",
            "api": 1,
            "zh": "参数",
            "repr": "name",
            "parents": [
                {
                    "name": "Table",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "项目id",
                },
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "64",
                    "post": 1,  # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "表名",
                    "args": [
                    ],
                },
                {
                    "name": "type",
                    "type": "str",
                    "length": "64",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "表名",
                    "args": [
                    ],
                },
                {
                    "name": "length",
                    "type": "str",
                    "length": "64",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "表名",
                    "args": [
                    ],
                },
                {
                    "name": "postneed",
                    "type": "bool",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "表名",
                    "args": [
                        {
                            "name": "default",
                            "value": 1,
                        },
                    ],
                },
                {
                    "name": "postmust",
                    "type": "bool",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "表名",
                    "args": [
                        {
                            "name": "default",
                            "value": 0,
                        },
                    ],
                },
                {
                    "name": "putneed",
                    "type": "bool",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "表名",
                    "args": [
                        {
                            "name": "default",
                            "value": 0,
                        },
                    ],
                },
                {
                    "name": "listmust",
                    "type": "bool",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "表名",
                    "args": [
                        {
                            "name": "default",
                            "value": 0,
                        },
                    ],
                },
                {
                    "name": "like",
                    "type": "bool",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "表名",
                    "args": [
                        {
                            "name": "default",
                            "value": 0,
                        },
                    ],
                },
            ],
        },  # 表列
        {
            "table": "ColumnArg",
            "api": 1,
            "zh": "参数",
            "repr": "name",
            "parents": [
                {
                    "name": "Column",
                    "index": "id",
                    "type": "int",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "项目id",
                },
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "64",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "表名",
                    "args": [
                    ],
                },
                {
                    "name": "value",
                    "type": "str",
                    "length": "64",

                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "表名",
                    "args": [
                    ],
                },
            ],
        },  # 表列

    ],
    "routes":[
        {
            "path": "oee",   #上级目录主菜单详情
            "name": "OEE时间分析",
            "icon":"",       #ant的菜单图标，图标列表[]
            "components": [
                {
                    "module":"protable",
                    "table": "Project",
                },
            ],
        },

    ],
}







