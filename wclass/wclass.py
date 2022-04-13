import os
from tools import name_convert
from wclass.parent import Parent
from wclass.table import Table
from wclass.sql import Sql


# 总表
class Project(object):
    def __init__(self, root, ojson):
        self.ojson = ojson
        self.root = root  # root,即文件的根目录，也就是project目录
        self.appname = ojson.get('app')
        self.appdir = os.path.join(root, f'{self.appname}/src/app')
        self.project_dir = os.path.join(root, f'{self.appname}')
        self.flask_dir = os.path.join(root, f'{self.appname}/flask')
        tables = ojson.get("databases")
        self.tables = []
        for t in tables:
            self.tables.append(
                Table(
                    t.get('table'),
                    t.get("api"),
                    t.get("zh"),
                    t.get("about"),
                    t.get("url_prefix"),
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

        self.sql = Sql(ojson.get("sql"))

        # for table in self.tables:
        #     for parent in table.parents:
        #         table.sons.append

        print("结构初始化成功")

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
