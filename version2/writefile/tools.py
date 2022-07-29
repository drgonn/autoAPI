import os

def write_map(addr_lines_map):
    """再次更改写入文件地址
    args:
        addr_lines_map:一个字典
            {w+文件绝对地址:[文件的字符串列表]}
    """
    for addr in addr_lines_map:
        dirname = os.path.dirname(addr)
        ex = os.path.exists(dirname)
        if not ex:
            os.makedirs(dirname)
        w = open(addr, "w")
        for line in addr_lines_map[addr]:
            w.write(line)
        w.close()