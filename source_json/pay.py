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
        # alert
        {"api": 1, "table": "Alert", "zh": "报警规则", "url_prefix": "", "about": "",
        "parents": [
            {"name":"User","index": "id","type": "int","post": 0,  "put": 0,"list": 0,"mean": "用户id",
        "show": [{"name": "name", "type": "string", "mean": "用户名"},],},
        ],
        "many":[],
        "args": [
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "id",         "type": "uint",  "length": "32", "default": None,    "mean": "主键ID",},
            {"post": 2, "put": 1, "list": 2, "sorter": 1, "name": "name",       "type": "string",  "length": "64", "default": None,  "mean": "名称", "unique": "global"},
            {"post": 1, "put": 1, "list": 1, "sorter": 0, "name": "webhook",       "type": "text",  "length": "256", "default": None, "mean": "推送地址", "index": 1},
            {"post": 1, "put": 1, "list": 2, "sorter": 0, "name": "emails",   "type": "json", "length": "", "default": None,    "mean": "告警邮箱"},
            {"post": 1, "put": 1, "list": 2, "sorter": 0, "name": "flow",   "type": "float", "length": "", "default": None,    "mean": "报警触发流量"},
            {"post": 1, "put": 1, "list": 2, "sorter": 0, "name": "all",   
                                "mapping": [
                        {'key': 0, 'value': "是"},
                        {'key': 1, 'value': "否"},
                    ],
            "type": "bool", "length": "", "default": None,    "mean": "是否是用户全部卡片"},
            {"post": 1, "put": 1, "list": 2, "sorter": 0, "name": "enable",   
                                "mapping": [
                        {'key': 0, 'value': "关闭"},
                        {'key': 1, 'value': "开启"},
                    ],
            "type": "bool", "length": "", "default": None,    "mean": "规则开启关闭"},
            {"post": 1, "put": 1, "list": 2, "sorter": 0, "name": "description",   "type": "text", "length": "", "default": None,    "mean": "描述",
                                "mapping": [
                        {'key': 1, 'value': "可激活"},
                        {'key': 2, 'value': "已激活"},
                        {'key': 3, 'value': "已停用"},
                    ],
            },
            {"post": 1, "put": 1, "list": 2, "sorter": 0, "name": "event",   "type": "int", "length": "", "default": None,    
                                "mapping": [
                        {'key': 1, 'value': "状态监控"},
                        {'key': 2, 'value': "流量值监控"},
                        {'key': 3, 'value': "流量比例监控"},
                    ],
            "mean": "规则类型分类"},
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "updated_at", "type": "time", "length": "", "default": "now",   "mean": "更新时间"},
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "created_at", "type": "time", "length": "", "default": "now",   "mean": "创建时间", },
        ],
        "repr": "id",
        },  # 
        {"api": 1, "table": "AlertLog", "zh": "告警日志", "url_prefix": "", "about": "", "parents": [
            {"name":"Alert","index": "id","type": "int","post": 0,  "put": 0,"list": 0,"mean": "规则id",
        "show": [{"name": "name", "type": "string", "mean": "规则名"},],},
        ], "many":[],
        "args": [
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "id",         "type": "uint",  "length": "32", "default": None,    "mean": "主键ID",},
            {"post": 2, "put": 1, "list": 2, "sorter": 1, "name": "iccid",       "type": "string",  "length": "128", "default": None,  "mean": "名称", "unique": "ouid"},
            {"post": 0, "put": 0, "list": 1, "sorter": 0, "name": "status",      
                                "mapping": [
                        {'key': 1, 'value': "可激活"},
                        {'key': 2, 'value': "已激活"},
                        {'key': 3, 'value': "已停用"},
                    ],
             "type": "int",  "length": "64", "default": None, "mean": "状态", "index": 1},
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "updated_at", "type": "time", "length": "", "default": "now",   "mean": "更新时间"},
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "created_at", "type": "time", "length": "", "default": "now",   "mean": "创建时间", },
        ],
        "repr": "id",
        },

        # 摄像头
        {"api": 1, "table": "Hikv", "zh": "摄像头", "url_prefix": "", "about": "摄像头",
        "parents": [
            {"name":"User","index": "id","type": "int","post": 0,  "put": 0,"list": 0,"mean": "用户id",
        "show": [{"name": "name", "type": "string", "mean": "用户名"},],},
            {"name":"Bridge","index": "id","type": "int","post": 1,  "put": 1,"list": 1,"mean": "桥梁id",
        "show": [{"name": "name", "type": "string", "mean": "桥梁名"},],},
            {"name":"Component","index": "id","type": "int","post": 1,  "put": 1,"list": 1,"mean": "部位id",
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

        {"api": 1, "table": "Config", "zh": "密码配置", "url_prefix": "", "about": "摄像头",
        "parents": [
        ],
        "many":[],
        "args": [
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "id",         "type": "uint",  "length": "", "default": None,    "mean": "主键ID",},
            {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "length",         "type": "uint",  "length": "", "default": None,    "mean": "主键ID",},
            {"post": 2, "put": 1, "list": 0, "sorter": 0, "name": "pure_number",       "type": "bool",  "length": "64", "default": None,  "mean": "摄像头名称"},
            {"post": 2, "put": 1, "list": 0, "sorter": 0, "name": "case_sensitive",       "type": "bool",  "length": "64", "default": None,  "mean": "摄像头账号的appKey"},
            {"post": 2, "put": 1, "list": 0, "sorter": 0, "name": "special_characters",       "type": "bool",  "length": "64", "default": None,  "mean": "摄像头账号的appSecret"},
            {"post": 2, "put": 1, "list": 0, "sorter": 0, "name": "auto_expire",       "type": "uint",  "length": "64", "default": None,  "mean": "摄像头账号的序列号"},
        ],
        "repr": "id",
        },  # 
    ],   
    "routes": [
        {
            "path": "args",  # 上级目录主菜单详情
            "name": "演示接口",
            "icon": "",  # ant的菜单图标，图标列表[]
            "components": [
                # {
                #     "module": "protable",
                #     "table": "Alert",
                # },
                {
                    "module": "protable",
                    "table": "AlertLog",
                },

            ],
        },
        {
            "path": "abc",  # 上级目录主菜单详情
            "name": "全部演示接口",
            "icon": "",  # ant的菜单图标，图标列表[]
            "components": "all",
        },
    ]
}
