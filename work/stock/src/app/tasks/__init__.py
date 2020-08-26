import time
from datetime import datetime

"""
year (int|str) – 年，4位数字 
month (int|str) – 月 (范围1-12) 
day (int|str) – 日 (范围1-31)  "9-22"
week (int|str) – 周 (范围1-53) 
day_of_week (int|str) – 周内第几天或者星期几 (范围0-6 或者 mon,tue,wed,thu,fri,sat,sun) 
hour (int|str) – 时 (范围0-23) 
minute (int|str) – 分 (范围0-59) 
second (int|str) – 秒 (范围0-59) 
start_date (datetime|str) – 最早开始日期(包含) 
end_date (datetime|str) – 最晚结束时间(包含) 
timezone (datetime.tzinfo|str) – 指定时区
"""
JOBS = [
    {
        'id': 'job1',
        'func': 'app.tasks:work_time',
        'args': None,
        'trigger': {
            'type': 'cron',  # 类型
            'minute': '*/2',   #每两分钟执行一次
        },
    },
    {
        'id': 'job9',
        'func': 'app.data.tusharedata:update_last_daily_basic',
        'args': None,
        'trigger': {
            'type': 'cron',  # 类型
            'day': '*/1',  #
        },
    },
]


def work_time():
    print(datetime.now())

