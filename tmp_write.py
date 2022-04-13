import os
import re
s = [
    ['ts_code', 'str', 'TS股票代码'],
    ['trade_date', 'str', '交易日期'],
    ['close', 'float', '当日收盘价'],
    ['turnover_rate', 'float', '换手率（%）'],
    ['turnover_rate_f', 'float', '换手率（自由流通股）'],
    ['volume_ratio', 'float', '量比'],
    ['pe', 'float', '市盈率（总市值/净利润，亏损的PE为空）'],
    ['pe_ttm', 'float', '市盈率（TTM，亏损的PE为空）'],
    ['pb', 'float', '市净率（总市值/净资产）'],
    ['ps', 'float', '市销率'],
    ['ps_ttm', 'float', '市销率（TTM）'],
    ['dv_ratio', 'float', '股息率（%）'],
    ['dv_ttm', 'float', '股息率（TTM）（%）'],
    ['total_share', 'float', '总股本（万股）'],
    ['float_share', 'float', '流通股本（万股）'],
    ['free_share', 'float', '自由流通股本（万）'],
    ['total_mv', 'float', '总市值（万元）'],
    ['circ_mv', 'float', '流通市值（万元）'],
]

# for i in s:
#     #     f = f'''
#     #                 {{
#     #                     "name": "{i[0]}",
#     #                     "type": "{i[1]}",
#     #                     "post": 1,  # 创建时候可以填写的参数
#     #                     "post": 2,  # 创建时候必须填写的参数
#     #                     "putneed": 1,  # 修改时可以修改的参数
#     #                     "listmust": 0,  # 请求列表必须post的参数
#     #                     "mean": "{i[2]}",
#     #                 }},
#     # '''
#     f = f'''{i[0]} = d.{i[0]},'''
#     f = f'''{i[0]} = np.float(d.{i[0]}) if not np.isnan(d.{i[0]}) else None,'''
#     print(f)
#

basedir = os.path.abspath(os.path.dirname(__file__))
f = re.match("/mnt/c/Users/(\w*)/", basedir)
user = f.group(1)

file = f"/mnt/c/Users/{user}/rong/project/autoAPI/work/stock/front/config/defaultSettings.ts"
to_file = f"/mnt/c/Users/{user}/rong/project/autoAPI/wfront/config/"
os.makedirs(to_file, exist_ok=True)

name = "defaultSettings"  # 生成的文件名

f = open(file, 'r')
w = open(to_file+f'{name}.py', 'w+')


w.write(f"import os\n")
w.write(f"import sys\n")
w.write(f"sys.path.append(os.path.abspath('.../tools'))\n")
w.write(f"\n")
w.write(f"from tools import Tdb\n")
w.write(f"\n")
w.write(f"def w_config_{name}(root,ojson):\n")
w.write(f"\tappname = ojson.get('app')\n")
w.write(f"\tdatabases = ojson.get('databases')\n")
w.write(f"\troutes = ojson.get('routes')\n")
w.write(f"\tdatabases_dir = {{i['table'] : i for i in databases}}\n")
w.write(f"\n")
w.write(f"\tfor route in routes:\n")
w.write(f"\t\tpath = route['path']\n")
w.write(f"\t\tcomponents = route['components']\n")
w.write(f"\t\tfor component in components:\n")
w.write(f"\t\t\tcomponent_name = component['table']\n")
w.write(f"\t\t\tmodule = component['module']\n")
w.write(
    f"\t\t\tos.makedirs(os.path.join(root,f'{{appname}}/front/src/pages/{{path}}/{{component_name.lower()}}_{{module}}'),exist_ok=True)\n")
w.write(
    f"\t\t\tinitdir = os.path.join(root,f'{{appname}}/front/src/pages/{{path}}/{{component_name.lower()}}_{{module}}/data.d ts')\n")
w.write(f"\t\t\tw = open(initdir,'w+')\n")
w.write(f"")
w.write(f"")

for i in f:
    print(i)
    i = i.replace("{", "{{")
    i = i.replace("}", "}}")
    i = i[:-1]
    print(i)
    w.write(f'''\t\t\tw.write(f"""{i}\\n""")\n''')

w.write(f'''\tw.close()\n''')
w.close()

# for i in range(67):
#     # f = f'''                    {{
#     #                     "name": "v{i+1}",
#     #                     "type": "float",
#     #                     "post": 1,  # 创建时候可以填写的参数
#     #                     "putneed": 1,  # 修改时可以修改的参数
#     #                     "listmust": 0,  # 请求列表必须post的参数
#     #                     "mean": "v{i+1}",
#     #                 }},'''
#     # print(f)
#     # print(f"v{i+1} = ts[{i+12}]/10,")+2
#     print(f"chart_data.push({{time: o.e_time, value: o.v{i+1},name:'v{i+1}'}})")
