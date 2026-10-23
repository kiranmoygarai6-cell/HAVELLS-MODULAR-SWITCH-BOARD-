import streamlit as st
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io

# Streamlit Page Config
st.set_page_config(page_title="Havells Crabtree Rate Chart Generator", layout="wide")

st.title("⚡ Havells Crabtree Rate & Margin Chart Generator")
st.write("পিডিএফ আপলোড করুন, সিরিজ সিলেক্ট করুন এবং ১৫% থেকে ২৭% পর্যন্ত মার্জিনযুক্ত রেট চার্ট ডাউনলোড করুন।")

# File Uploader
uploaded_file = st.file_uploader("প্রাইস লিস্ট পিডিএফ ফাইল আপলোড করুন", type=["pdf"])

# Series Selection
series_choice = st.selectbox("সিরিজ সিলেক্ট করুন:", ["Magnus", "Adiva"])

# Calculation function
def calc_all_prices(lp):
    net = round(lp * 0.674, 2)  # 32.6% discount
    res = [net]
    for m in range(15, 28):
        res.append(round(net * (1 + m / 100.0), 2))
    return res

# Data for Adiva
adiva_items = [
    ("6 AX Switch 1 Way", "AHASXXW061", 41, "AHASXXG061", 52, "AHASXXB061", 52),
    ("6 AX Switch 2 Way", "AHASXXW062", 119, "AHASXXG062", 145, "AHASXXB062", 145),
    ("6 A 1 Way Bell Push", "AHASBXW061", 124, "AHASBXG061", 150, "AHASBXB061", 150),
    ("16 AX Switch 1 Way", "AHASXXW161", 144, "AHASXXG161", 174, "AHASXXB161", 174),
    ("6 A 3 Pin Socket", "AHAKPXW063", 129, "AHAKPXG063", 157, "AHAKPXB063", 157),
    ("6 A/16 A Socket", "AHAKCXW163", 235, "AHAKCXG163", 292, "AHAKCXB163", 292),
    ("1 M Fan Regulator", "AHARFXW004", 440, "AHARFXG004", 548, "AHARFXB004", 548),
]

# Data for Magnus
magnus_items = [
    ("6 AX Switch 1 Way", "ACGSPXW061", 52, "ACGSPXG061", 68),
    ("6 AX Switch 2 Way", "ACGSPXW062", 163, "ACGSPXG062", 195),
    ("6 A 1 Way Bell Push", "ACGSBXW061", 198, "ACGSBXG061", 235),
    ("16 AX Switch 1 Way", "ACGSPXW161", 181, "ACGSPXG161", 216),
    ("6 A 3 Pin Socket", "ACGKPWW063", 157, "ACGKPWG063", 189),
    ("6 A/16 A Socket", "ACGKSWW163", 298, "ACGKSWG163", 356),
    ("1 M Fan Regulator", "ACGRFXW104", 537, "ACGRFXG104", 643),
]

if st.button("📥 পিডিএফ জেনারেট এবং ডাউনলোড করুন"):
    if uploaded_file is None:
        st.warning("দয়া করে প্রথমে প্রাইস লিস্ট পিডিএফ ফাইলটি আপলোড করুন।")
    else:
        # Generate PDF in memory buffer
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
        story.append(Paragraph("<b>Calculation Rules:</b> Net Price = List Price × 0.674 (32.6% Disc) | Sorted color-wise", subtitle_style))

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

        if series_choice == "Adiva":
            groups = [("WHITE", 1, 2), ("GREY", 3, 4), ("BLACK", 5, 6)]
            for color_label, sap_idx, lp_idx in groups:
                story.append(Paragraph(f"<b>ADIVA SERIES - {color_label} ITEMS</b>", section_style))
                rows = []
                for item in adiva_items:
                    name, sap, lp = item[0], item[sap_idx], item[lp_idx]
                    p_res = calc_all_prices(lp)
                    rows.append([name, sap, f"{lp:.0f}", f"{p_res[0]:.1f}"] + [f"{val:.1f}" for val in p_res[1:]])
                story.append(build_table(headers, rows))
                story.append(Spacer(1, 10))
        else: # Magnus
            groups = [("WHITE", 1, 2), ("GREY", 3, 4)]
            for color_label, sap_idx, lp_idx in groups:
                story.append(Paragraph(f"<b>MAGNUS SERIES - {color_label} ITEMS</b>", section_style))
                rows = []
                for item in magnus_items:
                    name, sap, lp = item[0], item[sap_idx], item[lp_idx]
                    p_res = calc_all_prices(lp)
                    rows.append([name, sap, f"{lp:.0f}", f"{p_res[0]:.1f}"] + [f"{val:.1f}" for val in p_res[1:]])
                story.append(build_table(headers, rows))
                story.append(Spacer(1, 10))

        doc.build(story)
        buffer.seek(0)

        st.success("পিডিএফ সফলভাবে তৈরি হয়েছে!")
        st.download_button(
            label=f"📥 {series_choice} Rate Chart PDF ডাউনলোড করুন",
            data=buffer,
            file_name=f"{series_choice.lower()}_rate_chart.pdf",
            mime="application/pdf"
                                   )
      
