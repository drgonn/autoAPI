from _datetime import datetime,timedelta

# HOLIDAY 周一到周五放假的日期
HOLIDAY = ["2020-05-01", "2020-05-02", "2020-05-03", "2020-10-01", "2020-10-02", "2020-10-03",
           "2020-10-04",
           "2020-10-05", "2020-10-06", "2020-10-07" ]

# get_time 如果传入时间当前放假返回 None ,否则返回本身
def not_holiday(now=datetime.now()):
    # 日期是周一到周五 ，判断是否在 HOLIDAY，不在就返回now,否则返回None
    # weekday 0-4 周一到周五    5,6 周六周天
    weekday = now.weekday()
    if weekday <= 4:
        if now.strftime("%Y-%m-%d") in HOLIDAY:
            return None
        return now
    return None

def get_last_unholiday(now=datetime.now()):
    today = not_holiday(now)
    while today is None:
        now = now-timedelta(days=1)
    return today
