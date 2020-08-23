import os
import sys
sys.path.append(os.path.abspath('.../tools'))

from tools import Tdb

def w_component_service(root,ojson):
	appname = ojson.get('app')
	databases = ojson.get('databases')
	routes = ojson.get('routes')
	databases_dir = {i['table'] : i for i in databases}

	for route in routes:
		path = route['path']
		components = route['components']
		for component in components:
			component_name = component['table']
			module = component['module']
			os.makedirs(os.path.join(root,f'src/pages/{path}/{component_name.lower()}_{module}'),exist_ok=True)
			initdir = os.path.join(root,f'src/pages/{path}/{component_name.lower()}_{module}/service.ts')
			w = open(initdir,'w+')
			w.write(f"""import request from 'umi-request';\n""")
			w.write(f"""import {{ TableListParams }} from './data.d';\n""")
			w.write(f"""\n""")


			w.write(f"""export async function query{component_name}List(params?: TableListParams) {{\n""")
			w.write(f"""  return request('/api/{component_name.lower()}/list', {{\n""")
			w.write(f"""    method: 'POST',\n""")
			w.write(f"""    data: {{\n""")
			w.write(f"""      ...params,\n""")
			w.write(f"""    }},\n""")
			w.write(f"""  }});\n""")


			w.write(f"""}}\n""")
			w.write(f"""\n""")
			w.write(f"""export async function removeRule(params: {{ key: number[] }}) {{\n""")
			w.write(f"""  return request('/api/rule', {{\n""")
			w.write(f"""    method: 'POST',\n""")
			w.write(f"""    data: {{\n""")
			w.write(f"""      ...params,\n""")
			w.write(f"""      method: 'delete',\n""")
			w.write(f"""    }},\n""")
			w.write(f"""  }});\n""")
			w.write(f"""}}\n""")
			w.write(f"""\n""")
			w.write(f"""export async function addRule(params: TableListParams) {{\n""")
			w.write(f"""  return request('/api/rule', {{\n""")
			w.write(f"""    method: 'POST',\n""")
			w.write(f"""    data: {{\n""")
			w.write(f"""      ...params,\n""")
			w.write(f"""      method: 'post',\n""")
			w.write(f"""    }},\n""")
			w.write(f"""  }});\n""")
			w.write(f"""}}\n""")
			w.write(f"""\n""")
			w.write(f"""export async function updateRule(params: TableListParams) {{\n""")
			w.write(f"""  return request('/api/rule', {{\n""")
			w.write(f"""    method: 'POST',\n""")
			w.write(f"""    data: {{\n""")
			w.write(f"""      ...params,\n""")
			w.write(f"""      method: 'update',\n""")
			w.write(f"""    }},\n""")
			w.write(f"""  }});\n""")
			w.write(f"""}}\n""")