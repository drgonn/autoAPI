project_json = {
    "app":"yuan",                  #文件源，app名
    "dataname":"yuan",                   #数据库名称
    "datapassword":"781117",
    "host":"http://frp.sealan.tech:20225",                             #文档中的域名地址
    "testhost":"frp.sealan.tech",                             #
    "testport":"20225",                             #
    "testprotocol":"http",                             #
    "blues":[
            {
                "name":"apiv1",
                "address":"/api/v1/yuan",      #其中一个api接口
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
            "table": "Face",
            "api":True,
            "zh":"脸",
            "parents":[
            ],
            "args": [

                {
                    "name": "age",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 1,
                    "mean": "肌肤年龄",

                    "args": [
                    ],
                },

                {
                    "name": "spot",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 1,
                    "mean": "斑点",

                    "args": [
                    ],
                },

                {
                    "name": "pore",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 1,
                    "mean": "毛孔",

                    "args": [
                    ],
                },

                {
                    "name": "skin_type",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 1,
                    "mean": "肤质",

                    "args": [
                    ],
                },

                {
                    "name": "acne",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 1,
                    "mean": "痤疮",

                    "args": [
                    ],
                },

                {
                    "name": "features",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 1,
                    "mean": "脸部特征属性",

                    "args": [
                    ],
                },

                {
                    "name": "chloasma",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 1,
                    "mean": "棕色斑",

                    "args": [
                    ],
                },

                {
                    "name": "roughness",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 1,
                    "mean": "粗糙度",

                    "args": [
                    ],
                },

                {
                    "name": "color",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 1,
                    "mean": "肤色",

                    "args": [
                    ],
                },

                {
                    "name": "disease",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 1,
                    "mean": "皮肤病",

                    "args": [
                    ],
                },

                {
                    "name": "texture",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 1,
                    "mean": "纹理",

                    "args": [
                    ],
                },

                {
                    "name": "uv_spot",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 1,
                    "mean": "紫外斑",

                    "args": [
                    ],
                },

                {
                    "name": "moisture",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 1,
                    "mean": "水分",

                    "args": [
                    ],
                },

                {
                    "name": "wrinkle",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 1,
                    "mean": "皱纹",

                    "args": [
                    ],
                },

                {
                    "name": "region",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 1,
                    "mean": "脸部关键点切割区域",

                    "args": [
                    ],
                },

                {
                    "name": "blackhead",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 1,
                    "mean": "黑头",

                    "args": [
                    ],
                },

                {
                    "name": "pockmark",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 1,
                    "mean": "痘痘",

                    "args": [
                    ],
                },

                {
                    "name": "dark_circl",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 1,
                    "mean": "黑眼圈",

                    "args": [
                    ],
                },

                {
                    "name": "appearance",
                    "type": "str",
                    "length": "64",
                    "post": 1,
                    "putneed": 1,
                    "mean": "颜",

                    "args": [
                    ],
                },

            ],
        },                  #yuan
    ]

}




