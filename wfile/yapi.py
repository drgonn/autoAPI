import os
import random
import json
import string
import html
import urllib
from tools import Tdb

def write_yapi(root, ojson):
    app = ojson.get('app')
    host = ojson.get("testhost")  #
    port = ojson.get("testport")  #
    protocol = ojson.get("testprotocol")  #
    r = []

    testdoc = os.path.join(root, f'{app}/test/yapi_reset.json')
    w = open(testdoc, 'w+')
    crud = [
        ("创建", "POST", '', False),
            ("列表", "GET", '/list', '$.data.records[-1].id'),
            ("单个获取", "GET", '/<id>', False),
            ("修改", "PUT", '/<id>', False),
            ("删除", "DELETE", '', False),
            ]
    for table in ojson.get('databases'):
        if table.get('api'):
            zh = table.get('zh')
            tablename = table.get("table").lower()
            gp = {}
            gp['index'] = 0
            gp['name'] = zh
            gp['desc'] = zh
            gp['list'] = []
            # gp[''] = 0
            for typezh, method, p, argaddr in crud:
                path = f"/api/v1/{app}/{tablename}"
                bean = False
                pjson = {}
                query = [{
                    "key": "token",
                    "value": "{{token}}"
                }
                ]
                pjson = {"type":"object",
                        "title":"empty object",
                        "properties":
                            {

                            },
                        "required":[]
                        }
                a = {"$schema":"http://json-schema.org/draft-04/schema#",
                     "type":"object",
                     "properties":
                         {"name":{"type":"string","description":"省名称"}},
                     "required":["name"]
                     }

                listjson = {"type": "object",
                     "title": "empty object",
                     "properties":
                         {"success":
                              {"type": "boolean",
                               "description": "返回成功",
                               "mock": {"mock": "true"}
                               },
                          "data":
                              {"type": "array",
                               "items":
                                   {"type": "object",
                                    "properties": {
                                        "id": {"type": "integer", "description": "id"},
                                    },
                                    "required": ["id"]},
                               "description": "数据列表"}
                          },
                     "required":["success", "data"]
                     }
                getjson = {"type": "object",
                            "title": "empty object",
                            "properties":
                                {"success":
                                     {"type": "boolean",
                                      "description": "返回成功",
                                      "mock": {"mock": "true"}
                                      },
                                 "record":
                                      {"type": "object",
                                       "properties": {
                                           "id": {"type": "integer", "description": "id"},
                                       },
                                       "required": ["id"]}
                                 },
                            "required":["success", "record"]
                            }
                sjson = {"type": "object",
                           "title": "empty object",
                           "properties":
                               {
                                   "success":
                                    {"type": "boolean",
                                     "description": "返回成功",
                                     "mock": {"mock": "true"}
                                     },
                                   "error_code":
                                       {"type": "integer",
                                        "description": "错误码",
                                        "mock": {"mock": 0}
                                        },

                           },
                         "required": ["success", "error_code"]
                         }


                if typezh == "创建":
                    pass
                    for column in table.get('args'):
                        if column.get('post'):
                            argname = column.get('name')
                            argmean = column.get('mean')
                            argtype = column.get('type')
                            ytype = Tdb(argtype).db.lower()
                            pjson["properties"][argname] = {"type":ytype,"description":argmean}
                            if column.get("post") == 2:
                                pjson["required"].append(argname)
                    rstr = json.dumps(sjson)

                    for column in table.get('parents'):
                        if column.get('postmust') and column.get('name') != 'User':
                            argname = column.get('name').lower() + "_id"
                            argtype = column.get('type')
                            argmean = column.get('mean')
                            pjson["properties"][argname] = {"type":"integer","description":argmean}

                elif typezh == "单个获取":
                    pjson["properties"]['current'] = {"type":"integer","description":"访问页"}
                    pjson["properties"]['pageSize'] = {"type":"integer","description":"单页条数"}
                    for column in table.get('args'):
                        if column.get('post'):
                            argname = column.get('name')
                            argmean = column.get('mean')
                            argtype = column.get('type')
                            ytype = Tdb(argtype).db.lower()
                            getjson["properties"]['record']["properties"][argname]= {"type": ytype, "description": zh+argmean}
                            getjson["properties"]['record']["required"].append(argname)
                    getjson["properties"]['record']["required"].append("token")
                    rstr = json.dumps(getjson)

                elif typezh == "列表":
                    sorter = {}
                    # sorter = urllib.parse.urlencode({})
                    pjson["properties"]['current'] = {"type": "integer", "description": "访问页"}
                    pjson["properties"]['pageSize'] = {"type": "integer", "description": "单页条数"}
                    pjson["properties"]['token'] = {"type":"string","description":"token"}
                    for column in table.get('args'):
                        if column.get('post'):
                            argname = column.get('name')
                            argmean = column.get('mean')
                            argtype = column.get('type')
                            ytype = Tdb(argtype).db.lower()
                            listjson["properties"]['data']['items']["properties"][argname] = {"type": ytype,"description": zh + argmean}
                            listjson["properties"]['data']['items']["required"].append(argname)
                    rstr = json.dumps(listjson)
                    # query.append({'key':'sorter','value': "%7B%7D"})
                    # bean = f"{table.get('table')}_id"
                elif typezh == "修改":
                    rstr = json.dumps(sjson)
                    for column in table.get('args'):
                        if column.get('putneed'):
                            argname = column.get('name')
                            argtype = column.get('type')
                            pjson[argname] = random_arg(argtype)
                    for column in table.get('args'):
                        if column.get('post'):
                            argname = column.get('name')
                            argmean = column.get('mean')
                            argtype = column.get('type')
                            ytype = Tdb(argtype).db.lower()
                            pjson["properties"][argname] = {"type": ytype, "description": argmean}
                    for column in table.get('parents'):
                        if column.get('postmust') and column.get('name') != 'User':
                            argname = column.get('name').lower() + "_id"
                            argtype = column.get('type')
                            argmean = column.get('mean')
                            pjson["properties"][argname] = {"type": "integer", "description": argmean}

                elif typezh == "删除":
                    rstr = json.dumps(sjson)
                    pjson["properties"]["ids"] = {"type": "array", "description": "要删除的id数组","items":{"type":"integer"}}
                    # pjson = {"ids":[1,2]}
                pjsonstr = json.dumps(pjson)
                # rstr = json.dumps(listjson)
                # pjsonstr = html.escape(pjsonstr)


                if p == '/<id>':
                    id = random_arg("int")
                    path += f'/id'
                else:
                    id = False
                    path += p
                single_api = single_str(zh, typezh, host, port, protocol, path, method, pjsonstr, tablename, id, app,
                                        query,rstr)
                gp["list"].append(single_api)
            r.append(gp)

    js = json.dumps(r)


    w.write(js)
    w.close()
    print(":--yapi运行完成")



def single_str(zh, typezh, host, port, protocol, path, method, pjson, tablename, id, appname, query,rstr):
    # print(zh, path, method, pjson)
    item = {
        "query_path": {
            "path": path,
            "params": []
        },
        "edit_uid": 0,
        "status": "undone",
        "type": "static",
        "req_body_is_json_schema": True,
        "res_body_is_json_schema": True,
        "api_opened": False,
        # "index": 7,
        "tag": [],
        # "_id": 926,
        "title": zh + typezh,
        "path": path,
        "method": method,
        "desc": "",
        "req_query": [
            # {
            #     "required": "0",
            #     "_id": "5fa39b1d6935300090607d79",
            #     "name": "token"
            # }
        ],
        "req_headers": [
            {
                "required": "1",
                "_id": "5fa39b1d6935300090607d7a",
                "name": "Content-Type",
                "value": "application/json"
            }
        ],
        "req_body_type": "json",
        "req_body_form": [],
        "req_body_other": pjson,
        "project_id": 26,
        "catid": 86,
        "req_params": [],
        "res_body_type": "json",
        "uid": 11,
        "add_time": 1604218693,
        "up_time": 1604557597,
        "__v": 0,
        "markdown": "",
        "res_body": rstr
    }

    #
    # if id:
    #     item['request']['url']['path'].append(id)
    # if typezh == "列表":
    #     item['request']['url']['path'].append('list')
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



f={"type":"object",
   "title":"empty object",
   "properties":
       {"success":
            {"type":"boolean",
             "description":"返回成功",
             "mock":{"mock":"true"}
             },
        "data":
            {"type":"array",
             "items":
                 {"type":"object",
                  "properties":{"id":{"type":"integer","description":"省id"},
                                "name":{"type":"string","description":"省名"}},
                  "required":["id","name"]},
             "description":"数据列表"}
        },
   "required":
       ["success","data"]
   }
