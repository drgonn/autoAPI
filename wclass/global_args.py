"""公共环境变量"""


class Global(object):
    # 返回数据标签
    RETURNBOOLNAME = "status"
    RETURNINTNAME = "code"
    RETURNSTRNAME = "message"
    RETURNLISTPERNAME = "per_page"
    RETURNLISTCURRENTNAME = "current"
    RETURNLISTSIZENAME = "size"
    RETURNLISTTOTALNAME = "total"

    TAB = "    "

    # go_dapr 使用的db数据库包
    GODAPRDBPACKAGE = "database"