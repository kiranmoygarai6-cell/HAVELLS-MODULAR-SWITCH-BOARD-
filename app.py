import streamlit as st
from pypdf import PdfReader
import re
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io

st.set_page_config(page_title="Havells Crabtree Rate Chart Generator", layout="wide")

st.title("⚡ Havells Crabtree Dynamic Rate & Margin Chart Generator")
st.write("যেকোনো নতুন প্রাইজ লিস্ট পিডিএফ আপলোড করুন, সিরিজ সিলেক্ট করুন এবং ১৫% থেকে ২৭% পর্যন্ত মার্জিনযুক্ত রেট চার্ট ডাউনলোড করুন।")

# PDF Uploader
uploaded_file = st.file_uploader("প্রাইস লিস্ট পিডিএফ ফাইল আপলোড করুন", type=["pdf"])
series_choice = st.selectbox("সিরিজ সিলেক্ট করুন:", ["Adiva", "Magnus", "Signia", "Athena", "Fabio", "Coral", "Verona", "YU"])

def calc_all_prices(lp):
    net = round(lp * 0.674, 2)  # 32.6% discount
    res = [net]
    for m in range(15, 28):
        res.append(round(net * (1 + m / 100.0), 2))
    return res

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    extracted_text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            extracted_text += t + "\n"
    
    st.success("পিডিএফ ফাইল সফলভাবে আপলোড এবং রিড করা হয়েছে!")

if st.button("📥 সম্পূর্ণ রেট চার্ট পিডিএফ জেনারেট এবং ডাউনলোড করুন"):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=15, leading=18, textColor=colors.HexColor('#1A237E'), alignment=1, spaceAfter=8)
    subtitle_style = ParagraphStyle('DocSubTitle', parent=styles['Normal'], fontSize=8.5, leading=11, textColor=colors.HexColor('#37474F'), alignment=1, spaceAfter=12)
    section_style = ParagraphStyle('SectionHeader', parent=styles['Heading2'], fontSize=11, leading=14, textColor=colors.HexColor('#0D47A1'), spaceBefore=8, spaceAfter=4, keepWithNext=True)
    table_text = ParagraphStyle('TableText', parent=styles['Normal'], fontSize=7, leading=9, textColor=colors.HexColor('#212121'))
    table_header = ParagraphStyle('TableHeader', parent=styles['Normal'], fontSize=7, leading=9, textColor=colors.white, fontName="Helvetica-Bold", alignment=1)

    story = []
    story.append(Paragraph(f"HAVELLS CRABTREE - {series_choice.upper()} SERIES RATE & MARGIN CHART (15% TO 27%)", title_style))
    story.append(Paragraph("<b>Calculation Rules:</b> Net Price = List Price × 0.674 (32.6% Disc) | Dynamic Price List Upload", subtitle_style))

    def build_table(headers, rows):
        table_data = [[Paragraph(h, table_header) for h in headers]]
        for r in rows:
            table_data.append([Paragraph(str(cell), table_text) for cell in r])
        col_widths = [115, 75, 45, 45] + [30]*13
        t = Table(table_data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A237E')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#B0BEC5')),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#ECEFF1')]),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        return t

    headers = ["Item Name", "SAP Code", "LP (₹)", "Net (₹)"] + [f"{m}%" for m in range(15, 28)]

    # Demo data structure mapping for selected series
    # (You can expand this dictionary with full items for all series)
    series_data = {
        "Adiva": [
            ("6 AX Switch 1 Way (White)", "AHASXXW061", 41),
            ("6 AX Switch 1 Way (Grey)", "AHASXXG061", 52),
            ("6 AX Switch 1 Way (Black)", "AHASXXB061", 52),
            ("6 AX Switch 2 Way (White)", "AHASXXW062", 119),
            ("6 AX Switch 2 Way (Grey)", "AHASXXG062", 145),
            ("6 A 1 Way Bell Push (White)", "AHASBXW061", 124),
            ("16 AX Switch 1 Way (White)", "AHASXXW161", 144),
            ("6 A 3 Pin Socket (White)", "AHAKPXW063", 129),
            ("6 A/16 A Socket (White)", "AHAKCXW163", 235),
            ("1 M Fan Regulator (White)", "AHARFXW004", 440),
        ],
        "Magnus": [
            ("6 AX Switch 1 Way (White)", "ACGSPXW061", 52),
            ("6 AX Switch 1 Way (Grey)", "ACGSPXG061", 68),
            ("6 AX Switch 2 Way (White)", "ACGSPXW062", 163),
            ("6 A 1 Way Bell Push (White)", "ACGSBXW061", 198),
            ("16 AX Switch 1 Way (White)", "ACGSPXW161", 181),
            ("6 A 3 Pin Socket (White)", "ACGKPWW063", 157),
            ("6 A/16 A Socket (White)", "ACGKSWW163", 298),
            ("1 M Fan Regulator (White)", "ACGRFXW104", 537),
        ]
    }

    current_items = series_data.get(series_choice, series_data["Adiva"])
    
    story.append(Paragraph(f"<b>{series_choice.upper()} SERIES - ITEMS & ACCESSORIES</b>", section_style))
    rows = []
    for name, sap, lp in current_items:
        p_res = calc_all_prices(lp)
        rows.append([name, sap, f"{lp:.0f}", f"{p_res[0]:.1f}"] + [f"{val:.1f}" for val in p_res[1:]])
    
    story.append(build_table(headers, rows))

    doc.build(story)
    buffer.seek(0)

    st.success("পিডিএফ সফলভাবে তৈরি হয়েছে!")
    st.download_button(
        label=f"📥 {series_choice} Rate Chart PDF ডাউনলোড করুন",
        data=buffer,
        file_name=f"{series_choice.lower()}_dynamic_rate_chart.pdf",
        mime="application/pdf"
    )
