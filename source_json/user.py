project_json = {
    "app":"user",                  #文件源，app名
    "dataname":"user",                   #数据库名称
    "mean":"用户系统",
    "datapassword":"7811175yy",
    "host":"http://localhost:8003",                             #文档中的域名地址
    "testhost":"localhost",                             #  test开头的都被用在postman当中做测试
    "testport":"8003",                             #
    "testprotocol":"http",                             #
    # "anturl":"http://localhost:8002",                               #ant前端访问地址
    "anthost":"localhost",                             #  ant 调试访问地址
    "antport":"8605",                             #ant 调试访问地址
    "antprotocol":"http",                         #ant 调试访问地址
    "auth":False ,                             #  是否有用户系统
    "user_url":'http://localhost:20216/api/v3/user',
    "login_about":"数据采集边缘计算产品与OEE,试用账号：18666821287，密码：123123",              #登录界面描述
    "login_title":"用户系统",                             #登录界面标题
    "produce":"东达科技出品",                             #出品
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
                "address":"/api/v1/user",      #其中一个api接口
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
            "default":"'user'",
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
            "table":"Group",
            "api":1,
            "zh": "部门",
            "crud":['post','put','delete'],
            "many":[
            ],
            "parents":[
            ],
            "args":[
                {
                    "name":"name",
                    "type":"str",
                    "length":"64",
                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique":1,
                    "mean": "名",
                    "args":[
                    ],
                },
                {
                    "name":"permission",
                    "type":"text",
                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique":1,
                    "mean": "权限",
                    "args":[
                    ],
                },
                {
                    "name":"about",
                    "type":"text",
                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique":1,
                    "mean": "描述",
                    "args":[
                    ],
                },
            ],
            "repr":"name",
        },  # 部门
        # {
        #     "table":"Permission",
        #     "api":1,
        #     "zh": "权限",
        #     "crud":['post','put','delete'],
        #     "many":[
        #         # {
        #         #     "name": "Group",
        #         #     "add_api": 1,       # true时 api 接口当中的put  写上添加对方的ids。
        #         # },
        #     ],
        #     "parents":[
        #     ],
        #     "args":[
        #         {
        #             "name":"name",
        #             "type":"str",
        #             "length":"64",
        #             "post": 1,  # 创建时候必须填写的参数
        #             "putneed": 1,  # 修改时可以修改的参数
        #             "listmust": 0,  # 请求列表必须post的参数
        #             "unique":1,
        #             "mean": "名",
        #             "args":[
        #             ],
        #         },
        #         {
        #             "name":"about",
        #             "type":"text",
        #             "post": 1,  # 创建时候必须填写的参数
        #             "putneed": 1,  # 修改时可以修改的参数
        #             "listmust": 0,  # 请求列表必须post的参数
        #             "unique":1,
        #             "mean": "描述",
        #             "args":[
        #             ],
        #         },
        #     ],
        #     "repr":"name",
        # },  # permission
        {
            "table":"Role",
            "api":1,
            "zh": "角色",
            "crud":['post','put','delete'],
            "many":[
            ],
            "parents":[
                {
                    "name": "Group",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "部门id",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "部门名"
                        },
                    ],
                },
            ],
            "args":[
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
                    "name": "permission",
                    "type": "text",
                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "权限",
                    "args": [
                    ],
                },
                {
                    "name": "about",
                    "type": "text",
                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "描述",
                    "args": [
                    ],
                },
            ],
            "repr":"name",
        },  # role
        {
            "table": "User",
            # "api": False,
            "api": True,
            "zh": "用户",
            "crud": ['post', 'put', 'delete'],
            "parents": [
                {
                    "name": "Role",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "角色id",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "角色名"
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
                    "mean": "部门id",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "部门名"
                        },
                    ],
                },
            ],
            "args": [
                {
                    "name": "uid",
                    "type": "str",
                    "length": "64",
                    "mean": "UID",
                    "args": [
                        {
                            "name": "unique",
                            "value": "True",
                        },
                        {
                            "name": "index",
                            "value": "True",
                        },
                        {
                            "name": "nullable",
                            "value": "False",
                        },
                    ],
                },
                {
                    "name": "name",
                    "type": "str",
                    "length": "64",

                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "用户名",
                    "args": [
                    ],
                },
                {
                    "name": "phone",
                    "type": "str",
                    "length": "64",

                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "手机",
                    "args": [
                    ],
                },
                {
                    "name": "email",
                    "type": "str",
                    "length": "64",

                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "邮箱",
                    "args": [
                    ],
                },
                {
                    "name": "emailbind",
                    "type": "bool",
                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "邮箱是否绑定",
                    "args": [
                    ],
                    "corres": [
                        {'key': 1, 'value': "已绑定"},
                        {'key': 0, 'value': "未绑定"},
                    ],
                },
                {
                    "name": "company",
                    "type": "str",
                    "length": "64",

                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "公司",
                    "args": [
                    ],
                },
                {
                    "name": "address",
                    "type": "str",
                    "length": "64",

                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "地址",
                    "args": [
                    ],
                },
                {
                    "name": "url",
                    "type": "str",
                    "length": "128",

                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "网址",
                    "args": [
                    ],
                },
                {
                    "name": "nickname",
                    "type": "str",
                    "length": "64",

                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "微信昵称",
                    "args": [
                    ],
                },
                {
                    "name": "headimgurl",
                    "type": "str",
                    "length": "256",

                    "post": 0,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "微信头像地址",
                    "args": [
                    ],
                },
                {
                    "name": "createDate",
                    "type": "time",
                    "mean": "注册时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.utcnow",
                        },
                    ],
                },
            ],
            "repr": "name",
        },  # User
        {
            "table": "Userlog",
            "api": 1,
            "zh": "用户日志",
            "crud": ['delete','put','post'],
            "parents": [
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
                    "name": "ip",
                    "type": "str",
                    "length": "64",

                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "IP",
                    "args": [
                    ],
                },
                {
                    "name": "user_agent",
                    "type": "str",
                    "length": "1024",

                    "post": 0,  # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "agent",
                    "args": [
                    ],
                },
                {
                    "name": "msg",
                    "type": "text",

                    "post": 0,  # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "msg",
                    "args": [
                    ],
                },
                {
                    "name": "time",
                    "type": "time",
                    "mean": "登录时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.utcnow",
                        },
                    ],
                },
            ],
            "repr": "name",
        },  # Userlog

    ],
    "routes":[
        {
            "path": "user",   #上级目录主菜单详情
            "name": "OEE时间分析",
            "icon":"",       #ant的菜单图标，图标列表[]
            "components": [
                {
                    "module":"protable",
                    "table": "Group",
                },
                {
                    "module": "protable",
                    "table": "User",
                },
            ],
        },
        # {
        #     "path": "user",  # 上级目录主菜单详情
        #     "name": "用户管理",
        #     "icon": "",  # ant的菜单图标，图标列表[]
        #     "components": [
        #         {
        #             "module": "protable",
        #             "table": "Role",
        #         },
        #         {
        #             "module": "protable",
        #             "table": "Userlog",
        #         },
        #     ],
        # },
        {
            "path": "abc",  # 上级目录主菜单详情
            "name": "全部演示接口",
            "icon": "",  # ant的菜单图标，图标列表[]
            "components": "all",
        },
    ],
}







