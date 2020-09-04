# -*- coding: UTF-8 -*-
import copy
import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.lib.units import cm
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table
from reportlab.platypus import Spacer, PageBreak
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.frames import Frame
from reportlab.platypus.tableofcontents import TableOfContents

pdfmetrics.registerFont(TTFont('SimHei', 'SimHei.ttf'))  # 注册字体
# styles = getSampleStyleSheet()
# styles.add(ParagraphStyle(fontName='SimHei', name='Song', leading=20, fontSize=12))  #自己增加新注册的字体


centered = PS(name='center',
              fontSize=18,
              leading=16,
              alignment=1,
              spaceAfter=20,
              fontName='SimHei',
              )

h1 = PS(
    fontName='SimHei',
    name='Heading1',
    fontSize=16,
    leading=30,
)

h2 = PS(name='Heading2',
        fontName='SimHei',
        fontSize=12,
        leading=30)

right = PS(name='right',
           fontName='SimHei',
           fontSize=12,
           leading=14)

body = PS(name='body',
          fontName='SimHei',
          leading=30,
          )

title = PS(name='normal',
           fontName='SimHei',
           leading=30,
           )


class MyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)

    def afterFlowable(self, flowable):
        "Registers TOC entries."
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'Heading1':
                level = 0
            elif style == 'Heading2':
                level = 1
            else:
                return
            E = [level, text, self.page - 1]
            # if we have a bookmark name append that to our notify data
            bn = getattr(flowable, '_bookmarkName', None)
            if bn is not None: E.append(bn)
            self.notify('TOCEntry', tuple(E))


def table_model(data):
    width = 6  # 总宽度
    colWidths = (width / len(data[0])) * inch  # 每列的宽度

    dis_list = []
    for x in data:
        # dis_list.append(map(lambda i: Paragraph('%s' % i, cn), x))
        dis_list.append(x)

    style = [
        ('FONTNAME', (0, 0), (-1, -1), "SimHei"),  # 字体
        ('FONTSIZE', (0, 0), (-1, 0), 13),  # 字体大小
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 对齐
        ('VALIGN', (-1, 0), (-2, 0), 'MIDDLE'),  # 对齐
        ('LINEBEFORE', (0, 0), (0, -1), 0.2, colors.grey),  # 设置表格左边线颜色为灰色，线宽为0.2
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.royalblue),  # 设置表格内文字颜色
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # 设置表格框线为grey色，线宽为0.5
    ]

    component_table = Table(dis_list, colWidths=colWidths, style=style)

    return component_table

class AutoPDF:

    def __init__(self, img_addr, path, doc_json):
        """
        :param img_addr: 图片存放地址
        :param pdf: pdf目标文件输出地址
        :return:
        """
        self.img_addr = img_addr
        self.path = path
        self.doc_json = doc_json

        self.icon = os.path.join(img_addr, "logo.png")
        self.day = doc_json.get("day")
        self.pdf_file = os.path.join(path, '统计分析报告.pdf')
        self.story = []


    def footer(self, canvas, doc):
        canvas.saveState()  # 先保存当前的画布状态
        page = canvas.getPageNumber()
        if page > 2:
            page = page - 2
            pageNumber = ("%s页" % page)  # 获取当前的页码
            p = Paragraph(pageNumber, right)
            w, h = p.wrap(1 * cm, 1 * cm)  # 申请一块1cm大小的空间，返回值是实际使用的空间
            p.drawOn(canvas, doc.leftMargin + doc.width - 20, doc.topMargin - 13)  # 将页码放在指示坐标处
            # print(doc.leftMargin, doc.width, doc.topMargin)  # 将页码放在指示坐标处
            p = Paragraph(self.day, right)
            w, h = p.wrap(4 * cm, 4 * cm)
            p.drawOn(canvas, doc.leftMargin, doc.topMargin - 13)  # 将页码放在指示坐标处
        canvas.restoreState()

    def header(self, canvas, doc):
        canvas.saveState()
        p = Paragraph("<img src='%s' width='%d' height='%d'/>" % (self.icon, 50, 50),
                      h2)  # 使用一个Paragraph Flowable存放图片
        w, h = p.wrap(doc.width, doc.bottomMargin)
        canvas.line(doc.leftMargin, doc.bottomMargin, doc.leftMargin + doc.width,
                    doc.bottomMargin)  # 画一条横线
        p.drawOn(canvas, doc.width + 20, doc.topMargin + doc.height - 10)  # 放置图片
        p = Paragraph(f"<font size=10 >{self.doc_json.get('header_name')}</font>", h1)
        w, h = p.wrap(doc.width, doc.bottomMargin)
        p.drawOn(canvas, doc.leftMargin, doc.topMargin + doc.height - 15)  # 放置报告这句话
        canvas.line(doc.leftMargin, doc.bottomMargin + doc.height, doc.leftMargin + doc.width,
                    doc.bottomMargin + doc.height)  # 画一条横线
        canvas.restoreState()

    def doHeading(self, text, sty):
        from hashlib import sha1
        bn = sha1((text + sty.name).encode("utf-8")).hexdigest()
        h = Paragraph(text + '<a name="%s"/>' % bn, sty)
        h._bookmarkName = bn
        self.story.append(h)


    def start(self):
        self.story.append(PageBreak())
        doc = MyDocTemplate(self.pdf_file, pageSize=letter)
        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
        template = PageTemplate(id='test', frames=frame, onPage=self.header, onPageEnd=self.footer)
        doc.addPageTemplates([template])

        catalog = self.doc_json.get("catalog")

        if catalog is not None:
            self.story.append(Paragraph('<b>目录</b>', centered))
            toc = TableOfContents()
            toc.levelStyles = [
                PS(fontName='SimHei', fontSize=16, name='TOCHeading1', leftIndent=20, firstLineIndent=-20,
                   spaceBefore=10,
                   leading=16),
                PS(fontName='SimHei', fontSize=12, name='TOCHeading2', leftIndent=40, firstLineIndent=-20,
                   spaceBefore=5,
                   leading=12),
            ]
            self.story.append(toc)
            self.story.append(PageBreak())

            for i, ts in enumerate(catalog):
                self.doHeading(f"{i + 1} {ts.get('title')}", h1)
                for j, cata in enumerate(ts.get("content")):
                    self.doHeading(f"{i + 1}.{j + 1} {cata.get('index')}", h2)
                    text = cata.get("text") or ""
                    text = text.replace('\n', "<br/>")
                    self.story.append(Paragraph(text, body))
                    img = cata.get("img")
                    imgs = cata.get("imgs")
                    if img is not None and img != "":
                        img = os.path.join(self.path, img)
                        p = Paragraph("<br/><img src='%s' width='%d' height='%d'/>" % (img, 560, 315),
                                      centered)  # 使用一个Paragraph Flowable存放图片
                        # p.drawOn(doc., doc.leftMargin, doc.topMargin + doc.height+10000)
                        self.story.append(Spacer(1, 280))
                        self.story.append(p)  # 放置图片
                    if imgs is not None and img != []:
                        for img in imgs:
                            img = os.path.join(self.path, img)
                            p = Paragraph("<br/><img src='%s' width='%d' height='%d'/>" % (img, 560, 315),
                                          centered)  # 使用一个Paragraph Flowable存放图片
                            # p.drawOn(doc., doc.leftMargin, doc.topMargin + doc.height+10000)
                            self.story.append(Spacer(1, 260))
                            self.story.append(p)  # 放置图片

                    table = cata.get("table")
                    if table is not None:
                        z = table_model(table)
                        self.story.append(z)
                        self.story.append(Spacer(1, 50))
        doc.multiBuild(self.story)









def auto_pdf(img_addr, path, doc_json):
    """
    :param img_addr: 图片存放地址
    :param pdf: pdf目标文件输出地址
    :return:
    """
    icon = os.path.join(img_addr, "logo.png")

    day = doc_json.get("day")
    pdf_file = os.path.join(path, '统计分析报告.pdf')

    def footer(canvas, doc):
        canvas.saveState()  # 先保存当前的画布状态
        page = canvas.getPageNumber()
        if page > 2:
            page = page - 2
            pageNumber = ("%s页" % page)  # 获取当前的页码
            p = Paragraph(pageNumber, right)
            w, h = p.wrap(1 * cm, 1 * cm)  # 申请一块1cm大小的空间，返回值是实际使用的空间
            p.drawOn(canvas, doc.leftMargin + doc.width - 20, doc.topMargin - 13)  # 将页码放在指示坐标处
            # print(doc.leftMargin, doc.width, doc.topMargin)  # 将页码放在指示坐标处
            p = Paragraph(day, right)
            w, h = p.wrap(4 * cm, 4 * cm)
            p.drawOn(canvas, doc.leftMargin, doc.topMargin - 13)  # 将页码放在指示坐标处
        canvas.restoreState()

    def header(canvas, doc):
        canvas.saveState()
        p = Paragraph("<img src='%s' width='%d' height='%d'/>" % (icon, 50, 50),
                      h2)  # 使用一个Paragraph Flowable存放图片
        w, h = p.wrap(doc.width, doc.bottomMargin)
        canvas.line(doc.leftMargin, doc.bottomMargin, doc.leftMargin + doc.width,
                    doc.bottomMargin)  # 画一条横线
        p.drawOn(canvas, doc.width + 20, doc.topMargin + doc.height - 10)  # 放置图片
        p = Paragraph(f"<font size=10 >{doc_json.get('header_name')}</font>", h1)
        w, h = p.wrap(doc.width, doc.bottomMargin)
        p.drawOn(canvas, doc.leftMargin, doc.topMargin + doc.height - 15)  # 放置报告这句话
        canvas.line(doc.leftMargin, doc.bottomMargin + doc.height, doc.leftMargin + doc.width,
                    doc.bottomMargin + doc.height)  # 画一条横线
        canvas.restoreState()

    def doHeading(text, sty):
        from hashlib import sha1
        bn = sha1((text + sty.name).encode("utf-8")).hexdigest()
        h = Paragraph(text + '<a name="%s"/>' % bn, sty)
        h._bookmarkName = bn
        story.append(h)

    story = []
    story.append(PageBreak())
    doc = MyDocTemplate(pdf_file, pageSize=letter)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    template = PageTemplate(id='test', frames=frame, onPage=header, onPageEnd=footer)
    doc.addPageTemplates([template])

    catalog = doc_json.get("catalog")

    if catalog is not None:
        story.append(Paragraph('<b>目录</b>', centered))
        toc = TableOfContents()
        toc.levelStyles = [
            PS(fontName='SimHei', fontSize=16, name='TOCHeading1', leftIndent=20, firstLineIndent=-20, spaceBefore=10,
               leading=16),
            PS(fontName='SimHei', fontSize=12, name='TOCHeading2', leftIndent=40, firstLineIndent=-20, spaceBefore=5,
               leading=12),
        ]
        story.append(toc)
        story.append(PageBreak())

        for i, ts in enumerate(catalog):
            doHeading(f"{i + 1} {ts.get('title')}", h1)
            for j, cata in enumerate(ts.get("content")):
                doHeading(f"{i + 1}.{j + 1} {cata.get('index')}", h2)
                text = cata.get("text") or ""
                text = text.replace('\n', "<br/>")
                story.append(Paragraph(text, body))
                img = cata.get("img")
                imgs = cata.get("imgs")
                if img is not None and img != "":
                    img = os.path.join(path, img)
                    p = Paragraph("<br/><img src='%s' width='%d' height='%d'/>" % (img, 560, 315),
                                  centered)  # 使用一个Paragraph Flowable存放图片
                    # p.drawOn(doc., doc.leftMargin, doc.topMargin + doc.height+10000)
                    story.append(Spacer(1, 280))
                    story.append(p)  # 放置图片
                if imgs is not None and img != []:
                    for img in imgs:
                        img = os.path.join(path, img)
                        p = Paragraph("<br/><img src='%s' width='%d' height='%d'/>" % (img, 560, 315),
                                      centered)  # 使用一个Paragraph Flowable存放图片
                        # p.drawOn(doc., doc.leftMargin, doc.topMargin + doc.height+10000)
                        story.append(Spacer(1, 260))
                        story.append(p)  # 放置图片

                table = cata.get("table")
                if table is not None:
                    z = table_model(table)
                    story.append(z)
                    story.append(Spacer(1, 50))
    doc.multiBuild(story)

def doc_json_format():

    doc_json = {
        "header_name": "python软件部分工作报告",
        "day": datetime.now().strftime("%Y%m%d") ,
        "catalog": [
            {
                "title": "近期工作",
                "content": [
                    {
                        "index": "之前",
                        "text": "协助西安做做煤炭的报表生成",
                    },

                    {
                        "index": "现在",
                        "text": "准备这里的前后台开发工作",
                    },
                    {
                        "index": "后期",
                        "text": "等待数据，等待需求",
                    },
                ]
            },
        ],
    }

    return doc_json

# basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# img_addr = os.path.join(basedir, 'static/logo')
# target_file = os.path.join(basedir, "static/reports/2020-08-13", 'mintoc.pdf')


titles = ["概述", "液压支架状态", "自动化"]


def tag2catalog(tags, date, s_table):
    """
    :param tags: 选择的需要生成的标签
    :param doc_json: 生成的json文件
    :return:
    """
    doc_json = doc_json_format(date, s_table)

    if tags is not None:
        for catalog in doc_json.get("catalog"):
            copy_cata = copy.copy(catalog)
            for cata in copy_cata:
                title = cata.get("index")
                if title not in tags:
                    catalog.remove(cata)
    return doc_json




auto_pdf(img_addr="../static/logo",path="../static/reports",doc_json=doc_json_format())