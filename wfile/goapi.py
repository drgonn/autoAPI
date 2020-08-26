import os

from tools import Tdb



def write_goapis(root,ojson):
    app = ojson.get('app')
    appdir = os.path.join(root, f'{app}/go/src')
    host = ojson.get("host")
    appname = ojson.get("name")
    for table in ojson.get('databases'):
        if not table.get('api'):
            continue
        tableclass = table.get('table')
        tablenames = table.get('table').lower() + 's'
        tablename = table.get('table').lower()
        apifile = table.get('table')
        zh = table.get('zh')
        apidir = os.path.join(appdir,f'z{apifile}.go')

        sons = []
        for stable in ojson.get('databases'):
            for parent in stable.get('parents'):
                parentname = parent.get('name')
                if parentname == tableclass:
                    sons.append(stable.get('table'))



        w = open(apidir,'w+')
        im = """package main

"""
        w.write(im)
        w.write('import (\n')
        w.write('\t"github.com/gin-gonic/gin"\n')
        w.write('\t"net/http"\n')
        # w.write('\t"strconv"\n')
        w.write('\t"strings"\n')

        ipt_time = False
        for column in table.get('args'):
            if column.get('type') == 'time':
                ipt_time = True
        if ipt_time:
            w.write('\t"time"\n')
        w.write(')\n')



        w.write(f'func fetchSingle{tableclass}(c *gin.Context){{\n')
        w.write(f'\tvar {tablename} {tableclass}\n')
        w.write(f'\t{tablename}ID := c.Param("id")\n')
        w.write(f'\tdb.First(&{tablename}, {tablename}ID)\n')
        w.write(f'\tif {tablename}.ID == 0 {{\n')
        w.write(f'\t\tc.JSON(http.StatusNotFound, gin.H{{"success": false, "error_code":-4, "errmsg": "No {tablename} found!"}})\n')
        w.write(f'\t\treturn\n')
        w.write(f'\t}}\n')
        w.write(f'\t_{tablename} :=  json{tableclass}{{\n')
        w.write(f'\t\tID : {tablename}.ID,\n')
        for arg in table.get('args'):
            w.write(f'\t\t{arg.get("name").title()} : {tablename}.{arg.get("name").title()},\n')
        w.write(f'\t}}\n')
        w.write(f'\tc.JSON(http.StatusOK, gin.H{{"success": true, "error_code":0, "data": _{tablename}}})\n')
        w.write('}\n')
        w.write('\n')

        # for column in table.get('args'):
        #     argname = column.get('name')
        #
        # w.write(f"@api.route('/{tablename}/<int:id>', methods=['GET'])\n")
        # w.write(f"def get_{tablename}(id):\n")
        # w.write(f"\t{tablename} = {tableclass}.query.get_or_404(id)\n")
        # to_what = 'to_json' #if table.get('nodetail') else 'to_detail'
        #
        # w.write(f"""\n\treturn jsonify({{'success':True,
        #             'error_code':0,
        #             'records':{tablename}.{to_what}(),
        #             }})""")
        # w.write(f"\n\n")





        w.write(f'func create{tableclass}(c *gin.Context){{\n')
        w.write(f'\tvar {tablename} json{tableclass}\n')
        w.write(f'\terr := c.BindJSON(&{tablename})\n')
        w.write(f'\tswitch {{\n')
        w.write(f'\tcase err != nil:\n')
        w.write(f'\t\tc.JSON(200,gin.H{{"success":false,"error_code": -1,"errmsg":"Post data err"}})\n')
        w.write(f'\t\treturn\n')
        for arg in table.get('args'):
            if arg.get('postmust'):
                tp = arg.get('type')
                emptyStr = Tdb(tp).empty
                w.write(f'\tcase {tablename}.{arg.get("name").title()} == {emptyStr}:\n')
                w.write(f'\t\tc.JSON(200,gin.H{{"success":false,"error_code": -1,"errmsg":"{arg.get("name")} 参数缺失"}})\n')
                w.write(f'\t\treturn\n')

        for parent in table.get('parents'):
            parentname = parent.get('name')
            if parent.get('postmust'):
                w.write(f'\tcase {tablename}.{parentname}ID == 0:\n')
                w.write(f'\t\tc.JSON(200,gin.H{{"success":false,"error_code": -1,"errmsg":"{parentname}ID 参数缺失"}})\n')
                w.write(f'\t\treturn\n')
        w.write('\t}\n')

        for arg in table.get('args'):
            if arg.get('unique'):
                aname = arg.get('name')
                w.write(f'\tvar query{tableclass} {tableclass}\n')
                w.write(f'\tdb.Where("{aname} = ?", {tablename}.{aname.title()}).First(&query{tableclass})\n')
                w.write(f'\tif query{tableclass}.ID != 0 {{\n')
                w.write(f'\t\tc.JSON(http.StatusNotFound, gin.H{{"success": false, "error_code":-4, "errmsg": "{tableclass} {aname} 已经存在，不允许重复"}})\n')
                w.write(f'\t\treturn\n')
                w.write(f'\t}}\n')

        for parent in table.get('parents'):
            parentname = parent.get('name')
            parenttablename = parentname.lower()
            if parent.get('name') == 'User':
                pass
            elif parent.get('postmust'):
                index = parent.get('index')
                argname = f"{parenttablename}{parent.get('index').capitalize()}"
                w.write(f'\tvar {parentname.lower()} {parentname}\n')
                w.write(f'\t{parentname.lower()}ID := {tablename}.{parentname}ID\n')
                w.write(f'\tdb.First(&{parentname.lower()}, {parentname.lower()}ID)\n')
                w.write(f'\tif {parentname.lower()}.ID == 0 {{\n')
                w.write(f'\t\tc.JSON(http.StatusNotFound, gin.H{{"success": false, "error_code":-4, "errmsg": "No {parentname} found!"}})\n')
                w.write(f'\t\treturn\n')
                w.write(f'\t}}\n')

        w.write(f'\tdb{tableclass} := {tableclass}{{\n')
        for column in table.get('args'):
            if column.get('need'):
                w.write(f'\t\t{column.get("name").title()} : {tablename}.{column.get("name").title()},\n')
            if column.get("name") == "create_time":
                w.write(f'\t\t{column.get("name").title()} : time.Now(),\n')
            if column.get("name") == "update_time":
                w.write(f'\t\t{column.get("name").title()} : time.Now(),\n')

        for parent in table.get('parents'):
            parentname = parent.get('name')
            parenttablename = parentname.lower()
            if parent.get('name') == 'User':
                pass
                # w.write(f"\t{parenttablename} = g.current_user\n ")
            elif parent.get('need'):
                index = parent.get('index')
                argname = f"{parenttablename}{parent.get('index').capitalize()}"
                w.write(f'\t\t{parentname}ID : {tablename}.{parentname}ID,\n')
        w.write(f'\t}}\n')
        w.write(f'\tdb.Save(&db{tableclass})\n')
        w.write(f'\tc.JSON(http.StatusCreated,gin.H{{\n')
        w.write(f'\t\t"success":true,\n')
        w.write(f'\t\t"error_code": 0,\n')
        w.write(f'\t\t"id":db{tableclass}.ID, \n')
        w.write('\t})\n')
        w.write('}\n\n')



#         if table.get("many"):
#             for many in table.get('many'):
#                 manyclass = many.get('name')
#                 manyname = many.get('name').lower()
#                 w.write(f"\n\t{manyname}_ids = request.json.get('{manyname}_ids') or []\n")
#                 w.write(f"\tfor {manyname}_id in {manyname}_ids:\n")
#                 w.write(f"\t\t{manyname} = {manyclass}.query.filter_by(id={manyname}_id)\n")
#                 w.write(f"\t\tif {manyname} is None:\n")
#                 w.write(f"\t\t\treturn jsonify({{'success':False,'error_code':-1,'errmsg':'{manyname}ID不存在'}})\n")
#                 w.write(f"\t\t{tablename}.{manyname}s.append({manyname})\n")
#                 w.write(f"\t\n")
#
#         w.write(f"\n\tdb.session.add({tablename})\n")
#         w.write(f"\ttry:\n\t\tdb.session.commit()\n\texcept Exception as e:\n\t\tdb.session.rollback()\n")
#         w.write(f"\t\tlogging.error(f'添加数据库发生错误,已经回退:{{e}}')\n")
#         w.write(f"\t\treturn jsonify({{'success': False, 'error_code': -123, 'errmsg': '数据库插入错误，请查看日志'}})\n")
#         w.write(f"""\n\treturn jsonify({{'success':True,
#                     'error_code':0,
#                     }})""")
#         w.write(f"\n\n")
#



        w.write(f'func update{tableclass}(c *gin.Context){{\n')
        w.write(f'\tvar {tablename} {tableclass}\n')
        w.write(f'\t{tablename}ID := c.Param("id")\n')
        w.write(f'\tdb.First(&{tablename}, {tablename}ID)\n')
        w.write(f'\tif {tablename}.ID == 0 {{\n')
        w.write(f'\t\tc.JSON(http.StatusNotFound, gin.H{{"success": false, "error_code":-4, "errmsg": "No {tablename} found!"}})\n')
        w.write(f'\t\treturn\n')
        w.write(f'\t}}\n')

        w.write(f'\tvar j{tablename} json{tableclass}\n')
        w.write(f'\terr := c.BindJSON(&j{tablename})\n')
        w.write(f'\tswitch {{\n')
        w.write(f'\tcase err != nil:\n')
        w.write(f'\t\tc.JSON(200,gin.H{{"success":false,"error_code": -1,"errmsg":"Post data err"}})\n')
        w.write(f'\t\treturn\n')
        w.write('\t}\n')

        for parent in table.get('parents'):
            parentname = parent.get('name')
            parenttablename = parentname.lower()
            if parent.get('name') == 'User':
                pass
            elif parent.get('putneed'):
                index = parent.get('index')
                argname = f"{parenttablename}{parent.get('index').capitalize()}"
                w.write(f'\tif j{tablename}.{parentname}ID != 0 {{\n')
                w.write(f'\t\tvar {parentname.lower()} {parentname}\n')
                w.write(f'\t\t{parentname.lower()}ID := j{tablename}.{parentname}ID\n')
                w.write(f'\t\tdb.First(&{parentname.lower()}, {parentname.lower()}ID)\n')
                w.write(f'\t\tif {parentname.lower()}.ID == 0 {{\n')
                w.write(f'\t\t\tc.JSON(http.StatusNotFound, gin.H{{"success": false, "error_code":-4, "errmsg": "No {parentname} found!"}})\n')
                w.write(f'\t\t\treturn\n')
                w.write(f'\t\t}}\n')
                w.write(f'\tdb.Model(&{tablename}).Update("{parentname.lower()}ID",{tablename}.{parentname}ID)\n')
                w.write(f'\t}}\n')



        for column in table.get('args'):
            if column.get('putneed'):
                columnname = column.get("name").title()
                tp = column.get('type')
                emptyStr = Tdb(tp).empty
                w.write(f'\tif j{tablename}.{columnname} != {emptyStr} {{\n')
                if column.get('unique'):
                    w.write(f'\t\tvar query{tableclass} {tableclass}\n')
                    w.write(f'\t\tdb.Where("{columnname} = ?", j{tablename}.{columnname}).First(&query{tableclass})\n')
                    w.write(
                        f'\t\tif query{tableclass}.ID != 0 && query{tableclass}.{columnname} != {tablename}.{columnname} {{\n')
                    w.write(
                        f'\t\t\tc.JSON(http.StatusNotFound, gin.H{{"success": false, "error_code":-4, "errmsg": "{tableclass} {columnname} 已经存在，不允许重复"}})\n')
                    w.write(f'\t\t\treturn\n')
                    w.write(f'\t\t}}\n')
                w.write(f'\t\tdb.Model(&{tablename}).Update("{columnname}",j{tablename}.{columnname})\n')
                w.write(f'\t}}\n')
            if column.get("name") == "update_time":
                w.write(f'\tdb.Model(&{tablename}).Update("Update_Time",time.Now())\n')
        w.write(f'\tc.JSON(http.StatusCreated,gin.H{{\n')
        w.write(f'\t\t"success":true,\n')
        w.write(f'\t\t"error_code": 0,\n')
        w.write(f'\t\t"id":{tablename}.ID, \n')
        w.write('\t})\n')
        w.write('}\n\n')





#         if table.get("many"):
#             for many in table.get('many'):
#                 manyclass = many.get('name')
#                 manyname = many.get('name').lower()
#                 w.write(f"\n\t{manyname}_ids = request.json.get('{manyname}_ids') or []\n")
#                 w.write(f"\toriginal_ids = [{manyname}.id for {manyname} in {tablename}.{manyname}s.all()]\n")
#                 w.write(f"\tnew_ids = list(set({manyname}_ids).difference(set(original_ids)))\n")
#                 w.write(f"\told_ids = list(set(original_ids).difference(set({manyname}_ids)))\n")
#                 w.write(f"\tfor {manyname}_id in new_ids:\n")
#                 w.write(f"\t\t{manyname} = {manyclass}.query.filter_by(id={manyname}_id)\n")
#                 w.write(f"\t\tif {manyname} is None:\n")
#                 w.write(f"\t\t\treturn jsonify({{'success':False,'error_code':-1,'errmsg':'{manyname}ID不存在'}})\n")
#                 w.write(f"\t\t{tablename}.{manyname}s.append({manyname})\n")
#                 w.write(f"\tfor {manyname}_id in old_ids:\n")
#                 w.write(f"\t\t{manyname} = {manyclass}.query.filter_by(id={manyname}_id)\n")
#                 w.write(f"\t\t{tablename}.{manyname}s.remove({manyname})\n")
#                 w.write(f"\t\n")
#

        w.write(f'func delete{tableclass}(c *gin.Context){{\n')
        w.write(f'\tvar {tablename} {tableclass}\n')
        w.write(f'\t{tablename}ID := c.Param("id")\n')
        w.write(f'\tdb.First(&{tablename}, {tablename}ID)\n')
        w.write(f'\tif {tablename}.ID == 0 {{\n')
        w.write(f'\t\tc.JSON(http.StatusNotFound, gin.H{{"success": false, "error_code":-4, "errmsg": "No {tablename} found!"}})\n')
        w.write(f'\t\treturn\n')
        w.write(f'\t}}\n')
        for son in sons:
            w.write(f'\tvar {son.lower()} {son}\n')
            w.write(f'\tdb.Where("{tablename}ID",{tablename}.ID).First(&{son.lower()})\n')
            w.write(f'\tif {son.lower()}.ID != 0 {{\n')
            w.write(
                f'\t\tc.JSON(http.StatusNotFound, gin.H{{"success": false, "error_code":-4, "errmsg": "{tablename}还拥有{son.lower()}，不能删除"}})\n')
            w.write(f'\t\treturn\n')
            w.write(f'\t}}\n')
        w.write(f'\tdb.Delete(&{tablename})\n')
        w.write(f'\tc.JSON(http.StatusCreated,gin.H{{\n')
        w.write(f'\t\t"success":true,\n')
        w.write(f'\t\t"error_code": 0,\n')
        w.write('\t})\n')
        w.write('}\n\n')







        w.write(f'type page{tableclass} struct {{\n')
        w.write('\tPageindex int `json:"current"`\n')
        w.write('\tPagesize int `json:"pagesize"`\n')
        w.write('\tOrder int `json:"order"`\n')
        w.write('\tSortfield string `json:"sortfield"`\n')
        w.write(f'\tjson{tableclass}\n')
        w.write('\t}\n\n')
        w.write(f'type rpage{tableclass} struct {{\n')
        w.write('\tPageindex int `json:"current"`\n')
        w.write('\tPagesize int `json:"pagesize"`\n')
        w.write('\tPagecount int `json:"pagecount"`\n')
        w.write('\tTotalcount int `json:"totalcount"`\n')
        w.write(f'\tRecords []json{tableclass} `json:"records"`\n')
        w.write('\t}\n\n')

        w.write(f'func fetchPage{tableclass}(c *gin.Context){{\n')
        w.write(f'\tvar totalcount int\n')
        w.write(f'\tvar pagecount int\n')
        w.write(f'\tvar {tablename} page{tableclass}\n')
        w.write(f'\tvar _j{tableclass}s []json{tableclass}\n')
        w.write(f'\tDb := db\n')
        w.write(f'\titem{tableclass}s := make([]{tableclass},0)\n')
        w.write(f'\terr := c.BindJSON(&{tablename})\n')
        w.write(f'\tswitch {{\n')
        w.write(f'\tcase err != nil:\n')
        w.write(f'\t\tc.JSON(200,gin.H{{"success":false,"error_code": -1,"errmsg":"Post data err"}})\n')
        w.write(f'\t\treturn\n')

        w.write(f'\tcase {tableclass.lower()}.Pageindex == 0:\n')
        w.write(f'\t\t{tableclass.lower()}.Pageindex = 1\n')
        w.write(f'\t\tfallthrough\n')
        w.write(f'\tcase {tableclass.lower()}.Pagesize == 0:\n')
        w.write(f'\t\t{tableclass.lower()}.Pagesize = 20\n')
        w.write('\t}\n')



        for parent in table.get('parents'):
            parentname = parent.get('name')
            parenttablename = parentname.lower()
            if parent.get('name') == 'User':
                pass
            else:
                index = parent.get('index')
                argname = f"{parenttablename}{parent.get('index').capitalize()}"
                w.write(f'\tif {tablename}.{parentname}ID != 0 {{ \n')
                w.write(f'\t\tvar {parentname.lower()} {parentname}\n')
                w.write(f'\t\t{parentname.lower()}ID := {tablename}.{parentname}ID\n')
                w.write(f'\t\tdb.First(&{parentname.lower()}, {parentname.lower()}ID)\n')
                w.write(f'\t\tif {parentname.lower()}.ID == 0 {{\n')
                w.write(f'\t\t\tc.JSON(http.StatusNotFound, gin.H{{"success": false, "error_code":-4, "errmsg": "No {parentname} found!"}})\n')
                w.write(f'\t\treturn\n')
                w.write(f'\t\t}} else {{\n')
                w.write(f'\t\t\tDb = Db.Where("{parentname.lower()}ID = ?",{tablename}.{parentname}ID)\n')
                w.write(f'\t\t}}\n')
                w.write(f'\t}}\n')


        for column in table.get('args'):
            tp = column.get('type')
            emptyStr = Tdb(tp).empty
            if column.get('need') or column.get('listneed'):
                argname = column.get('name')
                if column.get('type') in ['int','str']:
                    w.write(f"\tif {tablename}.{argname.title()} != {emptyStr} {{\n")
                    if column.get('like'):
                        w.write(f'\t\t\tDb = Db.Where("{argname} LIKE ?","%"+{tablename}.{argname.title()}+"%")\n')
                    else:
                        w.write(f'\t\t\tDb = Db.Where("{argname} = ?","{tablename}.{argname.title()}")\n')
                    w.write('\t}\n\n')

        w.write(f'\tif {tablename}.Sortfield != "" {{\n')
        w.write('\t\tvar build strings.Builder\n')
        w.write(f'\t\tbuild.WriteString({tablename}.Sortfield)\n')
        w.write(f'\t\tif {tablename}.Order == 0 {{\n')
        w.write(f'\t\t\tbuild.WriteString(" desc")\n')
        w.write(f'\t\t}} else {{\n')
        w.write(f'\t\t\tbuild.WriteString(" asc")\n')
        w.write(f'\t\t}}\n')
        w.write('\torderstr := build.String()\n')
        w.write(f'\tDb = Db.Order(orderstr)\n')
        w.write('\t}\n')

        w.write(f"\tif err := Db.Find(&item{tableclass}s).Count(&totalcount).Error; err != nil{{\n")
        w.write(
            f'\t\tc.JSON(http.StatusNotFound, gin.H{{"success": false, "error_code":-4, "errmsg": "{tableclass} 表数据查询错误"}})\n')
        w.write(f'\t\treturn\n')
        w.write('\t}\n\n')


        w.write(f'\tif {tablename}.Pagesize > totalcount {{ \n')
        w.write('\t\tpagecount = 1 \n')
        w.write('\t} else {\n')
        w.write(f'\t\tvar yu int\n')
        w.write(f'\t\tif  totalcount  % {tablename}.Pagesize == 0{{ \n')
        w.write(f'\t\t\tyu = 0\n')
        w.write(f'\t\t}} else{{ \n')
        w.write(f'\t\t\tyu = 1 \n')
        w.write(f'\t\t}} \n')
        w.write(f'\t\tpagecount = totalcount / {tablename}.Pagesize + yu\n')
        w.write('\t}\n')



        w.write(f"\tDb = Db.Limit({tablename}.Pagesize).Offset(({tablename}.Pageindex - 1)* {tablename}.Pagesize)\n")

        w.write(f"\tif err := Db.Find(&item{tableclass}s).Error; err != nil{{\n")
        w.write(
            f'\t\tc.JSON(http.StatusNotFound, gin.H{{"success": false, "error_code":-4, "errmsg": "{tableclass} 表数据查询错误"}})\n')
        w.write(f'\t\treturn\n')
        w.write('\t}\n\n')

        w.write(f'\tfor _, item := range item{tableclass}s {{\n')
        for parent in table.get('parents'):
            parentclass = parent.get('name')
            parentname = parentclass.lower()
            pname = parent.get('tojson')
            if pname is not None:
                w.write(f'\t\tvar {parentname} {parentclass}\n')
                w.write(f'\t\tdb.First(&{parentname},item.{parentclass}ID)\n')

        w.write(f'\t\t_j{tableclass}s = append(_j{tableclass}s, json{tableclass}{{\n')

        w.write(f"\t\t\tID : item.ID,\n")
        for column in table.get('args'):
            name = column.get('name')
            w.write(f'\t\t\t{name.title()} : item.{name.title()},\n')
        for parent in table.get('parents'):
            parentname = parent.get('name')
            w.write(f'\t\t\t{parentname}ID : item.{parentname}ID,\n')
            pname = parent.get('tojson')
            if pname is not None:
                w.write(f'\t\t\t{parentname}{pname.title()} : {parentname.lower()}.{pname.title()},\n')
        w.write('\t\t})\n')
        w.write('\t}\n')


        w.write(f'\t_page := rpage{tableclass}{{\n')
        w.write(f'\t\tPageindex : {tablename}.Pageindex,\n')
        w.write(f'\t\tPagesize : {tablename}.Pagesize,\n')
        w.write(f'\t\tPagecount : pagecount,\n')
        w.write(f'\t\tTotalcount : totalcount,\n')
        w.write(f'\t\tRecords : _j{tableclass}s,\n')
        w.write(f'\t}}\n')

        w.write(f'\tc.JSON(http.StatusCreated,gin.H{{\n')
        w.write(f'\t\t"success":true,\n')
        w.write(f'\t\t"error_code": 0,\n')
        w.write(f'\t\t"data": _page,\n')
        w.write('\t})\n')
        w.write('}\n\n')


def write_goapi_init(root,ojson):
    app = ojson.get('app')
    appdir = os.path.join(root, f'{app}/go/src')
    apidir = os.path.join(appdir, f'main.go')
    w = open(apidir, 'w+')
    im = """package main
    """
    w.write(im)
    w.write('\nimport (\n')
    w.write('\t"github.com/gin-gonic/gin"\n')
    w.write('\t_ "github.com/jinzhu/gorm/dialects/mysql"\n')
    w.write(')\n\n')
    w.write('func main() {\n')
    w.write('\tr := gin.Default()\n')
    w.write('\tr.Use(BeforeRequest())\n')
    w.write(f'\tv1 := r.Group("/api/v1/{app}")\n')
    w.write('\t{\n')
    for table in ojson.get('databases'):
        if not table.get('api'):
            continue
        tableclass = table.get('table')
        tablename = table.get('table').lower()

        w.write(f'\t\tv1.GET("/{tablename}/:id",fetchSingle{tableclass})\n')
        w.write(f'\t\tv1.POST("/{tablename}/",create{tableclass})\n')
        w.write(f'\t\tv1.PUT("/{tablename}/:id",update{tableclass})\n')
        w.write(f'\t\tv1.DELETE("/{tablename}/:id",delete{tableclass})\n')
        w.write(f'\t\tv1.POST("/{tablename}/list",fetchPage{tableclass})\n')

    w.write('\t}\n')
    w.write('\tr.Run("localhost:20303")\n')
    w.write('}\n')
