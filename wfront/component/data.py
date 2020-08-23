import os
import sys
sys.path.append(os.path.abspath('.../tools'))

from tools import Tdb

def w_component_data(root,ojson):
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
			initdir = os.path.join(root,f'src/pages/{path}/{component_name.lower()}_{module}/data.d.ts')
			w = open(initdir,'w+')

			w.write(f"export interface TableListItem {{\n")
			args = databases_dir[component_name]['args']
			for arg in args:
				arg_name = arg['name']
				type = Tdb(arg['type']).ts_interface
				w.write(f"  {arg_name}: {type};\n")
			w.write(f"}}\n")
			w.write(f"\n")
			w.write(f"export interface TableListPagination {{\n")
			w.write(f"  total: number;\n")
			w.write(f"  pageSize: number;\n")
			w.write(f"  current: number;\n")
			w.write(f"}}\n")
			w.write(f"\n")
			w.write(f"export interface TableListData {{\n")
			w.write(f"  list: TableListItem[];\n")
			w.write(f"  pagination: Partial<TableListPagination>;\n")
			w.write(f"}}\n")
			w.write(f"\n")
			w.write(f"export interface TableListParams {{\n")
			w.write(f"  status?: string;\n")
			w.write(f"  name?: string;\n")
			w.write(f"  desc?: string;\n")
			w.write(f"  key?: number;\n")
			w.write(f"  pageSize?: number;\n")
			w.write(f"  currentPage?: number;\n")
			w.write(f"  filter?: {{ [key: string]: any[] }};\n")
			w.write(f"  sorter?: {{ [key: string]: any }};\n")
			w.write(f"}}\n")
