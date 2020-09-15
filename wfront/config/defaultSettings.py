import os
import sys
sys.path.append(os.path.abspath('.../tools'))

from tools import Tdb

def w_config_defaultSettings(root,ojson):
	appname = ojson.get('app')
	appmean = ojson.get('mean')
	databases = ojson.get('databases')
	routes = ojson.get('routes')
	databases_dir = {i['table']: i for i in databases}

	initdir = os.path.join(root, f'config/defaultSettings.ts')
	w = open(initdir, 'w+')
	w.write(f"""import {{ Settings as ProSettings }} from '@ant-design/pro-layout';\n""")
	w.write(f"""\n""")
	w.write(f"""type DefaultSettings = ProSettings & {{\n""")
	w.write(f"""  pwa: boolean;\n""")
	w.write(f"""}};\n""")
	w.write(f"""\n""")
	w.write(f"""const proSettings: DefaultSettings = {{\n""")
	w.write(f"""  navTheme: 'dark',\n""")
	w.write(f"""  // 拂晓蓝\n""")
	w.write(f"""  primaryColor: '#1890ff',\n""")
	w.write(f"""  layout: 'side',\n""")
	w.write(f"""  contentWidth: 'Fluid',\n""")
	w.write(f"""  fixedHeader: false,\n""")
	w.write(f"""  fixSiderbar: true,\n""")
	w.write(f"""  colorWeak: false,\n""")
	w.write(f"""  menu: {{\n""")
	w.write(f"""    locale: true,\n""")
	w.write(f"""  }},\n""")
	w.write(f"""  title: '{appmean or appname}',\n""")
	w.write(f"""  pwa: false,\n""")
	w.write(f"""  iconfontUrl: '',\n""")
	w.write(f"""}};\n""")
	w.write(f"""\n""")
	w.write(f"""export type {{ DefaultSettings }};\n""")
	w.write(f"""\n""")
	w.write(f"""export default proSettings;\n""")
	w.close()
