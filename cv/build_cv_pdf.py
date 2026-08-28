from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
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
HAIRLINE = colors.HexColor("#B9BDC2")

styles = getSampleStyleSheet()
body = ParagraphStyle(
    "Body", parent=styles["Normal"], fontName="Helvetica", fontSize=7.45,
    leading=9.15, textColor=INK, spaceAfter=0,
)
body_muted = ParagraphStyle(
    "BodyMuted", parent=body, textColor=MUTED,
)
small = ParagraphStyle(
    "Small", parent=body, fontSize=6.7, leading=8.1, textColor=MUTED,
)
header_name = ParagraphStyle(
    "HeaderName", parent=body, fontName="Helvetica-Bold", fontSize=19,
    leading=21, textColor=INK, spaceAfter=3,
)
header_meta = ParagraphStyle(
    "HeaderMeta", parent=body, fontName="Helvetica-Bold", fontSize=8.2,
    leading=10, textColor=INK, spaceAfter=3,
)
section_style = ParagraphStyle(
    "Section", parent=body, fontName="Helvetica-Bold", fontSize=9.3,
    leading=11, textColor=INK, spaceBefore=0, spaceAfter=0,
)
entry_title = ParagraphStyle(
    "EntryTitle", parent=body, fontName="Helvetica-Bold", fontSize=8.05,
    leading=9.6, textColor=INK,
)
entry_italic = ParagraphStyle(
    "EntryItalic", parent=body, fontName="Helvetica-Oblique", fontSize=7.45,
    leading=9.0, textColor=INK,
)
date_style = ParagraphStyle(
    "Date", parent=body, alignment=TA_RIGHT, fontSize=7.2,
    leading=8.8, textColor=MUTED,
)


def section(title):
    table = Table([[Paragraph(title.upper(), section_style)]], colWidths=[PAGE_W - 0.86 * inch])
    table.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.55, INK),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
    ]))
    return table


def bullets(items, bullet_color=COBALT):
    return ListFlowable(
        [ListItem(Paragraph(item, body), leftIndent=0) for item in items],
        bulletType="bullet", start="circle", bulletFontName="Helvetica",
        bulletFontSize=5.4, bulletColor=bullet_color, leftIndent=11,
        bulletOffsetY=1.2, spaceBefore=1, spaceAfter=1,
    )


def entry(title, subtitle, date, details=None):
    rows = [[Paragraph(title, entry_title), Paragraph(date, date_style)],
            [Paragraph(subtitle, entry_italic), ""]]
    if details:
        rows.append([bullets(details), ""])
    table = Table(rows, colWidths=[PAGE_W - 2.08 * inch, 1.22 * inch], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("SPAN", (0, 1), (1, 1)),
        ("SPAN", (0, 2), (1, 2)) if details else ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.0),
    ]))
    return table


story = []

header_text = [
    Paragraph("Sheng Lu (Lucas Lu)", header_name),
    Paragraph("B.Eng. Candidate in Industrial Engineering | Class of 2029", header_meta),
    Paragraph("Email: <link href='mailto:12511133@mail.sustech.edu.cn' color='#2349D8'>12511133@mail.sustech.edu.cn</link> | Phone: (+86) 157-2864-3180", body),
    Paragraph("Website: <link href='https://lucas12511133.github.io' color='#2349D8'>lucas12511133.github.io</link> | Location: Zhicheng College, SUSTech, Shenzhen, China", body),
]
photo = Image(str(ROOT / "cv" / "photo.png"), width=0.82 * inch, height=1.09 * inch)
header = Table([[header_text, photo]], colWidths=[5.85 * inch, 0.9 * inch])
header.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("ALIGN", (1, 0), (1, 0), "RIGHT"),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
]))
story.extend([header, Spacer(1, 2)])

story.append(section("Research Interests & Mentorship"))
story.append(bullets([
    "<b>Interests:</b> Operations Research & Optimization; Emergency Response & Logistics; Machine Learning & Data Science; Mathematical Modeling.",
    "<b>Academic Mentor:</b> <b>Professor Yu Wang</b>, Department of Industrial Engineering, SUSTech.",
]))

story.append(section("Education"))
story.append(entry(
    "Southern University of Science and Technology (SUSTech)",
    "B.Eng. in Industrial Engineering, Zhicheng College | Shenzhen, China",
    "Aug. 2025 - Present",
    [
        "<b>GPA: 3.91 / 4.0</b> | <b>Ranking: 1 / 11</b>.",
        "<b>Selected Coursework:</b> Mathematical Analysis I-II (93, 96), Ordinary Differential Equations B (98), Foundation of Probability Theory (94), Linear Algebra (89), Introduction to C Programming (96), College Physics II (90).",
    ],
))
story.append(section("Selected Research & Projects"))
story.append(entry(
    "EMS Station Location Optimization",
    "Project Lead | 120 EMS Station Location Optimization",
    "2026 - Present",
    [
        "Leading a 6-member team to optimize emergency medical service station placement across Shenzhen. Partitioned the city into 5,279 500m x 500m grids and developed an XGBoost ETA model using 620K+ dispatch records and 360K Tencent Maps samples (MAE = 1.64 min, R2 = 0.863); achieved 90% coverage within 10 minutes.",
        "Finalist, 8th China University Mechanical Engineering Innovation & Creativity Competition (2026). Tools: Python, OSMnx, XGBoost.",
    ],
))
story.append(entry(
    "AED Deployment at Gulongzhong",
    "Project Participant | AED Deployment at Gulongzhong",
    "2026 - Present",
    ["Comparing static AED placement with a dynamic human-vehicle-drone coordinated scheme using road-network analysis; exploring sustainable operation through insurance partnership models."],
))
story.append(entry(
    "Meal Optimization WeChat Mini Program",
    "Project Developer | Personalized Meal Recommendation",
    "2026",
    [
        "Developed a WeChat mini program for personalized meal recommendations from user profiles and dietary preferences, using Taro + React + TypeScript with Tencent Cloud Functions and an optimization solver. Supported meat/vegetable/staple structure configuration, taste matching, nutrition constraints, and set-meal recommendations.",
        "Implemented upper/lower bounds for calories, protein, carbohydrates, and fats; hard-excluded disliked ingredients, dish-level replacement, infeasibility fallbacks, and carbohydrate-overage alerts with adjustment suggestions. Improved stability and UX through legacy solver compatibility, exception fallback, and frontend feedback.",
    ],
))

story.append(section("Selected Honors & Awards"))
story.append(bullets([
    "<b>APRU ULP Outstanding Student Ambassador</b> (one of ten university-wide), APRU / SUSTech - 2026",
    "<b>Second Prize</b>, 17th National College Student Mathematics Competition (Non-Math A) - 2025",
    "<b>Outstanding Individual</b>, SUSTech Winter Social Practice - 2026",
    "<b>Outstanding Camper</b>, 4th Xiancheng Program, Zhicheng College - 2025",
    "<b>Social Impact Award</b>, Hundreds, Thousands, Myriads Project, Chengguang Volunteer Team - 2025",
    "<b>Outstanding Volunteer Service Organization of 2025</b>, Chengguang Volunteer Team - 2025",
]))

story.append(section("Leadership & Service"))
story.append(entry(
    "Core Student Leader | SUSTech IE Hunt",
    "Optimization challenge planning and student team coordination",
    "Oct. 2025 - Present",
    ["Co-led Seasons 1-2 of a campus-wide optimization challenge, integrating the Traveling Salesman Problem and Linear Programming into game mechanics; coordinated a 5-member team across logistics, feasibility analysis, and promotion."],
))
story.append(entry(
    "Student Representative | Zhicheng College 10th Anniversary Ceremony",
    "Selected as the sole freshman representative to deliver a formal keynote speech",
    "Oct. 2025",
))
story.append(entry(
    "Group Leader | Orange Light Volunteer Service Team",
    "Community research and accessibility advocacy",
    "2025 - Present",
    ["Led community research across Shenzhen, Foshan, and Guangzhou; partnered with the Shenzhen Association for the Blind on accessibility supervision and hosted Oxford University delegations at SUSTech."],
))

story.append(section("Skills"))
story.append(bullets([
    "<b>Programming & Technical:</b> Python, MATLAB, R, C, LaTeX, AnyLogic, XGBoost, scikit-learn, NumPy, Pandas, Matplotlib, OSMnx.",
    "<b>Languages:</b> Mandarin (Native), English (Proficient), Korean (Daily basics).",
]))

doc = SimpleDocTemplate(
    str(OUT), pagesize=A4, rightMargin=0.43 * inch, leftMargin=0.43 * inch,
    topMargin=0.34 * inch, bottomMargin=0.32 * inch,
    title="Sheng Lu (Lucas Lu) - Curriculum Vitae",
    author="Sheng Lu",
)
doc.build(story)
print(OUT)
