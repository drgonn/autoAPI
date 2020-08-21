import os
s=[
['ts_code','str','TS股票代码'],
['trade_date','str','交易日期'],
['close','float','当日收盘价'],
['turnover_rate','float','换手率（%）'],
['turnover_rate_f','float','换手率（自由流通股）'],
['volume_ratio','float','量比'],
['pe','float','市盈率（总市值/净利润，亏损的PE为空）'],
['pe_ttm','float','市盈率（TTM，亏损的PE为空）'],
['pb','float','市净率（总市值/净资产）'],
['ps','float','市销率'],
['ps_ttm','float','市销率（TTM）'],
['dv_ratio','float','股息率（%）'],
['dv_ttm','float','股息率（TTM）（%）'],
['total_share','float','总股本（万股）'],
['float_share','float','流通股本（万股）'],
['free_share','float','自由流通股本（万）'],
['total_mv','float','总市值（万元）'],
['circ_mv','float','流通市值（万元）'],
]

# for i in s:
#     #     f = f'''
#     #                 {{
#     #                     "name": "{i[0]}",
#     #                     "type": "{i[1]}",
#     #                     "need": 1,  # 创建时候可以填写的参数
#     #                     "postmust": 1,  # 创建时候必须填写的参数
#     #                     "putneed": 1,  # 修改时可以修改的参数
#     #                     "listmust": 0,  # 请求列表必须post的参数
#     #                     "mean": "{i[2]}",
#     #                 }},
#     # '''
#     f = f'''{i[0]} = d.{i[0]},'''
#     f = f'''{i[0]} = np.float(d.{i[0]}) if not np.isnan(d.{i[0]}) else None,'''
#     print(f)
#


file = "/mnt/c/Users/dronn/rong/project/stock/front/my-stock/src/pages/list/table-list/data.d.ts"

to_file = "/mnt/c/Users/dronn/rong/project/autoAPI/wfront/component/"
os.makedirs(to_file,exist_ok=True)

# name = "data"

f = open(file,'r')
w = open(to_file+f'{name}.py','w+')
w.write(f"import os\n")
w.write(f"def w_component_{name}(root,ojson):\n")
w.write(f"\tappname = ojson.get('app')\n")
w.write(f"\tcomponent_name = 'table'\n")
w.write(f"\tos.makedirs(os.path.join(root,f'{{appname}}/front/src/pages/{{component_name}}'),exist_ok=True)\n")
w.write(f"\tinitdir = os.path.join(root,f'{{appname}}/front/src/pages/{{component_name}}/data.d.ts')\n")
w.write(f"\tw = open(initdir,'w+')\n")
w.write(f"")
w.write(f"")

for i in f:
    print(i)
    i = i.replace("{","{{")
    i = i.replace("}","}}")
    i = i[:-1]
    print(i)
    w.write(f'\tw.write(f"{i}")\n')

w.close()

