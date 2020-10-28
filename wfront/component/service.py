import os
import sys

sys.path.append(os.path.abspath('.../tools'))

from tools import Tdb


def w_component_service(root, ojson):
    appname = ojson.get('app')
    databases = ojson.get('databases')
    routes = ojson.get('routes') or []
    databases_dir = {i['table']: i for i in databases}
    auth = ojson.get('auth')
    token = '?token=${getToken()}' if auth else ""

    for route in routes:
        path = route['path']
        components = route['components']

        if components == "all":
            components = databases
        for component in components:
            component_name = component['table']
            if component_name == "User":
                continue
            table = databases_dir[component_name]
            crud = table.get('crud')
            os.makedirs(os.path.join(root, f'src/pages/{appname}/{component_name.lower()}'), exist_ok=True)
            initdir = os.path.join(root, f'src/pages/{appname}/{component_name.lower()}/service.ts')
            w = open(initdir, 'w+')
            # w.write(f"""import request from 'umi-request';\n""")
            w.write(f"""import request from '@/utils/request';\n""")
            if auth:
                w.write("""import { getToken } from '@/utils/authority';\n""")
            w.write(f"""import {{ TableListParams """)
            if "put" in crud:
                w.write(f""", TablePutItem""")
            w.write(f""" }} from './data.d';\n""")
            w.write(f"""\n""")

            w.write(f"""export async function query{component_name}List(params?: TableListParams) {{\n""")
            w.write(f"""  return request(`/api/{component_name.lower()}/list{token}`, {{\n""")
            w.write(f"""    params,\n""")
            w.write(f"""  }});\n""")
            w.write(f"""}}\n""")
            w.write(f"""\n""")

            if "post" in crud:
                w.write(f"""export async function add{component_name}(params: TableListParams) {{\n""")
                w.write(f"""  return request(`/api/{component_name.lower()}{token}`, {{\n""")
                w.write(f"""    method: 'POST',\n""")
                w.write(f"""    data: {{\n""")
                w.write(f"""      ...params,\n""")
                w.write(f"""    }},\n""")
                w.write(f"""  }});\n""")
                w.write(f"""}}\n""")
                w.write(f"""\n""")

            if "delete" in crud:
                w.write(f"""export async function remove{component_name}(params: {{ key: number[] }}) {{\n""")
                w.write(f"""  return request(`/api/{component_name.lower()}{token}`, {{\n""")
                w.write(f"""    method: 'DELETE',\n""")
                w.write(f"""    data: {{\n""")
                w.write(f"""      ...params,\n""")
                w.write(f"""      method: 'delete',\n""")
                w.write(f"""    }},\n""")
                w.write(f"""  }});\n""")
                w.write(f"""}}\n""")
                w.write(f"""\n""")

            if "put" in crud:
                w.write(f"""export async function update{component_name}(params: TablePutItem) {{\n""")
                w.write(f"""  return request(`/api/{component_name.lower()}/${{params.id}}{token}`, {{\n""")
                w.write(f"""    method: 'PUT',\n""")
                w.write(f"""    data: {{\n""")
                w.write(f"""      ...params,\n""")
                w.write(f"""    }},\n""")
                w.write(f"""  }});\n""")
                w.write(f"""}}\n""")
