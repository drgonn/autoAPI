import os
import sys
sys.path.append(os.path.abspath('.../tools'))

from tools import Tdb

def w_config_config(root,ojson):
	appname = ojson.get('app')
	databases = ojson.get('databases')
	routes = ojson.get('routes')
	databases_dir = {i['table'] : i for i in databases}


	initdir = os.path.join(root,f'config/config.ts')
	w = open(initdir,'w+')
	w.write(f"""// https://umijs.org/config/\n""")
	w.write(f"""import {{ defineConfig }} from 'umi';\n""")
	w.write(f"""import defaultSettings from './defaultSettings';\n""")
	w.write(f"""import proxy from './proxy';\n""")
	w.write(f"""\n""")
	w.write(f"""const {{ REACT_APP_ENV }} = process.env;\n""")
	w.write(f"""\n""")
	w.write(f"""export default defineConfig({{\n""")
	w.write(f"""  hash: true,\n""")
	w.write(f"""  antd: {{}},\n""")
	w.write(f"""  dva: {{\n""")
	w.write(f"""    hmr: true,\n""")
	w.write(f"""  }},\n""")
	w.write(f"""  locale: {{\n""")
	w.write(f"""    // default zh-CN\n""")
	w.write(f"""    default: 'zh-CN',\n""")
	w.write(f"""    antd: true,\n""")
	w.write(f"""    // default true, when it is true, will use `navigator.language` overwrite default\n""")
	w.write(f"""    baseNavigator: true,\n""")
	w.write(f"""  }},\n""")
	w.write(f"""  dynamicImport: {{\n""")
	w.write(f"""    loading: '@/components/PageLoading/index',\n""")
	w.write(f"""  }},\n""")
	w.write(f"""  targets: {{\n""")
	w.write(f"""    ie: 11,\n""")
	w.write(f"""  }},\n""")
	w.write(f"""  // umi routes: https://umijs.org/docs/routing\n""")
	w.write(f"""  routes: [\n""")
	w.write(f"""    {{\n""")
	w.write(f"""      path: '/user',\n""")
	w.write(f"""      component: '../layouts/UserLayout',\n""")
	w.write(f"""      routes: [\n""")
	w.write(f"""        {{\n""")
	w.write(f"""          name: 'login',\n""")
	w.write(f"""          path: '/user/login',\n""")
	w.write(f"""          component: './user/login',\n""")
	w.write(f"""        }},\n""")
	w.write(f"""      ],\n""")
	w.write(f"""    }},\n""")
	w.write(f"""    {{\n""")
	w.write(f"""      path: '/',\n""")
	w.write(f"""      // component: '../layouts/SecurityLayout',\n""")
	w.write(f"""      routes: [\n""")
	w.write(f"""        {{\n""")
	w.write(f"""          path: '/',\n""")
	w.write(f"""          component: '../layouts/BasicLayout',\n""")
	w.write(f"""          authority: ['admin', 'user'],\n""")
	w.write(f"""          routes: [\n""")
	w.write(f"""            {{\n""")
	w.write(f"""              path: '/',\n""")
	path = routes[0].get('path')
	table_name = routes[0]['components'][0].get("table")
	print("tablename",table_name)
	w.write(f"""              redirect: '/{path}/{table_name.lower()}',\n""")
	w.write(f"""            }},\n""")
	for route in routes:
		if route.get('components'):   #说明是菜单，不是最终标签
			son_routes = route.get('components')
			path = route.get('path')
			icon = route.get('icon')
			w.write(f"""            {{\n""")
			w.write(f"""              path: '/{path}',\n""")
			w.write(f"""              name: '{route.get('name')}',\n""")
			if icon:
				w.write(f"""              icon: '{icon}',\n""")
			w.write(f"""              routes: [\n""")
			for son_route in son_routes:
				table_name = son_route.get("table")
				table = databases_dir.get(table_name)
				w.write(f"""                {{\n""")
				w.write(f"""                  path: '/{path}/{table_name.lower()}',\n""")
				w.write(f"""                  name: '{table.get('zh')}',\n""")
				w.write(f"""                  component: './{path}/{table_name.lower()}',\n""")
				w.write(f"""                }},\n""")
			w.write(f"""              ]\n""")
			pass
		else:                   #是目标菜单
			pass        #一级目录，暂时不写

		w.write(f"""            }},\n""")



	w.write(f"""            {{\n""")
	w.write(f"""              path: '/admin',\n""")
	w.write(f"""              name: 'admin',\n""")
	w.write(f"""              icon: 'crown',\n""")
	w.write(f"""              component: './Admin',\n""")
	w.write(f"""              authority: ['admin'],\n""")
	w.write(f"""              routes: [\n""")
	w.write(f"""                {{\n""")
	w.write(f"""                  path: '/admin/sub-page',\n""")
	w.write(f"""                  name: 'sub-page',\n""")
	w.write(f"""                  icon: 'smile',\n""")
	w.write(f"""                  component: './Welcome',\n""")
	w.write(f"""                  authority: ['admin'],\n""")
	w.write(f"""                }},\n""")
	w.write(f"""              ],\n""")
	w.write(f"""            }},\n""")

	w.write(f"""            {{\n""")
	w.write(f"""              component: './404',\n""")
	w.write(f"""            }},\n""")
	w.write(f"""          ],\n""")
	w.write(f"""        }},\n""")
	w.write(f"""        {{\n""")
	w.write(f"""          component: './404',\n""")
	w.write(f"""        }},\n""")
	w.write(f"""      ],\n""")
	w.write(f"""    }},\n""")
	w.write(f"""    {{\n""")
	w.write(f"""      component: './404',\n""")
	w.write(f"""    }},\n""")
	w.write(f"""  ],\n""")
	w.write(f"""  // Theme for antd: https://ant.design/docs/react/customize-theme-cn\n""")
	w.write(f"""  theme: {{\n""")
	w.write(f"""    // ...darkTheme,\n""")
	w.write(f"""    'primary-color': defaultSettings.primaryColor,\n""")
	w.write(f"""  }},\n""")
	w.write(f"""  // @ts-ignore\n""")
	w.write(f"""  title: false,\n""")
	w.write(f"""  ignoreMomentLocale: true,\n""")
	w.write(f"""  proxy: proxy[REACT_APP_ENV || 'dev'],\n""")
	w.write(f"""  manifest: {{\n""")
	w.write(f"""    basePath: '/',\n""")
	w.write(f"""  }},\n""")
	w.write(f"""}});\n""")
	w.close()
