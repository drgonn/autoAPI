import os
import re
# from tools import write_map
from writefile.tools import write_map


def write_go_dapr_mygrations(p, path):
    """生成go dapr 后端文件"""
    print("生成go dapr 后端 数据库迁移文件。。。:", path)
    # 生成目录

    lines = []

    for table in p.tables:
        make_gin_dapr_internal_database_migrations_up(table, path)
        make_gin_dapr_internal_database_migrations_down(table, path)




def make_gin_dapr_internal_database_migrations_up(table, project_dir):
    file_path =  os.path.join(project_dir,f"internal/database/migrations/00000_{table.name}.up.sql")
    f_list = []
    f_list.append(f"/* {table.zh_name} */\n")
    f_list.append(f"CREATE TABLE IF NOT EXISTS `{table.name}`  (\n")
    for column in table.columns:
        default = f" DEFAULT {column.default.upper()}" if column.default else ""
        extra = column.extra.upper()
        s = f'    `{column.name}` {column.type.MYSQL_TYPE} {column.create_can_empty}{default} {extra} COMMENT \'{column.zh_name}\',\n'
        # print(s)
        f_list.append(s)
    
    for column in table.columns:
        if column.key:
            if column.key.lower() in ["pri","primary"]:
                s = f"    PRIMARY KEY (`{column.name}`),\n"
            elif column.key.lower() in ["pri","primary"]:
                s = f"    UNIQUE KEY (`{column.name}`),\n"

                    # s = f"{tab*tab_num}UNIQUE INDEX (`{column.name}`),\n"
            f_list.append(s)
    
    f_list[-1] =re.sub(",\n$","\n",f_list[-1])
    f_list.append(f") CHARACTER SET = utf8mb4;\n")

    r =  {file_path:f_list}
    write_map(r)
    

def make_gin_dapr_internal_database_migrations_down(table, project_dir):
    file_path =  os.path.join(project_dir,f"internal/database/migrations/00000_{table.names}.down.sql")
    f_list = []
    f_list.append(f"DROP TABLE IF EXISTS `{table.names}`;")
    write_map({file_path:f_list})

