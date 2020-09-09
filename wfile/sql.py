import os
from tools import Tdb
import pymysql



#用来写部署文档
def sql_start(ojson):            #没有databases时自动创建
    app = ojson.get('app')
    sql = ojson.get('sql')
    if sql is not None and sql.get('sql') == "mysql":
        host = sql.get('host')
        name =     sql.get('name')
        pwd =      sql.get('pwd')
        port= sql.get('port')
        conn = pymysql.connect(host, name, pwd,port=port,charset='utf8')
        cursor = conn.cursor()
        cursor.execute('show databases;')
        tables_tup = cursor.fetchall()
        print(f"开始创建{app}......")
        if f"('{app}',)" in str(tables_tup):
            print(f'{app}已经存在,开始检查表结构......')
            # migrate_dir = os.path.join(root, f'{app}/src/migrations')
            # if not os.path.exists(migrate_dir):
            #     os.system("python ")
        else:
            try:
                cursor.execute(f'CREATE DATABASE {app} character set utf8mb4;')
            except Exception as e:
                print(f'error:{e}')
                conn.rollback()
        conn.commit()
        cursor.close()
        conn.close()

