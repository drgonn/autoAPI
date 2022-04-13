project_json = {
    "app": "blog",
    "dataname": "blog",
    "datapassword": "781117",
    "host": "http://frp.sealan.tech:20222",
    "testhost": "frp.sealan.tech",
    "testport": "20221",
    "testprotocol": "http",
    "blues": [
    ],
    "sql":{
        "local_port":"3308",
        "docker_name":"mariadb2",
        "name":"mysql",
        "password":668899,
        "user":"root",
        "docker_port":"3306",
        "image":"mariadb:latest",
    },
    #用来配置环境变量，用来配置docker环境的
    "configs": [
        {},
        {},
        {},
    ],
    "packages": [
    ],
    "databases": [
        {"api": 1, "table": "Sun", "zh": "太阳", "url_prefix": "", "about": "",
        "parents": [
            # {"name":"User","index": "id","type": "int","post": 0,  "put": 0,"list": 0,"mean": "用户id",
        # "show": [{"name": "name", "type": "string", "mean": "用户名"},],},
        ],
        "many":[],
        "args": [
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "id",         "type": "uint",  "length": "", "default": None,    "mean": "主键ID",},
            {"post": 2, "put": 1, "list": 0, "sorter": 0, "name": "name",       "type": "string",  "length": "64", "default": None,  "mean": "名称"},
            {"post": 2, "put": 1, "list": 0, "sorter": 0, "name": "about",       "type": "text",  "length": "64", "default": None,  "mean": "简介"},
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "updated_at", "type": "time", "length": "", "default": "now",   "mean": "更新时间"},
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "created_at", "type": "time", "length": "", "default": "now",   "mean": "创建时间", },
        ],
        "repr": "id",
        },   

        {"api": 1, "table": "Moon", "zh": "月亮", "url_prefix": "", "about": "",
        "parents": [
            {"name":"Sun","index": "id","type": "int","post": 0,  "put": 0,"list": 0,"mean": "太阳id",
        "show": [{"name": "name", "type": "string", "mean": "太阳名"},],},
        ],
        "many":[],
        "args": [
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "id",         "type": "uint",  "length": "", "default": None,    "mean": "主键ID",},
            {"post": 2, "put": 1, "list": 0, "sorter": 0, "name": "name",       "type": "string",  "length": "64", "default": None,  "mean": "名称"},
            {"post": 2, "put": 1, "list": 0, "sorter": 0, "name": "about",       "type": "text",  "length": "64", "default": None,  "mean": "简介"},
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "updated_at", "type": "time", "length": "", "default": "now",   "mean": "更新时间"},
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "created_at", "type": "time", "length": "", "default": "now",   "mean": "创建时间", },
        ],
        "repr": "id",
        },   

        {"api": 1, "table": "Star", "zh": "星星", "url_prefix": "", "about": "",
        "parents": [
            {"name":"Moon","index": "id","type": "int","post": 0,  "put": 0,"list": 0,"mean": "月亮id",
        "show": [{"name": "name", "type": "string", "mean": "月亮名"},],},
        ],
        "many":[],
        "args": [
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "id",         "type": "uint",  "length": "", "default": None,    "mean": "主键ID",},
            {"post": 2, "put": 1, "list": 0, "sorter": 0, "name": "name",       "type": "string",  "length": "64", "default": None,  "mean": "名称"},
            {"post": 2, "put": 1, "list": 0, "sorter": 0, "name": "about",       "type": "text",  "length": "64", "default": None,  "mean": "简介"},
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "updated_at", "type": "time", "length": "", "default": "now",   "mean": "更新时间"},
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "created_at", "type": "time", "length": "", "default": "now",   "mean": "创建时间", },
        ],
        "repr": "id",
        },   
    ]
}
