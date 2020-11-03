project_json = {
    "app":"bridge",                  #文件源，app名
    "dataname":"bridge",                   #数据库名称
    "datapassword":"7811175yy",
    "host":"http://frp.sealan.tech:20303",                             #文档中的域名地址
    # "host":"http://localhost:20303",                             #文档中的域名地址
    "testhost":"frp.sealan.tech",                             #
    "testport":"20303",                             #
    "testprotocol":"http",                             #
    "anthost":"localhost",                             #  ant 调试访问地址
    "antport":"20305",                             #ant 调试访问地址
    "auth": 1,                                     #是否需要用户登录认证YY
    "user_url":'http://frp.sealan.tech:20216/api/v3/user',
    # "user_url":'http://localhost:20216/api/v3/user',
    "login_about":"智慧建筑监测系统,试用账号：18666821287，密码：123",              #登录界面描述
    "login_title":"智慧建筑",                             #登录界面标题
    "produce":"chenrong出品",                             #出品
    "sql":{                    #数据库详情
        "sql": "mysql",
        "host": "localhost",
        "name" :   'root',
        "pwd" :  '7811175yy',
        "port": 3306,
    },
    "antprotocol":"http",                         #ant 调试访问地址
    "blues":[
            {
                "name":"apiv1",
                "address":"/api/v1/bridge",      #其中一个api接口
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
                    # 创建时候可以填写的参数
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
            "table":"Province",
            "api":1,
            "zh": "省",
            "detail_sons":[
                "city"
            ],
            "crud":['post','put','delete'],
            "parents":[
            ],
            "args":[
                {
                    "name":"name",
                    "type":"str",
                    "length":"64",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique":1,
                    "mean": "省名",
                    "args":[
                    ],
                },
                {
                    "name": "code",
                    "type": "str",
                    "length": "64",
                    # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "行政编码",
                    "args": [
                    ],
                },
            ],
            "repr":"name",
        },                  #省
        {
            "table":"City",
            "api":1,
            "zh": "市",
            "crud":['post','put','delete'],
            "detail_sons":[
                "area"
            ],
            "parents":[
                {
                    "name": "Province",
                    "index": "id",
                    "type": "int",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "省份id",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "省名"
                        },
                    ],
                },
            ],
            "args":[
                {
                    "name":"name",
                    "type":"str",
                    "length":"64",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "市名",
                    "unique":1,
                    "args":[
                    ],
                },
                {
                    "name": "code",
                    "type": "str",
                    "length": "64",
                    # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "行政编码",
                    "args": [
                    ],
                },

            ],
            "repr":"name",
        },                  #市
        {
            "table":"Area",
            "api":1,
            "zh": "行政区",
            "crud":['post','put','delete'],
            "detail_sons":[
                "bridge"
            ],
            "parents":[
                {
                    "name": "City",
                    "index": "id",
                    "type": "int",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "市id",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "市名"
                        },
                    ],
                },
            ],
            "args":[
                {
                    "name":"name",
                    "type":"str",
                    "length":"64",
                    "unique":1,
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "行政区名",
                    "args":[
                    ],
                },
                {
                    "name": "code",
                    "type": "str",
                    "length": "64",
                    # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "unique": 1,
                    "mean": "行政编码",
                    "args": [
                    ],
                },

            ],
            "repr":"name",
        },                  #area
        {
            "table":"Basetype",
            "api":1,
            "zh": "基础类型",
            "crud":['post','put','delete'],
            "detail_sons":[
                "buildtype"
            ],
            "parents":[
            ],
            "args":[
                {
                    "name":"name",
                    "type":"str",
                    "length":"64",
                    "unique":1,
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "基础类名",
                    "args":[
                    ],
                },
            ],
            "repr":"name",
        },                  #基础类型
        {
            "table":"Buildtype",
            "api":1,
            "zh": "建筑种类",
            "crud":['post','put','delete'],
            "detail_sons":[
            ],
            "parents":[
                {
                    "name": "Basetype",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "建筑种类id",
                    "tojson": "name",  # 在json字段当中显示的参数
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "基础类型"
                        },
                        {
                            "name": "id",
                            "type": "int",
                            "mean": "id"
                        },
                    ],
                },
            ],
            "args":[
                {
                    "name":"name",
                    "type":"str",
                    "length":"64",
                    "unique":1,
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "建筑种类名",
                    "args":[
                    ],
                },
            ],
            "repr":"name",
        },                  #建筑种类
        {
            "table": "Bridge",
            "api": 1,
            "zh": "建筑",
            "crud":['post','put','delete'],
            "detail_sons":[
            ],
            "parents": [
                {
                    "name": "Basetype",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "基础种类id",
                    "tojson": "name",  # 在json字段当中显示的参数
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "基础类型"
                        },
                        {
                            "name": "id",
                            "type": "int",
                            "mean": "id"
                        },
                    ],
                },
                {
                    "name": "Buildtype",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "建筑种类id",
                    "tojson": "name",    #在json字段当中显示的参数
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "建筑类型"
                        },
                        {
                            "name": "id",
                            "type": "int",
                            "mean": "建筑类型id"
                        },
                    ],
                },
                {
                    "name": "Province",
                    "index": "id",
                    "type": "int",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "省份id",
                    "tojson": "name",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "省名 "
                        },
                        {
                            "name": "code",
                            "type": "int",
                            "mean": "建筑类型id"
                        },
                    ],
                },
                {
                    "name": "City",
                    "index": "id",
                    "type": "int",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "市id",
                    "tojson": "name",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "省名 "
                        },
                        {
                            "name": "code   ",
                            "type": "int",
                            "mean": "建筑类型id"
                        },
                    ],
                },
                {
                    "name": "Area",
                    "index": "id",
                    "type": "int",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "行政区id",
                    "tojson": "name",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "省名 "
                        },
                        {
                            "name": "code",
                            "type": "int",
                            "mean": "建筑类型id"
                        },
                    ],
                },
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "64",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 1,  # 是否支持模糊查找
                    "mean": "建筑名",
                    "unique":1,
                    "args": [
                    ],
                },
                {
                    "name": "safe_score",
                    "type": "float",
                    "length": "",
                    "post": 1,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "安全分数",
                    "args": [
                    ],
                },
                {
                    "name": "advice",
                    "type": "text",
                    "length": "",
                    "post": 1,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 0,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "管养建议",
                    "args": [
                    ],
                },
                {
                    "name": "address",
                    "type": "text",
                    "length": "",
                    "post": 1,  # 创建时候可以填写的参数
                    # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 0,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "详细地址",
                    "args": [
                    ],
                },
                {
                    "name": "about",
                    "type": "text",
                    "length": "",
                    "post": 1,  # 创建时候可以填写的参数
                    # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 0,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "概况",
                    "args": [
                    ],
                },
                {
                    "name": "monit_about",
                    "type": "text",
                    "length": "",
                    "post": 1,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 0,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "监测框架介绍",
                    "args": [
                    ],
                },
                {
                    "name": "latitude",
                    "type": "float",
                    # "length": "128",
                    "post": 1,  # 创建时候可以填写的参数
                    # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "纬度",
                    "args": [
                    ],
                },
                {
                    "name": "longitude",
                    "type": "float",
                    # "length": "128",
                    "post": 1,  # 创建时候可以填写的参数
                    # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "经度",
                    "args": [
                    ],
                },
                {
                    "name": "update_time",
                    "type": "time",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "更新时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.now",
                        },
                    ],
                },
                {
                    "name": "create_time",
                    "type": "time",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "创建时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.now",
                        },
                    ],
                },

            ],
            "repr": "name",
        },  # 建筑
        {
            "table": "Filetype",
            "api": 1,
            "zh": "文件类型",
            "crud":['post','put','delete'],
            "parents": [
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "64",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "文件类型名",
                    "args": [
                    ],
                },
                # {
                #     "name": "type",
                #     "type": "int",
                #       # 创建时候可以填写的参数
                #     "post": 2,  # 创建时候必须填写的参数
                #     "putneed": 1,  # 修改时可以修改的参数
                #     "listmust": 0,  # 请求列表必须post的参数
                #     "like": 0,  # 是否支持模糊查找
                #     "mean": "文件的种类：1图片，2excel，3pdf",
                #     "args": [
                #     ],
                # },
            ],
            "repr": "name",
        },  # 文件类型
        {
            "table": "File",
            "api": 1,
            "crud":['post','put','delete'],
            "zh": "文件",
            "parents": [
                {
                    "name": "Filetype",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "文件类型id",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "类型名"
                        },
                    ]
                },
                {
                    "name": "Bridge",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "建筑id",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "建筑名"
                        },
                    ]
                },
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "64",
                    "post": 2,  # 创建时候可以填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表必须post的参数
                    "like": 1,  # 是否支持模糊查找
                    "mean": "文件名",
                    "filter": "like",
                    "args": [
                    ],
                },
                {
                    "name": "file_name",
                    "type": "str",
                    "length": "256",
                    "post": 0,  # 创建时候可以填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表必须post的参数
                    "like": 1,  # 是否支持模糊查找
                    "mean": "文件上传名",
                    "filter": "like",
                    "file": 1,   #表示这是一个可以上传下载的文件：1表示可上传，2表示可下载，3表示可上传下载
                    "args": [
                    ],
                },
                # {
                #     "name": "type",
                #     "type": "int",
                #     "post": 2,  # 创建时候必须填写的参数
                #     "putneed": 1,  # 修改时可以修改的参数
                #     "listmust": 0,  # 请求列表必须post的参数
                #     "mean": "文件类型",
                #     "filter": "precise",
                #     "corres": [
                #         {'key': 1, 'value': "概览图片"},
                #         {'key': 2, 'value': "设计图纸"},
                #         {'key': 3, 'value': "设计文件"},
                #         {'key': 4, 'value': "施工文件"},
                #         {'key': 5, 'value': "竣工图纸"},
                #         {'key': 6, 'value': "验收文件"},
                #         {'key': 7, 'value': "行政文件"},
                #         {'key': 8, 'value': "定期检查报告"},
                #         {'key': 9, 'value': "特殊检查报告"},
                #         {'key': 10, 'value': "历史维修资料"},
                #     ],
                # },
                {
                    "name": "page",
                    "type": "int",
                    "post": 1,  # 创建时候可以填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "分册顺序",
                    "args": [
                    ],
                },
                {
                    "name": "update_time",
                    "type": "time",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "更新时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.now",
                        },
                    ],
                },
                {
                    "name": "create_time",
                    "type": "time",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "创建时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.now",
                        },
                    ],
                },

            ],
            "repr": "name",
        },  # 文件
        {
            "table": "Productimg",
            "api": 1,
            "zh": "产品图片",
            "parents": [
                {
                    "name": "Product",
                    "index": "id",
                    "type": "int",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "产品id",
                },
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "256",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "图片名",
                    "args": [
                    ],
                },

            ],
            "repr": "name",
        },  # 产品图片
        {
            "table": "Product",
            "api": 1,
            "crud":['post','put','delete'],
            "zh": "传感器类型",
            "detail_sons":[
                "device"
            ],
            "parents": [
                {
                    "name": "Monitgroup",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "监控分组id",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "分组名"
                        },
                        {
                            "name": "id",
                            "type": "int",
                            "mean": "id"
                        },
                    ]
                },
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "64",
                    # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "类型名",
                    "args": [
                    ],
                },
                {
                    "name": "args",
                    "type": "JSON",
                    "post": 1,  # 创建时候可以填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 0,  # 请求列表可以用来筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "默认自定义可变参数，在创建传感器时可以复用",
                    "args": [
                        {
                            "name": "default",
                            "value": "{}",
                        },
                    ],
                },
            ],
            "repr": "name",
        },  # 传感器类型
        {
            "table": "Device",
            "api": 1,
            "crud":['post','put','delete'],
            "zh": "传感器",
            "detail_sons":[
                "monitvalue"
            ],
            "many":[
            ],
            "parents": [
                {
                    "name": "Product",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "产品id",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "名"
                        },
                        {
                            "name": "id",
                            "type": "int",
                            "mean": "id"
                        },
                    ]
                },
                {
                    "name": "Bridge",
                    "index": "id",
                    "type": "int",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "建筑id",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "名"
                        },
                        {
                            "name": "id",
                            "type": "int",
                            "mean": "id"
                        },
                    ]
                },
                {
                    "name": "Dtu",
                    "index": "id",
                    "type": "int",
                    # 创建时候可以填写的参数
                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "DTUid",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "sn",
                            "type": "str",
                            "mean": "DTU序列号"
                        },
                        {
                            "name": "id",
                            "type": "int",
                            "mean": "id"
                        },
                    ],
                },
                {
                    "name": "Collect",
                    "index": "id",
                    "type": "int",
                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "采集仪id",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "sn",
                            "type": "str",
                            "mean": "采集仪序列号"
                        },
                        {
                            "name": "id",
                            "type": "int",
                            "mean": "id"
                        },
                    ],
                },
            ],
            "args": [
                {
                    "name": "sn",
                    "type": "str",
                    "length": "64",
                    "post": 0,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 1,  # 是否支持模糊查找
                    "mean": "编号",
                    "args": [
                    ],
                },
                {
                    "name": "exception",
                    "type": "bool",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 1,
                    "like": 0,  # 是否支持模糊查找
                    "mean": "是否异常",
                    "args": [
                        {
                            "name": "default",
                            "value": 0,
                        },
                    ],
                },
                {
                    "name": "bimid",
                    "type": "int",
                    "length": "256",
                      # 创建时候可以填写的参数
                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "位置BimId",
                    "args": [
                    ],
                },
                {
                    "name": "latitude",
                    "type": "float",
                    "post": 1,  # 创建时候可以填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "纬度",
                    "args": [
                    ],
                },
                {
                    "name": "longitude",
                    "type": "float",
                    "post": 1,  # 创建时候可以填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "经度",
                    "args": [
                    ],
                },
                {
                    "name": "fault",
                    "type": "bool",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 1,
                    "like": 0,  # 是否支持模糊查找
                    "mean": "是否故障",
                    "args": [
                        {
                            "name": "default",
                            "value": 0,
                        },
                    ],
                },
                {
                    "name": "install_time",
                    "type": "time",
                    "length": "",
                    "post": 1,  # 创建时候可以填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "安装时间",
                    "sorter": 1,
                    "args": [
                    ],
                },
                {
                    "name": "update_time",
                    "type": "time",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "更新时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.now",
                        },
                    ],
                },
                {
                    "name": "create_time",
                    "type": "time",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "创建时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.now",
                        },
                    ],
                },
                {
                    "name": "args",
                    "type": "JSON",
                    "post": 1,  # 创建时候可以填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 0,  # 请求列表可以用来筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "自定义可变参数",
                    "args": [
                        {
                            "name": "default",
                            "value": "{}",
                        },
                    ],
                },
            ],
            "repr": "name",
        },  # 传感器
        {
            "table": "Deviceimg",
            "api": 1,
            "zh": "通讯设备图片",
            "crud":['post','put','delete'],
            "parents": [
                {
                    "name": "Device",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "传感器id",
                },
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "256",
                    "need": 0,  # 创建时候可以填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "file": 1,  # 表示这是一个可以上传下载的文件：1表示可上传，2表示可下载，3表示可上传下载
                    "mean": "图片名",
                    "args": [
                    ],
                },

            ],
            "repr": "name",
        },  # 传感器图片
        {
            "table": "Dtutype",
            "api": 1,
            "zh": "通讯设备类型",
            "crud":['post','put','delete'],
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
                    "like": 0,  # 是否支持模糊查找
                    "mean": "通讯设备类型名",
                    "args": [
                    ],
                },
                {
                    "name": "args",
                    "type": "JSON",
                    "post": 1,  # 创建时候可以填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 0,  # 请求列表可以用来筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "自定义可变参数",
                    "args": [
                        {
                            "name": "default",
                            "value": "{}",
                        },
                    ],
                },
            ],
            "repr": "name",
        },  # 通讯设备类型
        {
            "table": "Dtu",
            "api": 1,
            "crud":['post','put','delete'],
            "zh": "通讯设备",
            "many":[
            ],
            "parents": [
                {
                    "name": "Dtutype",
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
                        {
                            "name": "id",
                            "type": "int",
                            "mean": "id"
                        },
                    ],
                },
            ],
            "args": [
                {
                    "name": "sn",
                    "type": "str",
                    "length": "64",
                    # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 1,  # 是否支持模糊查找
                    "mean": "编号",
                    "args": [
                    ],
                },
                {
                    "name": "dtu_img",
                    "type": "str",
                    "length": "64",
                    # 创建时候可以填写的参数
                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 1,  # 是否支持模糊查找
                    "mean": "图片",
                    "args": [
                    ],
                },
                {
                    "name": "fault",
                    "type": "bool",
                    "need": 0,  # 创建时候可以填写的参数
                    # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 1,
                    "like": 0,  # 是否支持模糊查找
                    "mean": "是否故障",
                    "args": [
                        {
                            "name": "default",
                            "value": 0,
                        },
                    ],
                },
                {
                    "name": "install_time",
                    "type": "time",
                    "length": "",
                    "post": 1,  # 创建时候可以填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "安装时间",
                    "sorter": 1,
                    "args": [
                    ],
                },
                {
                    "name": "update_time",
                    "type": "time",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                    # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "更新时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.now",
                        },
                    ],
                },
                {
                    "name": "create_time",
                    "type": "time",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                    # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "创建时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.now",
                        },
                    ],
                },
                {
                    "name": "args",
                    "type": "JSON",
                    "post": 1,  # 创建时候可以填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 0,  # 请求列表可以用来筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "自定义可变参数",
                    "args": [
                        {
                            "name": "default",
                            "value": "{}",
                        },
                    ],
                },
            ],
            "repr": "name",
        },  # 通讯设备
        {
            "table": "Dtuimg",
            "api": 1,
            "zh": "通讯设备图片",
            "parents": [
                {
                    "name": "Dtu",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "产品id",
                },
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "256",
                    "need": 0,  # 创建时候可以填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "file": 1,  # 表示这是一个可以上传下载的文件：1表示可上传，2表示可下载，3表示可上传下载
                    "mean": "图片名",
                    "args": [
                    ],
                },

            ],
            "repr": "name",
        },  # 通讯设备图片
        {
            "table": "Collecttype",
            "api": 1,
            "zh": "采集仪类型",
            "crud":['post','put','delete'],
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
                    "like": 0,  # 是否支持模糊查找
                    "mean": "采集仪类型名",
                    "args": [
                    ],
                },
                {
                    "name": "args",
                    "type": "JSON",
                    "post": 1,  # 创建时候可以填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 0,  # 请求列表可以用来筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "自定义可变参数",
                    "args": [
                        {
                            "name": "default",
                            "value": "{}",
                        },
                    ],
                },
            ],
            "repr": "name",
        },  # 采集仪类型
        {
            "table": "Collect",
            "api": 1,
            "zh": "采集仪",
            "many":[
            ],
            "parents": [
                {
                    "name": "Collecttype",
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
                        {
                            "name": "id",
                            "type": "int",
                            "mean": "id"
                        },
                    ],
                },
            ],
            "args": [
                {
                    "name": "sn",
                    "type": "str",
                    "length": "64",
                    # 创建时候可以填写的参数
                    "post": 1,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 1,  # 是否支持模糊查找
                    "mean": "采集仪编号",
                    "args": [
                    ],
                },
                {
                    "name": "fault",
                    "type": "bool",
                    "need": 0,  # 创建时候可以填写的参数
                    # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 1,
                    "like": 0,  # 是否支持模糊查找
                    "mean": "是否故障",
                    "args": [
                        {
                            "name": "default",
                            "value": 0,
                        },
                    ],
                },
                {
                    "name": "install_time",
                    "type": "time",
                    "length": "",
                    "post": 1,  # 创建时候可以填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "安装时间",
                    "sorter": 1,
                    "args": [
                    ],
                },
                {
                    "name": "update_time",
                    "type": "time",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                    # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "更新时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.now",
                        },
                    ],
                },
                {
                    "name": "create_time",
                    "type": "time",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                    # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "创建时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.now",
                        },
                    ],
                },
                {
                    "name": "args",
                    "type": "JSON",
                    "post": 1,  # 创建时候可以填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 0,  # 请求列表可以用来筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "自定义可变参数",
                    "args": [
                        {
                            "name": "default",
                            "value": "{}",
                        },
                    ],
                },
            ],
            "repr": "name",
        },  # 采集仪
        {
            "table": "Collectimg",
            "api": 1,
            "zh": "通讯设备图片",
            "crud":['post','put','delete'],
            "parents": [
                {
                    "name": "Collect",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "采集仪id",
                },
            ],
            "args": [
                {
                    "name": "name",
                    "type": "str",
                    "length": "256",
                    "need": 0,  # 创建时候可以填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "file": 1,  # 表示这是一个可以上传下载的文件：1表示可上传，2表示可下载，3表示可上传下载
                    "mean": "图片名",
                    "args": [
                    ],
                },

            ],
            "repr": "name",
        },  # 采集仪图片
        {
            "table": "Devicelog",
            "api": 1,
            "zh": "设备日志",
            "parents": [
                {
                    "name": "Device",
                    "index": "id",
                    "type": "int",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "设备id",
                },
            ],
            "args": [
                {
                    "name": "position",
                    "type": "int",
                    # "length": "64",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "设备位置代号",
                    "args": [
                    ],
                },
                {
                    "name": "exception",
                    "type": "bool",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 1,
                    "like": 0,  # 是否支持模糊查找
                    "mean": "是否异常",
                    "args": [
                    ],
                },
                {
                    "name": "fault",
                    "type": "bool",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listneed": 1,
                    "like": 0,  # 是否支持模糊查找
                    "mean": "是否故障",
                    "args": [
                    ],
                },
                {
                    "name": "create_time",
                    "type": "time",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "创建时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.now",
                        },
                    ],
                },

            ],
            "repr": "name",
        },  # 设备日志
        {
            "table": "Monitgroup",
            "api": 1,
            "crud":['post','put','delete'],
            "zh": "监测种类",
            "detail_sons":[
                "product"
            ],
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
                    "like": 0,  # 是否支持模糊查找
                    "mean": "监测种类名",
                    "args": [
                    ],
                },
            ],
            "repr": "name",
        },  # 监测种类
        {
            "table": "Excepttrigger",
            "api": 1,
            "zh": "监控参数异常条件",
            "parents": [
                {
                    "name": "Monitvalue",
                    "index": "id",
                    "type": "int",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "监控类型id",
                },
            ],
            "args": [
                {
                    "name": "value",
                    "type": "float",
                    # "length": "64",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "监控参数值",
                    "args": [
                    ],
                },
                {
                    "name": "compare",
                    "type": "int",
                    # "length": "64",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "取值执行条件，1:<,2:>,3:=",
                    "args": [
                    ],
                },
                {
                    "name": "logic",
                    "type": "int",
                    # "length": "64",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "取值判断条件，1: and, 0: or",
                    "args": [
                    ],
                },
            ],
            "repr": "id",
        },  # 监控异常范围
        {
            "table": "Valuelog",
            "api": 1,
            "crud":['post','put','delete'],
            "zh": "监控值日志",
            "parents": [
                {
                    "name": "Monitvalue",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "监控值id",
                },
                {
                    "name": "Device",
                    "index": "id",
                    "type": "int",
                    # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "设备id",
                    "show": [  # 放在api当中显示的参数
                        {
                            "name": "name",
                            "type": "str",
                            "mean": "传感器名"
                        },
                    ],
                },
            ],
            "args": [
                {
                    "name": "value",
                    "type": "float",
                    # "length": "64",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "监控参数名",
                    "args": [
                    ],
                },
                {
                    "name": "create_time",
                    "type": "time",
                    "length": "",
                    "need": 0,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 0,  # 修改时可以修改的参数
                    "listneed": 1,  # 请求列表可以用来筛选，只要有这个时候，不可创建也可筛选
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "创建时间",
                    "args": [
                        {
                            "name": "default",
                            "value": "datetime.now",
                        },
                    ],
                },
            ],
            "repr": "id",
        },  # 监控参数值日志
        {
            "table": "Warn",
            "api": 1,
            "zh": "预警",
            "parents": [
                {
                    "name": "Bridge",
                    "index": "id",
                    "type": "int",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "建筑id",
                },
                {
                    "name": "Device",
                    "index": "id",
                    "type": "int",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "设备id",
                },
            ],
            "args": [
                {
                    "name": "statu",
                    "type": "bool",
                    # "length": "64",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数int
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "处理状态，1已处理，0未处理",
                    "args": [
                        {
                            "name": "default",
                            "value": 0,
                        },
                    ],
                },
                {
                    "name": "about",
                    "type": "text",
   #                 "length": "64",
                    "post": 1,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "预警处理结果",
                    "args": [
                    ],
                },
            ],
            "repr": "id",
        },  # 预警信息
        {
            "table": "Contact",
            "api": 1,
            "zh": "应急联络网",
            "parents": [
                {
                    "name": "Bridge",
                    "index": "id",
                    "type": "int",
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "建筑id",
                },
            ],
            "args": [
                {
                    "name": "about",
                    "type": "text",
   #                 "length": "64",
                    "post": 1,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "简介",
                    "args": [
                    ],
                },
            ],
            "repr": "id",
        },  # 应急联络网
        {
            "table": "Plan",
            "api": 1,
            "zh": "应急预案模板",
            "parents": [
                {
                    "name": "Bridge",
                    "index": "id",
                    "type": "int",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "建筑id",
                },
            ],
            "args": [
                {
                    "name": "about",
                    "type": "text",
   #                 "length": "64",
                    "post": 1,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "预警处理结果",
                    "args": [
                    ],
                },
            ],
            "repr": "id",
        },  # 应急预案模板
        {
            "table": "Material",
            "api": 1,
            "crud": [],
            "zh": "应急物资管理",
            "parents": [
                {
                    "name": "Bridge",
                    "index": "id",
                    "type": "int",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "建筑id",
                },
            ],
            "args": [
                {
                    "name": "about",
                    "type": "text",
   #                 "length": "64",
                    "post": 1,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "预警处理结果",
                    "args": [
                    ],
                },
            ],
            "repr": "id",
        },  # 应急物资管理
        {
            "table": "Emergency",
            "api": 1,
            "zh": "应急抢险队伍管理",
            "parents": [
                {
                    "name": "Bridge",
                    "index": "id",
                    "type": "int",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "建筑id",
                },
            ],
            "args": [
                {
                    "name": "about",
                    "type": "text",
   #                 "length": "64",
                    "post": 1,  # 创建时候可以填写的参数
                      # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "预警处理结果",
                    "args": [
                    ],
                },
            ],
            "repr": "id",
        },  # 应急抢险队伍管理
        {
            "table": "Emgreport",
            "api": 1,
            "zh": "应急报告管理",
            "parents": [
                {
                    "name": "Bridge",
                    "index": "id",
                    "type": "int",
                      # 创建时候可以填写的参数
                    "post": 2,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "mean": "建筑id",
                },
            ],
            "args": [
                {
                    "name": "about",
                    "type": "text",
   #                 "length": "64",
                      # 创建时候可以填写的参数
                    "post":0,  # 创建时候必须填写的参数
                    "putneed": 1,  # 修改时可以修改的参数
                    "listmust": 0,  # 请求列表必须post的参数
                    "like": 0,  # 是否支持模糊查找
                    "mean": "预警处理结果",
                    "args": [
                    ],
                },
            ],
            "repr": "id",
        },  # 应急报告管理
    ],
    "routes": [

        {
            "path": "args",  # 上级目录主菜单详情
            "name": "演示接口",
            "icon": "",  # ant的菜单图标，图标列表[]
            "components": [
                {
                    "module": "protable",
                    "table": "Province",
                },
                {
                    "module": "protable",
                    "table": "City",
                },
                # {
                #     "module": "protable",
                #     "table": "Area",
                # },
                # {
                #     "module": "protable",
                #     "table": "Buildtype",
                # },
                # {
                #     "module": "protable",
                #     "table": "Filetype",
                # },
                # {
                #     "module": "protable",
                #     "table": "Property",
                # },
                #
                #
                # {
                #     "module": "protable",
                #     "table": "Bridge",
                # },
                # {
                #     "module": "protable",
                #     "table": "File",
                # },
                #
                # {
                #     "module": "protable",
                #     "table": "Dtu",
                # },
                # {
                #     "module": "protable",
                #     "table": "Location",
                # },
                # {
                #     "module": "protable",
                #     "table": "Product",
                # },
                # {
                #     "module": "protable",
                #     "table": "Device",
                # },
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







