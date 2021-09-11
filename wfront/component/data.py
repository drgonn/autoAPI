import os
import sys
sys.path.append(os.path.abspath('.../tools'))

from tools import Tdb

def w_component_data(root,ojson):
	appname = ojson.get('app')
	databases = ojson.get('databases')
	routes = ojson.get('routes') or []
	databases_dir = {i['table'] : i for i in databases}

	for route in routes:
		path = route['path']
		components = route['components']
		if components == "all":
			for table in databases:
				component_name = table.get('table')
				if component_name == "User":
					continue
				table = databases_dir[component_name]
				os.makedirs(os.path.join(root, f'src/pages/{appname}/{component_name.lower()}'), exist_ok=True)

				initdir = os.path.join(root, f'src/pages/{appname}/{component_name.lower()}/data.d.ts')
				w = open(initdir, 'w+')

				w.write(f"export interface TableListItem {{\n")
				args = databases_dir[component_name]['args']
				w.write(f"  id?: number;\n")
				for arg in args:
					arg_name = arg['name']
					type = Tdb(arg['type']).ts_interface
					w.write(f"  {arg_name}: {type};\n")
				w.write(f"}}\n")
				w.write(f"\n")

				w.write(f"export interface TablePutItem {{\n")
				args = databases_dir[component_name]['args']
				w.write(f"  id?: number;\n")
				for arg in args:
					put = arg.get('putneed')
					if put:
						arg_name = arg['name']
						type = Tdb(arg['type']).ts_interface
						if put == 1:
							w.write(f"  {arg_name}?: {type};\n")
						elif put == 2:
							w.write(f"  {arg_name}: {type};\n")

				if table.get("many"):
					for many in table.get('many'):
						if many.get('add_api'):
							manyclass = many.get('name')
							manyname = many.get('name').lower()
							w.write(f"  add_{manyname}_ids?: number[];\n")
							w.write(f"  remove_{manyname}_ids?: number[];\n")
				w.write(f"}}\n")
				w.write(f"\n")

			break
		for component in components:
			component_name = component['table']
			if component_name == "User":
				continue
			table = databases_dir[component_name]
			crud = table.get('crud') or []
			module = component['module']
			os.makedirs(os.path.join(root,f'src/pages/{appname}/{component_name.lower()}'),exist_ok=True)

			initdir = os.path.join(root,f'src/pages/{appname}/{component_name.lower()}/data.d.ts')
			w = open(initdir,'w+')

			w.write(f"export interface TableListItem {{\n")
			args = databases_dir[component_name]['args']
			w.write(f"  id?: number;\n")
			for arg in args:
				arg_name = arg['name']
				type = Tdb(arg['type']).ts_interface
				w.write(f"  {arg_name}: {type};\n")
			w.write(f"}}\n")
			w.write(f"\n")

			if "put" in crud:
				w.write(f"export interface TablePutItem {{\n")
				args = databases_dir[component_name]['args']
				w.write(f"  id?: number;\n")
				for arg in args:
					put = arg.get('putneed')
					if put:
						arg_name = arg['name']
						type = Tdb(arg['type']).ts_interface
						if put == 1:
							w.write(f"  {arg_name}?: {type};\n")
						elif put == 2:
							w.write(f"  {arg_name}: {type};\n")

				if table.get("many"):
					for many in table.get('many'):
						if many.get('add_api'):
							manyclass = many.get('name')
							manyname = many.get('name').lower()
							w.write(f"  add_{manyname}_ids?: number[];\n")
							w.write(f"  remove_{manyname}_ids?: number[];\n")
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
