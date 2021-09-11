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
        {
            "api": 1, "table": "Project", "zh": "项目", "url_prefix": "", "about": "",
            "parents": [
            ],
            "many":[
            ],
            "args": [
                {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "id",         "type": "int",  "length": "", "default": None,    "mean": "主键ID"},
                {"post": 1, "put": 1, "list": 2, "sorter": 1, "name": "name",       "type": "str",  "length": "64", "default": None,  "mean": "名称"},
                {"post": 0, "put": 0, "list": 1, "sorter": 0, "name": "puid",       "type": "str",  "length": "256", "default": None, "mean": "PID"},
                {"post": 1, "put": 0, "list": 1, "sorter": 0, "name": "ouid",       "type": "str",  "length": "256", "default": None, "mean": "租户UID"},
                {"post": 1, "put": 1, "list": 2, "sorter": 0, "name": "describe",   "type": "text", "length": "", "default": None,    "mean": "描述"},
                {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "updated_at", "type": "time", "length": "", "default": "now",   "mean": "更新时间"},
                {"post": 0, "put": 0, "list": 0, "sorter": 1, "name": "created_at", "type": "time", "length": "", "default": "now",   "mean": "创建时间", },
            ],
            "repr": "id",
        },  # 巡检任务
    ]
}
