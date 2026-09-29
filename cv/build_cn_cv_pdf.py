from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "lu-sheng-cv-zh.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

FONT_DIR = Path(r"C:\Windows\Fonts")
pdfmetrics.registerFont(TTFont("MicrosoftYaHei", str(FONT_DIR / "msyh.ttc"), subfontIndex=0))
pdfmetrics.registerFont(TTFont("MicrosoftYaHei-Bold", str(FONT_DIR / "msyhbd.ttc"), subfontIndex=0))
pdfmetrics.registerFontFamily(
    "MicrosoftYaHei", normal="MicrosoftYaHei", bold="MicrosoftYaHei-Bold",
    italic="MicrosoftYaHei", boldItalic="MicrosoftYaHei-Bold",
)

PAGE_W, _ = A4
INK = colors.HexColor("#15191C")
COBALT = colors.HexColor("#2349D8")
MUTED = colors.HexColor("#5F6366")

styles = getSampleStyleSheet()
body = ParagraphStyle(
    "ChineseBody", parent=styles["Normal"], fontName="MicrosoftYaHei",
    fontSize=8.8, leading=11.1, textColor=INK, spaceAfter=0,
)
header_name = ParagraphStyle(
    "ChineseHeaderName", parent=body, fontName="MicrosoftYaHei-Bold",
    fontSize=22, leading=25, alignment=TA_CENTER, spaceAfter=2,
)
header_meta = ParagraphStyle(
    "ChineseHeaderMeta", parent=body, fontName="MicrosoftYaHei",
    fontSize=8.6, leading=10.5, alignment=TA_CENTER, spaceAfter=1,
)
section_style = ParagraphStyle(
    "ChineseSection", parent=body, fontName="MicrosoftYaHei-Bold",
    fontSize=9.8, leading=12, spaceBefore=0, spaceAfter=0,
)
entry_title = ParagraphStyle(
    "ChineseEntryTitle", parent=body, fontName="MicrosoftYaHei-Bold",
    fontSize=8.8, leading=10.8,
)
entry_meta = ParagraphStyle(
    "ChineseEntryMeta", parent=body, fontSize=8.2, leading=10,
)
date_style = ParagraphStyle(
    "ChineseDate", parent=body, alignment=TA_RIGHT, fontSize=8.1,
    leading=9.8, textColor=INK,
)
location_style = ParagraphStyle(
    "ChineseLocation", parent=entry_meta, alignment=TA_RIGHT, textColor=INK,
)
project_body = ParagraphStyle(
    "ChineseProjectPoint", parent=body, fontSize=8.7, leading=10.7,
)
bullet_style = ParagraphStyle(
    "ChineseBullet", parent=body, fontSize=9, leading=10.5,
)


def section(title):
    table = Table([[Paragraph(title.upper(), section_style)]], colWidths=[PAGE_W - 0.96 * inch])
    table.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.45, INK),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table


def paragraphs(items):
    return bullet_table(items, body)


def bullet_table(items, paragraph_style):
    rows = [[Paragraph("•", bullet_style), Paragraph(item, paragraph_style)] for item in items]
    table = Table(rows, colWidths=[0.18 * inch, PAGE_W - 0.96 * inch - 0.18 * inch])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.2),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return table


def project_points(items):
    return bullet_table(items, project_body)


def entry(title, role, date, details=None, project=False, location=None):
    rows = [
        [Paragraph(title, entry_title), Paragraph(date, date_style)],
        [Paragraph(role, entry_meta), Paragraph(location, location_style) if location else ""],
    ]
    if details:
        rows.append([project_points(details) if project else paragraphs(details), ""])
    table = Table(rows, colWidths=[PAGE_W - 2.18 * inch, 1.22 * inch], hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("SPAN", (0, 1), (1, 1)) if not location else ("RIGHTPADDING", (0, 1), (1, 1), 0),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
    ]
    if details:
        commands.append(("SPAN", (0, 2), (1, 2)))
    table.setStyle(TableStyle(commands))
    return table


story = []
header_text = [
    Paragraph("卢胜", header_name),
    Paragraph("南方科技大学 · 工业工程专业本科生 · 2029届", header_meta),
    Paragraph("<link href='mailto:12511133@mail.sustech.edu.cn' color='#2349D8'>12511133@mail.sustech.edu.cn</link>　|　(+86) 157-2864-3180", header_meta),
    Paragraph("<link href='https://lucas12511133.github.io' color='#2349D8'>lucas12511133.github.io</link>　|　深圳，中国", header_meta),
]
for paragraph in header_text:
    story.append(paragraph)
story.append(Spacer(1, 5))

story.append(section("教育经历"))
story.append(entry(
    "南方科技大学（SUSTech）",
    "工学学士在读 · 工业工程专业 · 致诚书院",
    "2025.08 - 至今",
    [
        "<b>GPA：3.91 / 4.0</b>　|　<b>排名：1 / 11</b>。",
        "<b>部分课程：</b>数学分析 I-II（93、96）、常微分方程 B（98）、概率论基础（94）、线性代数（89）、C语言程序设计（96）、大学物理 II（90）。",
    ], location="深圳，中国",
))
story.append(section("研究兴趣"))
story.append(Paragraph("运筹优化、应急响应与物流、机器学习与数据科学、数学建模。", body))

story.append(section("研究经历"))
story.append(entry(
    "深圳市急救站点选址优化",
    "项目负责人 · 120急救站点选址优化",
    "2026 - 至今",
    [
        "带领6人团队开展深圳市急救站点布局优化，将全市划分为5,279个500米×500米网格。",
        "基于62万余条急救调度记录和36万条腾讯地图样本构建XGBoost预计到达时间模型，MAE为1.64分钟、R²为0.863，实现10分钟覆盖率90%。",
        "入围第八届中国大学生机械工程创新创意大赛（2026）。工具：Python、OSMnx、XGBoost。",
    ], project=True,
))
story.append(entry(
    "古隆中景区 AED 布设优化",
    "项目参与者",
    "2026 - 至今",
    [
        "基于道路网络分析，比较固定式AED布设与人、车、无人机协同的动态响应方案。",
        "探索通过保险合作等方式构建可持续运营机制。",
    ], project=True,
))
story.append(entry(
    "餐食优化微信小程序",
    "项目开发者 · 智能膳食推荐",
    "2026",
    [
        "采用Taro + React + TypeScript构建前端，结合腾讯云云函数与优化求解器，根据用户画像和饮食偏好生成膳食套餐；支持荤素主食结构配置与口味匹配。",
        "设置热量、蛋白质、碳水和脂肪上下限；支持不喜欢食材硬排除、菜品逐道替换及无解场景备选方案。",
        "针对主食加入后碳水超标提供指标提示与饮食建议；兼容旧版求解器返回结果，并完善异常降级和交互反馈。",
    ], project=True,
))

story.append(section("领导力与志愿服务经历"))
story.append(entry(
    "核心学生负责人｜南科大 IE Hunt",
    "优化挑战策划与学生团队协作",
    "2025.10 - 至今",
    [
        "共同策划第1、2季校园优化挑战赛，将旅行商问题与线性规划融入游戏机制；协调5人团队负责物流、可行性分析与宣传。",
    ],
))
story.append(entry(
    "致诚书院十周年庆典学生代表",
    "作为唯一新生代表发表主题演讲",
    "2025.10",
))
story.append(entry(
    "志愿者｜APEC Shenzhen 2026",
    "APEC深圳2026志愿服务",
    "2026",
))
story.append(entry(
    "组长｜晨光志愿服务队",
    "社区调研与无障碍倡导 · 志愿服务累计160+小时",
    "2025 - 至今",
    [
        "在深圳、佛山、广州开展社区调研；与深圳市盲人协会合作开展无障碍监督，并在南科大接待牛津大学代表团。",
    ],
))

story.append(section("荣誉与获奖"))
story.append(paragraphs([
    "<b>奖学金：</b>南方科技大学优秀学生一等奖学金（全校前5%，2026）。",
    "<b>竞赛：</b>粤港澳大湾区工业工程创新大赛一等奖（54人中排名第2，2026）；第十七届全国大学生数学竞赛非数学A类二等奖（全国前15%，2025）。",
    "<b>荣誉：</b>APRU ULP优秀学生大使（全校十位之一，2026）；南科大寒假社会实践优秀实践个人、寒假母校行先进个人（全校评选50人，2026）；致诚书院第四届先诚团优秀营员（2025）；晨光志愿服务队“百千万工程”社会效益奖及年度优秀志愿服务组织（2025）。",
]))

story.append(section("技能与兴趣"))
story.append(paragraphs([
    "<b>编程与技术：</b>Python、MATLAB、R、C、LaTeX、AnyLogic、XGBoost、scikit-learn、NumPy、Pandas、Matplotlib、OSMnx",
    "<b>语言：</b>普通话（母语）、英语（熟练）、韩语（日常基础）。",
]))

doc = SimpleDocTemplate(
    str(OUT), pagesize=A4, rightMargin=0.43 * inch, leftMargin=0.43 * inch,
    topMargin=0.46 * inch, bottomMargin=0.46 * inch,
    title="卢胜 - 个人简历",
    author="卢胜",
)
doc.build(story)
print(OUT)
