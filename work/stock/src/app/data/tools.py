import requests
import re


def get_pai_ming(code):
    url = f"""http://guba.eastmoney.com/list,{code}.html"""
    r = requests.get(url)
    t = r.text
    e = re.search(' 当前浏览排行第 .*>(\d+)</em>',t)
    print(e.group())
    print(e.group(1))
    pm = int(e.group(1))
    print(type(pm))
    return pm

get_pai_ming('000651')