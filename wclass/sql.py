"""写入配置环境的class"""


class Sql(object):
    def __init__(self,  sql_dir):
        sql_dir = sql_dir or {}
        self.local_port = sql_dir.get("local_port")   # 本地宿主机sql的访问port:3307
        self.docker_name = sql_dir.get("docker_name")  # docker的访问名称:mariadb2
        self.name = sql_dir.get("name")                # 使用的sql类型：mysql
        self.password = sql_dir.get("password")        # 密码：668899
        self.user = sql_dir.get("user")                # 访问sql用户：root
        self.docker_port = sql_dir.get("docker_port")  # sql的内部端口：33.6
        self.image = sql_dir.get("image")              # 镜像名：mariadb:latest

    def write_docker_compose_str(self):
        t = "    "
        s = ""
        s += f'{t}{self.docker_name}:\n{t*2}image: {self.image}\n'
        s += f'{t*2}container_name: {self.docker_name}\n{t*2}environment:\n'
        s += f'{t*3}MYSQL_ROOT_PASSWORD: {self.password}\n'
        s += f'{t*3}MYSQL_USER: {self.user}\n'
        s += f'{t*2}ports:\n{t*3}- {self.local_port}:{self.docker_port}\n'
        # s += f'{t*2}volumns:\n{t*3}- {}\n'
        return s

