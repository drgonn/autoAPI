import os
import random
import json
import string
import html
import urllib


def write_postman(root, ojson):
    app = ojson.get('app')
    host = ojson.get("testhost")  #
    port = ojson.get("testport")  #
    protocol = ojson.get("testprotocol")  #
    r = {
        "info": {
            "_postman_id": "17c8561c-5131-404e-98ef-1a2c52be6c09",
            "name": app + " reset",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": [
        ],
        "protocolProfileBehavior": {}
    }
    testdoc = os.path.join(root, f'{app}/test/postman_reset.json')
    w = open(testdoc, 'w+')
    crud = [("创建", "POST", '', False),
            ("列表", "GET", '/list', '$.data.records[-1].id'),
            ("单个获取", "GET", '/<id>', False),
            ("修改", "PUT", '/<id>', False),
            ("删除", "DELETE", '', False),
            ]
    for table in ojson.get('databases'):
        if table.get('api'):
            zh = table.get('zh')
            tablename = table.get("table").lower()

            for typezh, method, p, argaddr in crud:
                path = f"/api/v1/order/{tablename}"
                bean = False
                pjson = {}
                query = [{
                    "key": "token",
                    "value": "{{token}}"
                }
                ]
                if typezh == "创建":
                    for column in table.get('args'):
                        if column.get('need'):
                            argname = column.get('name')
                            argtype = column.get('type')
                            pjson[argname] = random_arg(argtype)
                    for column in table.get('parents'):
                        pclass = column.get('name')
                        if column.get('postmust') and column.get('name') != 'User':
                            argname = column.get('name').lower() + "_id"
                            argtype = column.get('type')
                            pjson[argname] = random_arg('int')
                elif typezh == "列表":
                    sorter = {}
                    # sorter = urllib.parse.urlencode({})
                    query.append({'key':'current','value':'1'})
                    query.append({'key':'pagesize','value': '6'})
                    query.append({'key':'sorter','value': "%7B%7D"})
                    bean = f"{table.get('table')}_id"
                elif typezh == "修改":
                    pjson = {}
                    for column in table.get('args'):
                        if column.get('putneed'):
                            argname = column.get('name')
                            argtype = column.get('type')
                            pjson[argname] = random_arg(argtype)
                elif typezh == "删除":
                    pjson = {"ids":[1,2]}
                pjsonstr = json.dumps(pjson)
                # pjsonstr = html.escape(pjsonstr)
                if p == '/<id>':
                    id = random_arg("int")
                    path += f'/id'
                else:
                    id = False
                    path += p
                single_api = single_str(zh, typezh, host, port, protocol, path, method, pjsonstr, tablename, id, app,
                                        query)
                r["item"].append(single_api)

    js = json.dumps(r)

    w.write(js)
    w.close()


def single_str(zh, typezh, host, port, protocol, path, method, pjson, tablename, id, appname, query):
    # print(zh, path, method, pjson)
    item = {
        "name": zh + typezh,
        "request": {
            "method": method,
            "header": [],
            "body": {
                "mode": "raw",
                "raw": pjson,
                "options": {
                    "raw": {
                        "language": "json"
                    }
                }
            },
            "url": {
                "raw": f"{protocol}://{host}:{port}{path}?token={{token}}",
                "protocol": protocol,
                "host": [
                    host
                ],
                "port": port,
                "path": [
                    "api",
                    "v1",
                    appname,
                    tablename,
                ],
                "query": query,
            }
        },
        "response": []
    }
    if id:
        item['request']['url']['path'].append(id)
    if typezh == "列表":
        item['request']['url']['path'].append('list')
    return item


def random_arg(type):
    if type == 'str':
        return ''.join(random.sample(string.ascii_letters + string.digits, 8))
    elif type == "float":
        return round(random.uniform(1, 100), 3)
    elif type == "bool":
        return random.randint(0, 1)
    elif type == "int":
        return random.randint(0, 5)
