import os
from tools import make_tree, name_convert
from wclass.parent import Parent
from wclass.table import Table


# 总表
class Project(object):
    def __init__(self, root, ojson):
        self.ojson = ojson
        self.root = root
        self.appname = ojson.get('app')
        self.appdir = os.path.join(root, f'{self.appname}/src/app')
        self.project_dir = os.path.join(root, f'{self.appname}')
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

        for t in self.tables:
            t.table_map = self.table_map

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
        rd = {}
        for table in self.tables:
            rd.update(table.write_flask_models(self.project_dir))
            rd.update(table.write_api(self.appdir))
        return rd

    def generate_go_gin(self):
        go_gin_dir = os.path.join(self.project_dir, f'go_{self.appname}')
        rd = {}
        for table in self.tables:
            rd.update(table.make_go_gin(go_gin_dir))
        return rd

    def make_all(self):
        return {
            **self.generate_test_script_yapi(),
            **self.generate_flask(),
            **self.generate_go_gin(),
        }

    def write_all(self, addr_lines_map):
        """再次更改写入文件地址"""
        try:
            # addr_lines_map["w/home/dron/rong/bridge/go-tenants-manager/internal/routers/api/v1/pconfig.go"] = addr_lines_map.pop("w/home/dron/rong/autoAPI/work/new_work/pay/go_pay/internal/routers/api/v1/pconfig.go")
            # addr_lines_map["w/home/dron/rong/bridge/go-tenants-manager/internal/service/pconfig.go"] = addr_lines_map.pop("w/home/dron/rong/autoAPI/work/new_work/pay/go_pay/internal/service/pconfig.go")
            # addr_lines_map["w/home/dron/rong/bridge/go-tenants-manager/internal/dao/pconfig.go"] = addr_lines_map.pop("w/home/dron/rong/autoAPI/work/new_work/pay/go_pay/internal/dao/pconfig.go")
            # addr_lines_map["w/home/dron/rong/bridge/go-tenants-manager/internal/model/pconfig.go"] = addr_lines_map.pop("w/home/dron/rong/autoAPI/work/new_work/pay/go_pay/internal/model/pconfig.go")
            # addr_lines_map["w/home/dron/rong/bridge/go-tenants-manager/internal/routers/api/v1/tenant.go"] = addr_lines_map.pop("w/home/dron/rong/autoAPI/work/new_work/pay/go_pay/internal/routers/api/v1/tenant.go")
            # addr_lines_map["w/home/dron/rong/bridge/go-tenants-manager/internal/service/tenant.go"] = addr_lines_map.pop("w/home/dron/rong/autoAPI/work/new_work/pay/go_pay/internal/service/tenant.go")
            # addr_lines_map["w/home/dron/rong/bridge/go-tenants-manager/internal/dao/tenant.go"] = addr_lines_map.pop("w/home/dron/rong/autoAPI/work/new_work/pay/go_pay/internal/dao/tenant.go")
            # addr_lines_map["w/home/dron/rong/bridge/go-tenants-manager/internal/model/tenant.go"] = addr_lines_map.pop("w/home/dron/rong/autoAPI/work/new_work/pay/go_pay/internal/model/tenant.go")
            # addr_lines_map["w/home/dron/rong/bridge/go-tenants-manager/internal/routers/api/v1/project.go"] = addr_lines_map.pop("w/home/dron/rong/autoAPI/work/new_work/pay/go_pay/internal/routers/api/v1/project.go")
            # addr_lines_map["w/home/dron/rong/bridge/go-tenants-manager/internal/service/project.go"] = addr_lines_map.pop("w/home/dron/rong/autoAPI/work/new_work/pay/go_pay/internal/service/project.go")
            # addr_lines_map["w/home/dron/rong/bridge/go-tenants-manager/internal/dao/project.go"] = addr_lines_map.pop("w/home/dron/rong/autoAPI/work/new_work/pay/go_pay/internal/dao/project.go")
            # addr_lines_map["w/home/dron/rong/bridge/go-tenants-manager/internal/model/project.go"] = addr_lines_map.pop("w/home/dron/rong/autoAPI/work/new_work/pay/go_pay/internal/model/project.go")
            pass
        except KeyError as e:
            print("地址错误 ",e)
        
        for addr in addr_lines_map:
            print(addr)
            dirname = os.path.dirname(addr[1:])
            ex = os.path.exists(dirname)
            if not ex:
                os.makedirs(dirname)
            w = open(addr[1:], addr[0])
            for line in addr_lines_map[addr]:
                w.write(line)
            w.close()

    def run(self):
        print("开始运行全新写入")
        self.write_all(self.make_all())
