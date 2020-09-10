import os
import pprint



def out_detail(tableclass,ojson):
    outdir = {}
    for table in ojson.get('databases'):
        if tableclass == table.get('table'):
            zh = table.get('zh')
            outdir['id']=f'{zh}ID'
            for column in table.get('args'):
                argname = column.get('name')
                argmean = column.get('mean')
                outdir[f"{argname}"]=f"{argmean}"
            if table.get('detail_sons') is not None:
                for son in table.get('detail_sons'):
                    outdir[f"{son.lower()}s"] = [out_detail(son,ojson)]
    return outdir


def write_docs(root,ojson):
    app = ojson.get('app')
    appdir = os.path.join(root, f'{app}/src/app')
    doc = os.path.join(root, f'{app}/doc')
    host = ojson.get("host")
    testhost = ojson.get("testhost")
    appname = ojson.get("app")
    for table in ojson.get('databases'):
        if not table.get('api'):
            continue
        tablename = table.get('table').lower()
        zh = table.get('zh')
        docdir = os.path.join(doc,f'{zh}接口.md')
        d = open(docdir,'w+')

        d.write(f"##{zh}接口\n###1、查看单个{zh}接口")
        d.write(f"""
```javascript
请求方式：GET
请求URL：{host}/api/v1/{appname}/{tablename}/<int:id>
测试URL：{testhost}/api/v1/{appname}/{tablename}/<int:id>
数据格式：JSON
请求说明： 根据{zh}ID查看单个{zh}
```
""")
        d.write("**返回示例**\n> 正常情况下，会返回下述JSON数据包\n")
        d.write("```javascript\n")
        d.write("```javascript\n{\n\t'success': true,\n\t'error_code': 0,\n")
        d.write("\t'records':{\n")
        # outstr = out_detail(tableclass,ojson)
        # outstr['success'] = True
        # outstr['error_code'] = 0
        # pprint.pprint(outstr, d)
        # d.write(outstr)
        for column in table.get('args'):
            argname = column.get('name')
            argmean = column.get('mean')
            d.write(f"\t\t'{argname}':'{argmean}',\n")

        if table.get('detail_sons') is not None:
            for son in table.get('detail_sons'):
                d.write(f"\t\t'{son}s':[{son}.to_detail() for {son} in self.{son}s],\n")

        d.write("\t}\n}\n```\n")

        d.write(f"###2、创建{zh}接口\n")
        d.write(f"""```javascript\n请求方式：POST\n请求URL：{host}/api/v1/{appname}/{tablename}\n""")
        d.write(f"""测试URL：{testhost}/api/v1/{appname}/{tablename}\n""")
        d.write(f"""数据格式：JSON\n请求说明： 创建{zh}\n```\n""")
        d.write("*请求参数说明*\n\n")
        d.write("| 参数  | 类型   | 是否必须 | 说明        |\n")
        d.write("| ----- | ------ | -------- | ----------- |\n")
        for column in table.get('args'):
            if column.get('post'):
                argname = column.get('name')
                argmean = column.get('mean')
                argtype = column.get('type')
                postmust = '是' if column.get('post') == 2 else '否'
                d.write(f"|{argname}|{argtype}|{postmust}|{argmean}|\n")
        for parent in table.get('parents'):
            parentname = parent.get('name')
            pmean = parent.get('mean')
            ptype = parent.get('type')
            postmust = '是' if parent.get('post') == 2 else '否'
            parenttablename = parentname.lower()
            argname = f"{parenttablename}_{parent.get('index')}"
            if parent.get('post'):
                d.write(f"|{argname}|{ptype}|{postmust}|{pmean}|\n")
        if table.get('many'):
            for many in table.get('many'):
                manyclass = many.get('name')
                manyname = many.get('name').lower()
                d.write(f"|{manyname}_ids|List|否|{manyclass}ID列表|\n")
        d.write("\n")
        d.write("**返回示例**\n> 正常情况下，会返回下述JSON数据包\n")
        d.write("```javascript\n{\n\t'success': true,\n\t'error_code': 0\n}\n```\n")



        d.write(f"###3、修改{zh}接口\n")
        d.write(f"""```javascript\n请求方式：PUT\n请求URL：{host}/api/v1/{appname}/{tablename}/<int:id>""")
        d.write(f"""测试URL：{testhost}/api/v1/{appname}/{tablename}/<int:id>\n""")
        d.write(f"""数据格式：JSON\n请求说明： 根据{zh}ID修改{zh}\n```\n""")
        d.write("*请求参数说明*\n\n")
        d.write("| 参数  | 类型   | 是否必须 | 说明        |\n")
        d.write("| ----- | ------ | -------- | ----------- |\n")
        for column in table.get('args'):
            if column.get('putneed'):
                argname = column.get('name')
                argmean = column.get('mean')
                argtype = column.get('type')
                d.write(f"|{argname}|{argtype}|否|{argmean}|\n")
        for parent in table.get('parents'):
            parentname = parent.get('name')
            pmean = parent.get('mean')
            ptype = parent.get('type')
            parenttablename = parentname.lower()
            argname = f"{parenttablename}_{parent.get('index')}"
            if parent.get('putneed'):
                d.write(f"|{argname}|{ptype}|否|{pmean}|\n")
        if table.get('many'):
            for many in table.get('many'):
                manyclass = many.get('name')
                manyname = many.get('name').lower()
                d.write(f"|{manyname}_ids|List|否|{manyclass}ID列表|\n")
        d.write("\n")
        d.write("**返回示例**\n> 正常情况下，会返回下述JSON数据包\n")
        d.write("```javascript\n{\n\t'success': true,\n\t'error_code': 0\n}\n```\n")


        d.write(f"###4、删除{zh}接口\n")
        d.write(f"""```javascript\n请求方式：DELETE\n请求URL：{host}/api/v1/{appname}/{tablename}\n数据格式：JSON\n请求说明： 根据{zh}ID删除{zh}\n```\n""")
        d.write("*请求参数说明*\n\n")
        d.write("| 参数  | 类型   | 是否必须 | 说明        |\n")
        d.write("| ----- | ------ | -------- | ----------- |\n")
        d.write(f"|ids|list|是|要删除的id列表|\n")
        d.write("**返回示例**\n> 正常情况下，会返回下述JSON数据包\n")
        d.write("```javascript\n{\n\t'success': true,\n\t'error_code': 0\n}\n```\n")


        d.write(f"###5、获取{zh}分页列表接口\n")
        d.write(f"""```javascript\n请求方式：GET\n请求URL：{host}/api/v1/{appname}/{tablename}/list\n""")
        d.write(f"""测试URL：{testhost}/api/v1/{appname}/{tablename}/list\n""")
        d.write(f"""```数据格式：JSON\n""")
        d.write(f"""请求说明： 获取{zh}分页列表接口\n```\n""")
        d.write("*请求参数说明*\n\n")
        d.write("| 参数  | 类型   | 是否必须 | 说明        |\n")
        d.write("| ----- | ------ | -------- | ----------- |\n")
        d.write(f"|current|int|否|页位置|\n")
        d.write(f"|pageSize|int|否|单页条数|\n")
        d.write(f"|sorter|object|否|排序参数，格式例如：{{'price':'desend'}}，就是按价格降序|\n")
        for column in table.get('args'):
            if column.get('listneed'):
                if column.get('type') in ['float']:
                    continue
                argname = column.get('name')
                argmean = column.get('mean')
                argtype = column.get('type')
                alistmust = '是' if column.get('listmust') else '否'
                if column.get('like'):
                    d.write(f"|{argname}|{argtype}|{alistmust}|{argmean},支持模糊查找|\n")
                else:
                   d.write(f"|{argname}|{argtype}|{alistmust}|{argmean}|\n")
        for parent in table.get('parents'):
            parentname = parent.get('name')
            pmean = parent.get('mean')
            ptype = parent.get('type')
            plistmust = '是' if parent.get('listmust') else '否'
            parenttablename = parentname.lower()
            argname = f"{parenttablename}_{parent.get('index')}"
            if parent.get('list'):
                d.write(f"|{argname}|{ptype}|{plistmust}|{pmean}|\n")
        d.write("\n")
        d.write("**返回示例**\n> 正常情况下，会返回下述JSON数据包\n")
        d.write("```javascript\n{\n\t'success': true,\n\t'error_code': 0,\n")
        d.write("\t'total':'总条数',\n")
        d.write("\t'data':[\n\t\t{\n")
        d.write(f"\t\t\t'id':'{zh}ID',\n")
        for column in table.get('args'):
            argname = column.get('name')
            argmean = column.get('mean')
            d.write(f"\t\t\t'{argname}':'{argmean}',\n")
        d.write("\t\t},\n\t\t...\n\t]\n\t}\n}\n```\n")


        d.close()
    print(":--doc运行完成")

