新建projects目录下 xxx/doc/xxx.json


运行命令：

创建某项目的flask代码：
python3 run.py -p <项目名称> -m <需要生成的模块名称，不填表示生成全部> 
python3 run.py -p bridge  -m md

-p 项目名称

-m 运行模式 
-m json  默认模式
-m sealan_doc doc转化为对象，然后转化为json，然后转化为对象模式。



├── generatep          生成总p对象的方法目录
├── object             存放各种对象
│   ├── __init__.py
│   ├── api.py         api对象
│   ├── arg.py
│   └── type.py
├── p2doc              将对象转为文档
├── projects           生成的项目存储位置
│   ├── hikv
│   │   ├── doc
│   │   │   ├── hikv.json
│   │   │   ├── mysql.md                                   mysql数据库文档
│   │   │   ├── sealan2doc.json
│   │   │   ├── sealan_doc.md
│   │   │   └── 摄像头模块功能设计说明书-V0.1.0.md
│   │   └── docker-compose.yml
│   └── readme.md
├── reademe.md
├── run.py
└── writefile