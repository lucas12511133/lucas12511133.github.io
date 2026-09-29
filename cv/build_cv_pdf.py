from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "lu-sheng-cv-meal-optimization.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

PAGE_W, PAGE_H = A4
INK = colors.HexColor("#15191C")
COBALT = colors.HexColor("#2349D8")
MUTED = colors.HexColor("#5F6366")
FONT_DIR = Path(r"C:\Windows\Fonts")
for name, filename in {
    "Georgia": "georgia.ttf",
    "Georgia-Bold": "georgiab.ttf",
    "Georgia-Italic": "georgiai.ttf",
    "Georgia-BoldItalic": "georgiaz.ttf",
}.items():
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / filename)))
pdfmetrics.registerFontFamily(
    "Georgia", normal="Georgia", bold="Georgia-Bold",
    italic="Georgia-Italic", boldItalic="Georgia-BoldItalic",
)

styles = getSampleStyleSheet()
body = ParagraphStyle(
    "Body", parent=styles["Normal"], fontName="Georgia", fontSize=8.55,
    leading=10.55, textColor=INK, spaceAfter=0,
)
body_muted = ParagraphStyle(
    "BodyMuted", parent=body, textColor=MUTED,
)
header_contact = ParagraphStyle(
    "HeaderContact", parent=body, alignment=1,
)
small = ParagraphStyle(
    "Small", parent=body, fontSize=7.8, leading=9.5, textColor=MUTED,
)
header_name = ParagraphStyle(
    "HeaderName", parent=body, fontName="Georgia-Bold", fontSize=22,
    leading=25, alignment=1, textColor=INK, spaceAfter=2,
)
header_meta = ParagraphStyle(
    "HeaderMeta", parent=body, fontName="Georgia", fontSize=9,
    leading=11, alignment=1, textColor=INK, spaceAfter=1,
)
section_style = ParagraphStyle(
    "Section", parent=body, fontName="Georgia-Bold", fontSize=10.2,
    leading=12, textColor=INK, spaceBefore=0, spaceAfter=0,
)
entry_title = ParagraphStyle(
    "EntryTitle", parent=body, fontName="Georgia-Bold", fontSize=9.1,
    leading=11, textColor=INK,
)
entry_italic = ParagraphStyle(
    "EntryItalic", parent=body, fontName="Georgia-Italic", fontSize=8.5,
    leading=10.3, textColor=INK,
)
date_style = ParagraphStyle(
    "Date", parent=body, alignment=TA_RIGHT, fontName="Georgia", fontSize=8.5,
    leading=10.3, textColor=INK,
)
location_style = ParagraphStyle(
    "Location", parent=entry_italic, alignment=TA_RIGHT, fontSize=8.3,
    leading=10.1,
)
project_body = ParagraphStyle(
    "ProjectPoint", parent=body, fontSize=8.4, leading=10.2,
)
bullet_style = ParagraphStyle(
    "Bullet", parent=body, fontName="Georgia", fontSize=9, leading=10.5,
)


def section(title):
    table = Table([[Paragraph(title.upper(), section_style)]], colWidths=[PAGE_W - 0.96 * inch])
    table.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.45, INK),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def bullets(items, bullet_color=INK):
    return bullet_table(items, body)


def project_points(items):
    return bullet_table(items, project_body)


def bullet_table(items, paragraph_style):
    rows = [[Paragraph("•", bullet_style), Paragraph(item, paragraph_style)] for item in items]
    table = Table(rows, colWidths=[0.18 * inch, PAGE_W - 0.96 * inch - 0.18 * inch])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.7),
    ]))
    return table


def entry(title, subtitle, date, details=None, project=False, location=None):
    rows = [[Paragraph(title, entry_title), Paragraph(date, date_style)],
            [Paragraph(subtitle, entry_italic), Paragraph(location, location_style) if location else ""]]
    if details:
        rows.append([project_points(details) if project else bullets(details), ""])
    table = Table(rows, colWidths=[PAGE_W - 2.18 * inch, 1.22 * inch], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("SPAN", (0, 1), (1, 1)) if not location else ("RIGHTPADDING", (0, 1), (1, 1), 0),
        ("SPAN", (0, 2), (1, 2)) if details else ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
    ]))
    return table


story = []

header_text = [
    Paragraph("Lucas Lu", header_name),
    Paragraph("B.Eng. Candidate in Industrial Engineering | Class of 2029", header_meta),
    Paragraph("<link href='mailto:12511133@mail.sustech.edu.cn' color='#2349D8'>12511133@mail.sustech.edu.cn</link> | (+86) 157-2864-3180", header_contact),
    Paragraph("<link href='https://lucas12511133.github.io' color='#2349D8'>lucas12511133.github.io</link> | Shenzhen, China", header_contact),
]
for paragraph in header_text:
    story.append(paragraph)
story.append(Spacer(1, 5))

story.append(section("Education"))
story.append(entry(
    "Southern University of Science and Technology (SUSTech)",
    "B.Eng. in Industrial Engineering, Zhicheng College",
    "Aug. 2025 - Present",
    [
        "<b>GPA: 3.91 / 4.0</b> | <b>Major Ranking: 1 / 11</b> | <b>Comprehensive Assessment Ranking: 3 / 244</b>.",
        "<b>Selected Coursework:</b> Mathematical Analysis I-II (93, 96), Ordinary Differential Equations B (98), Foundation of Probability Theory (94), Linear Algebra (89), Introduction to C Programming (96), College Physics II (90).",
    ], location="Shenzhen, China",
))
story.append(section("Research Interests"))
story.append(Paragraph("Operations Research & Optimization; Emergency Response & Logistics; Machine Learning & Data Science; Mathematical Modeling.", body))
story.append(section("Research Experience"))
story.append(entry(
    "EMS Station Location Optimization",
    "Project Lead | 120 EMS Station Location Optimization",
    "2026 - Present",
    [
        "Led a 6-member team in optimizing EMS station locations across Shenzhen; partitioned the city into 5,279 500m x 500m grids.",
        "Built an XGBoost ETA model from 620K+ dispatch records and 360K Tencent Maps samples (MAE = 1.64 min, R2 = 0.863), achieving 90% coverage within 10 minutes.",
        "Finalist, 8th China University Mechanical Engineering Innovation & Creativity Competition (2026). Tools: Python, OSMnx, XGBoost.",
    ], project=True,
))
story.append(entry(
    "AED Deployment at Gulongzhong",
    "Project Participant | AED Deployment at Gulongzhong",
    "2026 - Present",
    [
        "Compared fixed AED placement with a dynamic human-vehicle-drone response scheme using road-network analysis.",
        "Explored sustainable operating models, including potential insurance partnerships.",
    ], project=True,
))
story.append(entry(
    "Meal Optimization WeChat Mini Program",
    "Project Developer | Personalized Meal Recommendation",
    "2026",
    [
        "Built a personalized meal recommendation mini program with Taro + React + TypeScript, Tencent Cloud Functions, and an optimization solver; supports meal composition, taste matching, nutrition constraints, and set-meal recommendations.",
        "Implemented upper/lower bounds for calories, protein, carbohydrates, and fats, plus hard exclusion of disliked ingredients, dish-level replacement, and alternatives for infeasible plans.",
        "Added carbohydrate-overage alerts and diet suggestions; improved reliability with legacy solver compatibility, exception fallbacks, and clearer frontend feedback.",
    ], project=True,
))

story.append(section("Leadership & Volunteer Experience"))
story.append(entry(
    "Core Student Leader",
    "SUSTech IE Hunt | Optimization challenge planning and team coordination",
    "Oct. 2025 - Present",
    ["Co-led Seasons 1-2 of a campus-wide optimization challenge, integrating the Traveling Salesman Problem and Linear Programming into game mechanics; coordinated a 5-member team across logistics, feasibility analysis, and promotion."],
))
story.append(entry(
    "Student Representative",
    "Zhicheng College 10th Anniversary Ceremony | Sole freshman keynote speaker",
    "Oct. 2025",
))
story.append(entry(
    "Volunteer",
    "APEC Shenzhen 2026",
    "2026",
))
story.append(entry(
    "Group Leader",
    "Orange Light Volunteer Service Team | Community research and accessibility advocacy",
    "2025 - Present",
    ["Completed 160+ hours of volunteer service. Led community research across Shenzhen, Foshan, and Guangzhou; partnered with the Shenzhen Association for the Blind on accessibility supervision and hosted Oxford University delegations at SUSTech."],
))

story.append(section("Selected Honors & Awards"))
story.append(bullets([
    "<b>Scholarships:</b> First-Class Outstanding Student Scholarship, SUSTech (top 5% university-wide, 2026).",
    "<b>Competitions:</b> First Prize, Greater Bay Area Industrial Engineering Innovation Competition (ranked 2nd of 54, 2026); Second Prize, National College Student Mathematics Competition (Non-Math A, top 15% nationally, 2025).",
    "<b>Honors:</b> APRU ULP Outstanding Student Ambassador (one of ten university-wide, 2026); Outstanding Individual, SUSTech Winter Social Practice and Winter Visit to Alma Mater (one of 50 selected university-wide, 2026); Outstanding Camper, 4th Xiancheng Program (2025); Social Impact Award and Outstanding Volunteer Service Organization, Chengguang Volunteer Team (2025).",
]))

story.append(section("Skills & Interests"))
story.append(bullets([
    "<b>Programming Skills:</b> Python, MATLAB, R, C, LaTeX, AnyLogic, XGBoost, scikit-learn, NumPy, Pandas, Matplotlib, OSMnx.",
    "<b>Languages:</b> Mandarin (Native), English (Proficient), Korean (Daily basics).",
]))

doc = SimpleDocTemplate(
    str(OUT), pagesize=A4, rightMargin=0.43 * inch, leftMargin=0.43 * inch,
    topMargin=0.46 * inch, bottomMargin=0.46 * inch,
    title="Lucas Lu - Curriculum Vitae",
    author="Sheng Lu",
)
doc.build(story)
print(OUT)
