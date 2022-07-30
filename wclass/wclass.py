import os
import json
import time
import datetime
from tools import name_convert
from wclass.parent import Parent
from wclass.table import Table
from wclass.sql import Sql

from wclass.classfuc.data_switch import to_doc, doc2class
from wclass.doc.markdown import to_md


# 总表
class Project(object):
    def __init__(self, project, data_type):
        """初始化
        project string 项目名，例子 "nauth"
        data_type string 转化类型，包含 json doc mysql

        """
        # 找到project文件夹绝对地址
        file_dir = os.path.abspath(os.path.dirname(__file__))
        file_dir = os.path.dirname(file_dir)
        self.project_dir = os.path.join(file_dir, f"projects/{project}")
        self.doc_dir = os.path.join(self.project_dir, 'doc')
        self.flask_dir = os.path.join(self.project_dir, 'flask')
        now = datetime.datetime.now() - datetime.timedelta(days=1)
        self.now = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
        self.now_date = now.strftime('%Y/%m/%d')
        # 如果没有该目录，报错
        if not os.path.exists(self.project_dir):
            print(self.project_dir, "项目目录不存在")
            os.abort()

        # 查询该目录下的json文件
        json_dir = os.path.join(self.doc_dir, f"{project}.json")
        if not os.path.exists(json_dir):
            print(json_dir, "json文件不存在")
            os.abort()

        with open(json_dir, encoding='utf-8') as ff:
            project_json = json.load(ff)
        if project_json is None:
            os.abort("json文件导入失败")

        # 将json文件导入到对象
        if data_type == "json":
            with open(json_dir, encoding='utf-8') as ff:
                project_json = json.load(ff)
            if project_json is None:
                print("json文件导入失败")
                os.abort()

            self.project_json = project_json
            # self.root = project_dir  # root,即文件的根目录，也就是project目录
            self.appname = project_json.get('app')
            # self.appdir = os.path.join(project_dir, f'{self.appname}/src/app')
            # zh为项目中文名称，可用于文档名
            self.zh = project_json.get("zh") or "未命名"
            tables = project_json.get("databases")
            self.tables = []
            for t in tables:
                self.tables.append(
                    Table(
                        t.get('table'),
                        t.get("api"),
                        t.get("zh"),
                        t.get("about"),
                        t.get("url_prefix"),
                        t.get("index"),
                        t.get("repr"),
                        t.get("args"),
                        t.get("parents"),
                        t.get("many"),
                        t.get("sons"),
                    )
                )
            self.table_map = {}
            for table in self.tables:
                self.table_map[table.Name] = table
                table.app_name = self.appname

            for t in self.tables:
                t.table_map = self.table_map

            self.sql = Sql(project_json.get("sql"))
            print("json导入对象成功")
            
        elif data_type == "doc":
            # 先打开word文件，提取信息存入对象当中，然后对象写入json当中
            doc2class(self)



    def generate_test_script_yapi(self):
        rd = {}
        for table in self.tables:
            rd.update(table.write_test_yapi(self.project_dir))
        return rd


    def generate_flask(self):
        """
        return  rd:{w+文件绝对地址:[文件的字符串列表]}
        """
        rd = {}
        for table in self.tables:
            rd.update(table.write_flask_models(self.flask_dir))
            rd.update(table.write_api(self.flask_dir))
        return rd

    def generate_go_gin(self):
        go_gin_dir = os.path.join(self.project_dir, 'go_gin')
        rd = {}
        for table in self.tables:
            rd.update(table.make_go_gin(go_gin_dir))
        return rd

    def generate_go_gin_dapr(self):
        go_dir = os.path.join(self.project_dir, 'go_dapr')
        rd = {}
        for table in self.tables:
            rd.update(table.make_go_gin_dapr(go_dir))

        # 写入很多表都在一个文件里面时候情形
        wire_list = []
        server_list = []
        wire_path = os.path.join(go_dir, "internal/http/wire.go")
        server_path = os.path.join(go_dir, "internal/http/server.go")
        for table in self.tables:
            wire_list += table.make_gin_dapr_internal_http_wire()
            server_list += table.make_gin_dapr_internal_http_server()
        rd.update({wire_path: wire_list, server_path: server_list})
        return rd

    def generate_environment(self):
        docker_compose_file = os.path.join(self.project_dir, 'docker-compose.yml')
        docker_compose_str_list = ['version: "3.3"\nservices:\n']
        docker_compose_str_list.append(self.sql.write_docker_compose_str())
        rd = {docker_compose_file: docker_compose_str_list}
        return rd

    # 生成所有目录对应字符串的字典
    def make_all(self):
        return {
            **self.generate_test_script_yapi(),
            **self.generate_flask(),
            **self.generate_go_gin(),
            **self.generate_go_gin_dapr(),
            **self.generate_environment(),
        }

    def write_all(self, addr_lines_map):
        """再次更改写入文件地址
        args:
            addr_lines_map:一个字典
                {w+文件绝对地址:[文件的字符串列表]}
        """
        for addr in addr_lines_map:
            dirname = os.path.dirname(addr[1:])
            ex = os.path.exists(dirname)
            if not ex:
                os.makedirs(dirname)
            # print("addr", addr)
            w = open(addr, "w")
            for line in addr_lines_map[addr]:
                w.write(line)
            w.close()

    def run(self):
        print("开始运行全新写入")
        self.write_all(self.make_all())

        # 生成word文档
        to_doc(self)
        to_md(self)

