from datetime import datetime, timedelta
import os
# from PIL import Image
from report.shields_pressure_save import Pressure_save
from report.shearer_info_save import Shearer_csv
from report.pressure_heatmap import func_heat
from report.shearer_curve import func_pos, func_auto, func_speed
from report.pressure_3D import pressure_3D
from report.auto_statistics import Statistic
from report.auto_pdf import auto_pdf, doc_json_format, tag2catalog, AutoPDF
from report.analysis_data import harvest_advance
import time

HOST = '192.168.3.100'
USER = 'root'
PWD = '123456'
DATABASE = 'marcosys1'
PORT = 3306


def summary_pdf(num, sensor_id, time_begin, time_end, pro, target_dir, tags=None, date=time.strftime('%Y-%m-%d')):
    """
    保存图片至目标文件夹，汇总图片成pdf
    target_dir 目标文件夹位置
    num  支架数量
    date 生成的日期时间，格式 2020-07-23
    pro 项目号
    sensor_id 传感器类型
    date 报告所在文件夹名
    time_begin  起始时间
    time_end    终止时间
    tags: 排除
    :return:
-   tpdf： 目标文件相对位-置
    """
    # path = os.path.join(target_dir, "charts", date)
    img_addr = os.path.join(target_dir, "static", "logo")
    path = os.path.join(target_dir, "static", "reports", date)
    os.makedirs(path, exist_ok=True)

    # try:
    #
    shearer_csv = Shearer_csv(HOST, USER, PWD, DATABASE, PORT)
    shearer_csv.func_shearer_save(time_begin, time_end, path, pro)        # 生成采煤机数据csv文件
    # pressure_save = Pressure_save(HOST, USER, PWD, DATABASE, PORT)
    # pressure_save.func_psave(num, sensor_id, time_begin, time_end, path, pro)   # 生成支架压力csv文件
    # 存储图片
    # p3D = pressure_3D()
    # p3D.func_3D(num, time_begin, path, pro, sensor_id)   # 工作面压力3D显示
    # func_heat(num, time_begin, path, pro, sensor_id)     # 工作面压力热力图
    func_pos(path, pro, time_begin)                      # 采煤机位置曲线
    func_speed(path, pro, time_begin)                    # 采煤机速度曲线
    func_auto(path, pro, time_begin)                     # 采煤机自动化轨迹
    statistic = Statistic()
    s_table = statistic.func(path, pro, time_begin)  # 采煤机自动化统计
    harvest_advance(path, pro, time_begin)  # 产量统计
    #
    doc_json = tag2catalog(tags, date, s_table)
    auto_pdf = AutoPDF(img_addr, path, doc_json)
    auto_pdf.start()
    # auto_pdf(img_addr, path, doc_json)                   # 自动生成pdf
    # except Exception as e:
    #     return (False, None)
    # result = os.path.join(path, "统计分析报告.pdf")
    # return (True, result)


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
summary_pdf(num=173, sensor_id=304, time_begin='2020-08-26 00:00:00', time_end='2020-08-26 23:59:59', pro='shm8',
            target_dir=basedir, date='2020-08-26')
