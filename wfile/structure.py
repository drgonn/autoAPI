import os
from tools import Tdb


#用来写部署文档
def write_deploy(root,ojson):
    app = ojson.get('app')
    databases = ojson.get('databases')
    modeldir = os.path.join(root,f'{app}/doc/deploy.md')
    w = open(modeldir,'w+')
    w.write(f"#{app}部署环境变量\n")
    w.write("```javascript\n")

    for config in ojson.get('configs'):
        if config.get('deploy'):
            w.write(f"{config.get('arg')}: {config.get('default')}\n")

    w.write("```\n")
    w.close()



#用来写表结构的plantuml文件
def write_model_doc_plant(root,ojson):
    app = ojson.get('app')
    databases = ojson.get('databases')
    modeldir = os.path.join(root,f'{app}/doc/表结构.plantuml')
    w = open(modeldir,'w+')

    # w.write(f"#{app}数据\n")
    # w.write(f"##database名\n")
    # w.write(f"###{ojson.get('dataname')}\n")
    # w.write(f"##表结构\n")
    # w.write(f"```mermaid\n")
    w.write(f"@startuml\n")



    for table in databases:
        tableclass = table.get('table')
        zh  = table.get('zh')
        # w.write(f"{tableclass}[{zh}({tableclass})]\n")
        w.write(f"Class {tableclass} {{\n")
        w.write(f"\t--{zh}--\n")
        for arg in table.get('args'):
            w.write(f"\t{arg.get('name')}-{arg.get('type')}-{arg.get('zh')}\n")

        w.write(f"}}\n")
        # if table.get("many"):
        #     for many in table.get('many'):
        #         manyclass = many.get('name')
        #         w.write(f"{tableclass}-->{manyclass}\n")
        #         w.write(f"{manyclass}-->{tableclass}\n")
        for parent in table.get('parents'):
            parentname = parent.get('name')
            w.write(f"{tableclass} }}-- {parentname}\n")
        if table.get('many'):
            for parent in table.get('many'):
                parentname = parent.get('name')
                w.write(f"{tableclass} }}-- {parentname}\n")
                w.write(f"{parentname} }}-- {tableclass}\n")

    w.write(f"@enduml\n")
    w.close()


