import os
import sys
sys.path.append(os.path.abspath('.../tools'))

from tools import Tdb

def w_config_proxy(root,ojson):
	appname = ojson.get('app')
	databases = ojson.get('databases')
	port = ojson.get("testport")
	routes = ojson.get('routes')
	databases_dir = {i['table'] : i for i in databases}


	initdir = os.path.join(root,f'config/proxy.ts')
	w = open(initdir,'w+')
	w.write(f"""export default {{\n""")
	w.write(f"""  dev: {{\n""")
	w.write(f"""    '/api/': {{\n""")
	w.write(f"""      target: 'http://localhost:{port}/api/v1/{appname}',\n""")
	w.write(f"""      changeOrigin: true,\n""")
	w.write(f"""      pathRewrite: {{ '^/api': '' }},\n""")
	w.write(f"""    }},\n""")
	w.write(f"""  }},\n""")
	w.write(f"""  test: {{\n""")
	w.write(f"""    '/api/': {{\n""")
	w.write(f"""      target: 'https://preview.pro.ant.design',\n""")
	w.write(f"""      changeOrigin: true,\n""")
	w.write(f"""      pathRewrite: {{ '^': '' }},\n""")
	w.write(f"""    }},\n""")
	w.write(f"""  }},\n""")
	w.write(f"""  pre: {{\n""")
	w.write(f"""    '/api/': {{\n""")
	w.write(f"""      target: 'your pre url',\n""")
	w.write(f"""      changeOrigin: true,\n""")
	w.write(f"""      pathRewrite: {{ '^': '' }},\n""")
	w.write(f"""    }},\n""")
	w.write(f"""  }},\n""")
	w.write(f"""}};\n""")
	w.close()
