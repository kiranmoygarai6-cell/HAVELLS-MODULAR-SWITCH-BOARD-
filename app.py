import streamlit as st
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io

st.set_page_config(page_title="Havells Crabtree Rate Chart Generator", layout="wide")

st.title("⚡ Havells Crabtree Rate & Margin Chart Generator")
st.write("সিরিজ সিলেক্ট করুন এবং ১৫% থেকে ২৭% পর্যন্ত মার্জিনযুক্ত সম্পূর্ণ রেট চার্ট পিডিএফ ডাউনলোড করুন।")

series_choice = st.selectbox("সিরিজ সিলেক্ট করুন:", ["Magnus", "Adiva"])

def calc_all_prices(lp):
    net = round(lp * 0.674, 2)  # 32.6% discount
    res = [net]
    for m in range(15, 28):
        res.append(round(net * (1 + m / 100.0), 2))
    return res

# Full Adiva Data
adiva_items = [
    ("6 AX Switch 1 Way", "AHASXXW061", 41, "AHASXXG061", 52, "AHASXXB061", 52),
    ("6 AX Switch 2 Way", "AHASXXW062", 119, "AHASXXG062", 145, "AHASXXB062", 145),
    ("6 A 1 Way Bell Push", "AHASBXW061", 124, "AHASBXG061", 150, "AHASBXB061", 150),
    ("6 A Switch 1 Way Bell Push Ind.", "AHASBIW061", 140, "AHASBIG061", 171, "AHASBIB061", 171),
    ("16 AX Switch 1 Way", "AHASXXW161", 144, "AHASXXG161", 174, "AHASXXB161", 174),
    ("16 AX Switch 1 Way Ind.", "AHASXIW161", 176, "AHASXIG161", 215, "AHASXIB161", 215),
    ("16 AX Switch 2 Way", "AHASXXW162", 184, "AHASXXG162", 226, "AHASXXB162", 226),
    ("25 A 1 Way Switch With Ind.", "AHASXIW251", 215, "AHASXIG251", 261, "AHASXIB251", 261),
    ("6 AX Mega Two Way Switch", "AHAMXXW062", 223, "AHAMXXG062", 272, "AHAMXXB062", 272),
    ("6 A Switch 1W Mega Bell Push Ind.", "AHAMBIW061", 172, "AHAMBIG061", 210, "AHAMBIB061", 210),
    ("20 A DP Switch 1 Way Ind.", "AHASDIW201", 284, "AHASDIG201", 345, "AHASDIB201", 345),
    ("32 A DP Switch 1 Way Ind.", "AHASDIW321", 303, "AHASDIG321", 371, "AHASDIB321", 371),
    ("6 AX One Way Flat Switch", "AHASPXW061", 48, "AHASPXG061", 63, "AHASPXB061", 63),
    ("6 AX 2 Way Flat Switch", "AHASPXW062", 124, "AHASPXG062", 157, "AHASPXB062", 157),
    ("6 A Bell Push Flat Switch", "AHASPKW061", 131, "AHASPKG061", 163, "AHASPKB061", 163),
    ("16 AX One Way Flat Switch", "AHASPXW161", 156, "AHASPXG161", 188, "AHASPXB161", 188),
    ("16 AX One Way Flat Ind Switch", "AHASPIW161", 188, "AHASPIG161", 223, "AHASPIB161", 223),
    ("6 A 3 Pin Socket", "AHAKPXW063", 129, "AHAKPXG063", 157, "AHAKPXB063", 157),
    ("6 A/16 A Socket", "AHAKCXW163", 235, "AHAKCXG163", 292, "AHAKCXB163", 292),
    ("16 A Heavy Duty Socket", "AHAKCXW253", 264, "AHAKCXG253", 318, "AHAKCXB253", 318),
    ("1 M Fan Regulator", "AHARFXW004", 440, "AHARFXG004", 548, "AHARFXB004", 548),
    ("2 M Fan Regulator", "AHARFHW005", 560, "AHARFHG005", 681, "AHARFHB005", 681),
    ("Telephone Socket - 1 M", "AHAKNWW111", 147, "AHAKNWG111", 176, "AHAKNWB111", 176),
    ("Computer Jack", "AHAKNWW451", 838, "AHAKNWG451", 1012, "AHAKNWB451", 1012),
    ("TV Socket", "AHAKTXW001", 140, "AHAKTXG001", 170, "AHAKTXB001", 170),
    ("Indicator Lamp", "AHAIIIW060", 116, "AHAIIIG060", 139, "AHAIIIB060", 139),
    ("1 M Dummy Plate", "AHAPFBWV01", 34, "AHAPFBGV01", 42, "AHAPFBBV01", 42),
    ("1 M USB Socket Type A 18 W", "AHAKGWW002", 1815, "AHAKGWG002", 2200, "AHAKGWB002", 2200),
    ("1 M USB Socket Type C 18 W", "AHAKGMW002", 1892, "AHAKGMG002", 2293, "AHAKGMB002", 2293),
    ("4 M Footlamp Color CCT", "AHAPFCWW04", 757, "AHAPFCGV04", 917, "AHAPFCBV04", 917),
    ("Footlamp-2 M", "AHAPFCWV02", 371, "AHAPFCGV02", 450, "AHAPFCBV02", 450),
    ("30 A Key Tag Mechanical", "AHASEXW000", 857, "AHASEXG000", 1037, "AHASEXB000", 1037),
    ("20 A Key Tag Electronic", "AHASEIW000", 2664, "AHASEIG000", 3228, "AHASEIB000", 3228),
    ("2 M Buzzer", "AHABXXW002", 277, "AHABXXG002", 340, "AHABXXB002", 340),
    ("DND & MMR Outdoor Panel - 1M", "AHASIIW061", 847, "AHASIIG061", 1028, "AHASIIB061", 1028),
    ("DND Two Way Switch (6 A)", "AHASXDW062", 368, "AHASXDG062", 445, "AHASXDB062", 445),
    ("MMR 1 Way Switch (6 A)", "AHASIXW061", 299, "AHASIXG061", 364, "AHASIXB061", 364),
    ("25 A Motor Starter", "AHASMXW251", 333, "AHASMXG251", 449, "AHASMXB251", 449),
    ("32 A Motor Starter", "AHASMXW321", 555, "AHASMXG321", 675, "AHASMXB321", 675),
    ("10 A SP 'C' Mini MCB", "DHANCSPA010", 345, "DHANCSPA100MR", 417, "DHANCSPA100EB", 417),
    ("16 A SP 'C' Mini MCB", "DHANCSPA016", 345, "DHANCSPA160MR", 417, "DHANCSPA160EB", 417),
    ("20 A SP 'C' Mini MCB", "DHANCSPA020", 345, "DHANCSPA200MR", 417, "DHANCSPA200EB", 417),
    ("25 A SP 'C' Mini MCB", "DHANCSPA025", 366, "DHANCSPA250MR", 441, "DHANCSPA250EB", 441),
    ("32 A SP 'C' Mini MCB", "DHANCSPA032", 366, "DHANCSPA320MR", 441, "DHANCSPA320EB", 441),
]

# Full Magnus Data
magnus_items = [
    ("6 AX Switch 1 Way", "ACGSPXW061", 52, "ACGSPXG061", 68),
    ("6 AX Switch 2 Way", "ACGSPXW062", 163, "ACGSPXG062", 195),
    ("6 A 1 Way Bell Push", "ACGSBXW061", 198, "ACGSBXG061", 235),
    ("16 AX Switch 1 Way", "ACGSPXW161", 181, "ACGSPXG161", 216),
    ("16 AX Switch 2 Way", "ACGSPXW162", 307, "ACGSPXG162", 365),
    ("16 AX Switch 1 Way Ind.", "ACGSPIW161", 263, "ACGSPIG161", 316),
    ("6 A Switch 1W Mega Bell Push Ind.", "ACGMBIW061", 241, "ACGMBIG061", 288),
    ("32 A DP Switch 1 Way Ind.", "ACGSDIW321", 574, "ACGSDIG321", 689),
    ("6 AX One Way Flat Switch", "ACGZPXW061", 58, "ACGZPXG061", 71),
    ("6 AX Two Way Flat Switch", "ACGZPXW062", 180, "ACGZPXG062", 215),
    ("6 A Bell Push Flat Switch", "ACGZBXW061", 220, "ACGZBXG061", 263),
    ("16 AX One Way Flat Switch", "ACGZPXW161", 198, "ACGZPXG161", 237),
    ("16 AX One Way Flat Switch Ind", "ACGZPIW161", 290, "ACGZPIG161", 350),
    ("6 A 3 Pin Socket", "ACGKPWW063", 157, "ACGKPWG063", 189),
    ("6 A/16 A Socket", "ACGKSWW163", 298, "ACGKSWG163", 356),
    ("1 M Fan Regulator", "ACGRFXW104", 537, "ACGRFXG104", 643),
    ("2 M Fan Regulator", "ACGRFHW015", 599, "ACGRFHG015", 720),
    ("2M BLDC Fan Regulator", "ACGRFEW005", 599, "ACGRFEG005", 720),
    ("Telephone Socket - 1 M", "ACGKNWW111", 172, "ACGKNWG111", 207),
    ("Computer Jack", "ACGKRWW451", 699, "ACGKRWG451", 838),
    ("TV Socket", "ACGKTCW111", 172, "ACGKTCG111", 207),
    ("Indicator Lamp", "ACGIPIW060", 139, "ACGIPIG061", 167),
    ("1 M Dummy Plate", "ACGPLBWW01", 42, "ACGPLBGW01", 51),
    ("1 M USB Socket 2.1 A", "ACGGGOW001", 799, "ACGGGOG001", 963),
    ("20 A Motor Starter", "ACGSMXW201", 371, "ACGSMXG201", 452),
    ("25 A Motor Starter", "ACGSMXW251", 407, "ACGSMXG251", 475),
    ("6 A SP 'C' Mini MCB", "DCSNCSPA61MMR", 316, "DCSNCSPA61MWH", 381),
    ("10 A SP 'C' Mini MCB", "DCSNCSPA101MMR", 316, "DCSNCSPA101MWH", 381),
    ("16 A SP 'C' Mini MCB", "DCSNCSPA161MMR", 316, "DCSNCSPA161MWH", 381),
    ("20 A SP 'C' Mini MCB", "DCSNCSPA201MMR", 316, "DCSNCSPA201MWH", 381),
    ("25 A SP 'C' Mini MCB", "DCSNCSPA251MMR", 316, "DCSNCSPA251MWH", 381),
    ("32 A SP 'C' Mini MCB", "DCSNCSPA321MMR", 316, "DCSNCSPA321MWH", 381),
]

if st.button("📥 পিডিএফ জেনারেট এবং ডাউনলোড করুন"):
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
        label=f"📥 {series_choice} Complete Rate Chart PDF ডাউনলোড করুন",
        data=buffer,
        file_name=f"{series_choice.lower()}_complete_rate_chart.pdf",
        mime="application/pdf"
    )
