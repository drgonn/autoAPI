project_json = {
    "app": "pay",
    "dataname": "pay",
    "datapassword": "781117",
    "host": "http://frp.sealan.tech:20222",
    "testhost": "frp.sealan.tech",
    "testport": "20221",
    "testprotocol": "http",
    "blues": [
    ],
    "configs": [
    ],
    "packages": [
    ],
    "databases": [
        {"api": 1, "table": "Tenant", "zh": "租户", "url_prefix": "", "about": "",
        "parents": [],
        "many":[],
        "args": [
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "id",         "type": "uint",  "length": "32", "default": None,    "mean": "主键ID",},
            {"post": 2, "put": 1, "list": 2, "sorter": 1, "name": "name",       "type": "string",  "length": "64", "default": None,  "mean": "名称", "unique": "global"},
            {"post": 0, "put": 0, "list": 1, "sorter": 0, "name": "ouid",       "type": "string",  "length": "256", "default": None, "mean": "租户UID", "index": 1},
            {"post": 1, "put": 1, "list": 2, "sorter": 0, "name": "describe",   "type": "text", "length": "", "default": None,    "mean": "描述"},
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "updated_at", "type": "time", "length": "", "default": "now",   "mean": "更新时间"},
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "created_at", "type": "time", "length": "", "default": "now",   "mean": "创建时间", },
        ],
        "repr": "id",
        },  # 
        {"api": 1, "table": "Project", "zh": "项目", "url_prefix": "", "about": "", "parents": [], "many":[],
        "args": [
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "id",         "type": "uint",  "length": "32", "default": None,    "mean": "主键ID",},
            {"post": 2, "put": 1, "list": 2, "sorter": 1, "name": "name",       "type": "string",  "length": "64", "default": None,  "mean": "名称", "unique": "ouid"},
            {"post": 0, "put": 0, "list": 1, "sorter": 0, "name": "puid",       "type": "string",  "length": "256", "default": None, "mean": "PID", "index": 1},
            {"post": 1, "put": 1, "list": 1, "sorter": 0, "name": "ouid",       "type": "string",  "length": "256", "default": None, "mean": "租户UID"},
            {"post": 1, "put": 1, "list": 2, "sorter": 0, "name": "describe",   "type": "text", "length": "", "default": None,    "mean": "描述"},
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "updated_at", "type": "time", "length": "", "default": "now",   "mean": "更新时间"},
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "created_at", "type": "time", "length": "", "default": "now",   "mean": "创建时间", },
        ],
        "repr": "id",
        },
        {"api": 1, "table": "Pconfig", "zh": "配置", "url_prefix": "", "about": "", "parents": [], "many":[],
        "args": [
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "id",         "type": "uint",  "length": "32", "default": None,    "mean": "主键ID",},
            {"post": 2, "put": 1, "list": 2, "sorter": 1, "name": "name",       "type": "string",  "length": "64", "default": None,  "mean": "名称" ,"unique": "ouid"},
            {"post": 1, "put": 1, "list": 1, "sorter": 0, "name": "puid",       "type": "string",  "length": "256", "default": None, "mean": "PID",},
            {"post": 1, "put": 1, "list": 2, "sorter": 0, "name": "value",      "type": "text", "length": "", "default": None,    "mean": "value"},
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "updated_at", "type": "time", "length": "", "default": "now",   "mean": "更新时间"},
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "created_at", "type": "time", "length": "", "default": "now",   "mean": "创建时间", },
        ],
        "repr": "id",
        },
        {"api": 1, "table": "Hikv", "zh": "摄像头", "url_prefix": "", "about": "摄像头",
        "parents": [
            {"name":"User","index": "id","type": "int","post": 0,  "put": 0,"list": 0,"mean": "用户id",
        "show": [{"name": "name", "type": "string", "mean": "用户名"},],},
            {"name":"Bridge","index": "id","type": "int","post": 1,  "put": 1,"list": 0,"mean": "桥梁id",
        "show": [{"name": "name", "type": "string", "mean": "桥梁名"},],},
            {"name":"Component","index": "id","type": "int","post": 1,  "put": 1,"list": 0,"mean": "部位id",
        "show": [{"name": "sn", "type": "string", "mean": "构件sn"},],}
        ],
        "many":[],
        "args": [
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "id",         "type": "uint",  "length": "", "default": None,    "mean": "主键ID",},
            {"post": 2, "put": 1, "list": 0, "sorter": 0, "name": "name",       "type": "string",  "length": "64", "default": None,  "mean": "摄像头名称"},
            {"post": 2, "put": 1, "list": 0, "sorter": 0, "name": "app_key",       "type": "string",  "length": "64", "default": None,  "mean": "摄像头账号的appKey"},
            {"post": 2, "put": 1, "list": 0, "sorter": 0, "name": "app_secret",       "type": "string",  "length": "64", "default": None,  "mean": "摄像头账号的appSecret"},
            {"post": 2, "put": 1, "list": 0, "sorter": 0, "name": "hikv_serial",       "type": "string",  "length": "64", "default": None,  "mean": "摄像头账号的序列号"},
            {"post": 2, "put": 1, "list": 0, "sorter": 0, "name": "validate_code",       "type": "string",  "length": "64", "default": None,  "mean": "摄像头账号的验证码"},
            {"post": 1, "put": 1, "list": 0, "sorter": 0, "name": "cap_minute",       "type": "uint",  "length": "", "default": None,  "mean": "摄像头定时间隔拍照时间"},
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "updated_at", "type": "time", "length": "", "default": "now",   "mean": "更新时间"},
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "created_at", "type": "time", "length": "", "default": "now",   "mean": "创建时间", },
        ],
        "repr": "id",
        },  # 
        {"api": 1, "table": "Capimg", "zh": "抓拍图片", "url_prefix": "inspect", "about": "抓拍的图片记录", "parents": [
            {"name":"Hikv","index": "id","type": "int","post": 0,  "put": 0,"list": 1,"mean": "card id",
        "show": [],}
        ], "many":[
        ],
        "args": [
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "id",         "type": "uint",  "length": "32", "default": None,    "mean": "主键ID",},
            {"post": 0, "put": 1, "list": 0, "sorter": 0, "name": "hikv_url",       "type": "string",  "length": "256", "default": None,  "mean": "图片地址"},
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "created_at", "type": "time", "length": "", "default": "now",   "mean": "创建时间", },
        ],
        "repr": "id",
        },
        {"api": 1, "table": "Captime", "zh": "定时计划", "url_prefix": "", "about": "定时任务时间", "parents": [
            {"name":"Hikv","index": "id","type": "int","post": 0,  "put": 0,"list": 0,"mean": "摄像头",},
        ], "many":[
        ],
        "args": [
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "id",         "type": "uint",  "length": "32", "default": None,    "mean": "主键ID",},
            {"post": 2, "put": 1, "list": 2, "sorter": 1, "name": "iccid",       "type": "string",  "length": "128", "default": None,  "mean": "卡iccid" ,"unique": "ouid"},
            {"post": 1, "put": 1, "list": 1, "sorter": 0, "name": "status",       "type": "string",  "length": "64", "default": None, "mean": "通知返回状态码",},
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "created_at", "type": "time", "length": "", "default": "now",   "mean": "创建时间", },
        ],
        "repr": "id",
        },
    ]
}
