import os
import sys
sys.path.append(os.path.abspath('.../tools'))


from tools import replace_file

def modify_package_json(root,ojson):  #替换ant运行的port
	appname = ojson.get('app')
	antport = ojson.get('antport')
	file = os.path.join(root,'package.json')
	replace_file(file,'"start": (.+)"',f'"start": "umi dev --port={antport}"')


	login_about= ojson.get('login_about') or ""
	login_title= ojson.get('login_title') or ""
	file = os.path.join(root,'src/layouts/UserLayout.tsx')
	replace_file(file,'.+<div className={styles.desc}>(.+)</div>',f'        <div className={{styles.desc}}>{login_about}</div>')
	replace_file(file,'.+<span className={styles.title}>(.+)</span>',f'       <span className={{styles.title}}>{login_title}</span>')

	produce= ojson.get('produce') or ""
	file = os.path.join(root,'src/layouts/BasicLayout.tsx')
	replace_file(file,'.+copyright(.+)`}',f'       copyright={{`${{new Date().getFullYear()}} {produce}`}}')
