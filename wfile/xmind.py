import os
import random
import json
import string
import html

def write_xmind(root,ojson):
    app = ojson.get('app')
    host=ojson.get("testhost")                             #
    port = ojson.get("testport")                                #
    protocol= ojson.get("testprotocol")                             #

    testdoc = os.path.join(root, f'{app}/test/{app}_xmind.md')
    w = open(testdoc,'w+')
    w.write(f'# {app}\n\n')
    crud = [("创建","POST",'',False),
            ("列表","POST",'/list','$.data.records[-1].id'),
            ("单个获取","GET",'/<id>',False),
            ("修改","PUT",'/<id>',False),
            ("删除","DELETE",'/<id>',False),
            ]
    for table in ojson.get('databases'):
        if table.get('api'):
            zh = table.get('zh')
            tablename = table.get("table").lower()
            pjson = {}
            w.write(f'## {zh}\n\n')
            for typezh,method,p,argaddr in crud:
                path = f"/api/v1/order/{tablename}"
                bean = False
                if typezh == "创建":
                    for column in table.get('args'):
                        if column.get('need'):
                            argname = column.get('name')
                            argtype = column.get('type')
                            pjson[argname] = random_arg(argtype)
                    for column in table.get('parents'):
                        pclass = column.get('name')
                        if column.get('postmust') and column.get('name') != 'User':
                            argname = column.get('name').lower()+ "Id"
                            argtype = column.get('type')
                            pjson[argname] = random_arg('int')
                elif typezh == "列表":
                    pjson['pageindex'] = 1
                    pjson['pagesize'] = 15
                    bean = f"{table.get('table')}_id"
                elif typezh == "修改":
                    pjson = {}
                    for column in table.get('args'):
                        if column.get('putneed'):
                            argname = column.get('name')
                            argtype = column.get('type')
                            pjson[argname] = random_arg(argtype)
                pjsonstr = json.dumps(pjson)
                # pjsonstr = html.escape(pjsonstr)
                if p == '/<id>':
                    id = random_arg("int")
                    path+=f'/id'
                else:
                    id = False
                    path += p
                single_api = single_str(zh,typezh,host,port,protocol,path,method,pjsonstr,tablename,id,w)


    w.close()
def single_str(zh,typezh,host,port,protocol,path,method,pjson,tablename,id,w):
    w.write(f'- {zh + typezh}\n\n')
    w.write(f'\t- 请求方法\n\n')
    w.write(f'\t\t- {method}\n\n')
    w.write(f'\t- 请求地址\n\n')
    if id:
        w.write(f'\t\t- {protocol}://{host}:{port}{path}/{id}?token={{token}}\n\n')
    else:
        w.write(f'\t\t- {protocol}://{host}:{port}{path}?token={{token}}\n\n')
    w.write(f'\t- 请求参数示例\n\n')
    w.write(f'\t\t- {pjson}\n\n')



def random_arg(type):
    if type == 'str':
        return ''.join(random.sample(string.ascii_letters + string.digits, 8))
    elif type == "float":
        return round(random.uniform(1, 100),3)
    elif type == "bool":
        return random.randint(0,1)
    elif type == "int":
        return random.randint(0,5)








