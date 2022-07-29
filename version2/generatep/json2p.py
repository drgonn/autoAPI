"""使用json文件生成总对象p"""
import os
import json


from allobject.project import Project
from allobject.api import ResetApiInterface
from allobject.arg import Arg, data_arg, status_out_args, list_arg, page_query_args, page_return_args
from allobject.data_type import DataType
from allobject.column import Column

# from allobject. import 

              

def json2project(appName, projects_dir):
    """使用json文件生成总对象p
    appName: app名
    projects_dir: 存放生成项目文件的目录
    """
    root_dir = os.path.join(projects_dir, appName)
    print("项目目录是：", root_dir)
    doc_json_dir = os.path.join(root_dir, "doc", f"{appName}.json")
    print("源json文件位置是：", doc_json_dir)
    # 查询该目录下的json文件
    if not os.path.exists(doc_json_dir):
        print(doc_json_dir, "json文件不存在")
        os.abort()

    # 将源json文件读取出来为一个对象 project_json
    with open(doc_json_dir, encoding='utf-8') as ff:
        project_json = json.load(ff)
    if project_json is None:
        os.abort("json文件导入失败")

    # 1 生成接口对象
    apiInterfaces = []    # 所有接口对象列表
    blue_path = project_json.get("blue_path")
    tables = project_json.get("databases")
    
    # 生成table部分
    for table_json in tables:
        create_input_args = []            # 创建提交参数
        get_args = []                     # 返回的详情参数,只包含数据部分
        update_input_args = []            #indexindex参数
        index_arg = None                # 索引参数
        list_input_args = []              # 提交参数
        delete_arg = []             # 提交参数
        delete_args = []            # 提交参数
        
        table_index_name=table_json.get("index")
        
        # 将表内的所有参数生成对象
        for arg_json in table_json.get("args"):
            # column_class = Column(
            #     arg_json.get('name'),
            #     arg_json.get('type'),
            #     arg_json.get('length'),
            #     arg_json.get('post'),
            #     arg_json.get('put'),
            #     arg_json.get('list'),
            #     arg_json.get('about'),
            #     arg_json.get('sorter'),
            #     arg_json.get('zh'),
            #     arg_json.get('unique'),
            #     arg_json.get('mapping'),
            #     arg_json.get('index'),
            #     arg_json.get('not_null'),
            #     arg_json.get("default")
            # )
            get_args.append(
                Arg(
                    zh_name=arg_json.get("zh"),
                    name=arg_json.get('name'),
                    type=arg_json.get('type'),
                    about= arg_json.get('about'),
                    unique=arg_json.get('unique'),
                    default=arg_json.get("default"),
                    required=True
                )
            )
            if arg_json.get("post"):
                create_input_args.append(
                    Arg(
                        zh_name=arg_json.get("zh"),
                        name=arg_json.get('name'),
                        type=arg_json.get('type'),
                        about= arg_json.get('about'),
                        unique=arg_json.get('unique'),
                        default=arg_json.get("default"),
                        required=True if arg_json.get("post") == 2 else False
                    )
                )
            if arg_json.get("put"):
                update_input_args.append(
                    Arg(
                        zh_name=arg_json.get("zh"),
                        name=arg_json.get('name'),
                        type=arg_json.get('type'),
                        about= arg_json.get('about'),
                        unique=arg_json.get('unique'),
                        default=arg_json.get("default"),
                        required=True if arg_json.get("put") == 2 else False
                    )
                )

            if arg_json.get("list"):
                list_input_args.append(
                    Arg(
                        zh_name=arg_json.get("zh"),
                        name=arg_json.get('name'),
                        type=arg_json.get('type'),
                        about= arg_json.get('about'),
                        unique=arg_json.get('unique'),
                        default=arg_json.get("default"),
                        required=False
                    )
                )
            if arg_json.get("name") == table_index_name:
                index_arg = Arg(
                        zh_name=arg_json.get("zh"),
                        name=arg_json.get('name'),
                        type=arg_json.get('type'),
                        about= arg_json.get('about'),
                        unique=arg_json.get('unique'),
                        default=arg_json.get("default"),
                        required=True
                    )
        if index_arg == None:
            print("表缺少索引")     

        curds = table_json.get("curds") or ["c", "u", "r", "d", "rs", "ds"]
        for curd in curds:
            interface = ResetApiInterface(
                    curd=curd,
                    blue_path=blue_path,
                    path_prefix=table_json.get("path_prefix"),
                    index_arg=table_json.get("index"),
                    zh_table_name=table_json.get("zh"),
                    table_name=table_json.get("name"),
                )
            if curd == "c":
                interface.input_args = create_input_args
                interface.out_args = status_out_args + [data_arg] + get_args
            elif curd == "u":
                interface.path_args = [index_arg]
                interface.input_args = update_input_args
                interface.out_args = status_out_args
            elif curd == "rs":
                interface.input_args = page_query_args + list_input_args
                interface.out_args = page_return_args + [list_arg] + get_args
            elif curd == "r":
                interface.path_args = [index_arg]
                interface.out_args = status_out_args + [data_arg] + get_args
            elif curd == "d":
                interface.path_args = [index_arg]
                interface.out_args = status_out_args




            apiInterfaces.append(interface)





    p = Project(
        name= appName,
        zh=project_json.get("zh"),
        app_root_dir=root_dir)

    # print("apiInterfaces",apiInterfaces)
    p.apis = apiInterfaces

    return p



