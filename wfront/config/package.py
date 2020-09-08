import os
import sys
sys.path.append(os.path.abspath('.../tools'))


from tools import replace_file

def modify_package_json(root,ojson):  #替换ant运行的port
	appname = ojson.get('app')
	antport = ojson.get('antport')
	file = os.path.join(root,'package.json')
	replace_file(file,'"start": (.+)"',f'"start": "umi dev --port={antport}"')



