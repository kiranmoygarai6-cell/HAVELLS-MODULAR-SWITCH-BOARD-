import streamlit as st
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io

st.set_page_config(page_title="Havells Crabtree Rate Chart Generator", layout="wide")

st.title("⚡ Havells Crabtree Rate & Margin Chart Generator")
st.write("সিরিজ সিলেক্ট করুন এবং ১৫% থেকে ২৭% পর্যন্ত মার্জিনযুক্ত সম্পূর্ণ রেট চার্ট (সুইচ, সকেট ও প্লেটসহ) পিডিএফ ডাউনলোড করুন।")

series_choice = st.selectbox("সিরিজ সিলেক্ট করুন:", ["Magnus", "Adiva"])

def calc_all_prices(lp):
    net = round(lp * 0.674, 2)  # 32.6% discount
    res = [net]
    for m in range(15, 28):
        res.append(round(net * (1 + m / 100.0), 2))
    return res

# ----------------- ADIVA DATA -----------------
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

adiva_plates = [
    ("Combined Plates - White", {1: ("AHAPLCWV01", 108), 2: ("AHAPLCWV02", 108), 3: ("AHAPLCWV03", 147), 4: ("AHAPLCWV04", 169), 6: ("AHAPLCWV06", 249), 8: ("AHAPLCWV08", 316), "8H": ("AHAPLCWH08", 316), 9: ("AHAPLCWV09", 352), 12: ("AHAPLCWV12", 382), 16: ("AHAPLCWV16", 402), 18: ("AHAPLCWV18", 417)}),
    ("Combined Plates - Grey", {1: ("AHAPLCGV01", 123), 2: ("AHAPLCGV02", 123), 3: ("AHAPLCGV03", 169), 4: ("AHAPLCGV04", 195), 6: ("AHAPLCGV06", 285), 8: ("AHAPLCGV08", 365), "8H": ("AHAPLCGH08", 365), 9: ("AHAPLCGV09", 409), 12: ("AHAPLCGV12", 443), 16: ("AHAPLCGV16", 464), 18: ("AHAPLCGV18", 481)}),
    ("Combined Plates - Black", {1: ("AHAPLCBV01", 123), 2: ("AHAPLCBV02", 123), 3: ("AHAPLCBV03", 169), 4: ("AHAPLCBV04", 195), 6: ("AHAPLCBV06", 285), 8: ("AHAPLCBV08", 365), "8H": ("AHAPLCBH08", 365), 9: ("AHAPLCBV09", 409), 12: ("AHAPLCBV12", 443), 16: ("AHAPLCBV16", 464), 18: ("AHAPLCBV18", 481)}),
    ("Combined Plates - White with Chrome Bezel", {1: ("AHAPLBWV01", 120), 2: ("AHAPLBWV02", 120), 3: ("AHAPLBWV03", 161), 4: ("AHAPLBWV04", 188), 6: ("AHAPLBWV06", 272), 8: ("AHAPLBWV08", 350), "8H": ("AHAPLBWH08", 350), 9: ("AHAPLBWV09", 391), 12: ("AHAPLBWV12", 423), 16: ("AHAPLBWV16", 445), 18: ("AHAPLBWV18", 463)}),
    ("Combined Plates - White with Rose Gold", {1: ("AHAPLBAV01", 122), 2: ("AHAPLBAV02", 122), 3: ("AHAPLBAV03", 164), 4: ("AHAPLBAV04", 193), 6: ("AHAPLBAV06", 280), 8: ("AHAPLBAV08", 357), "8H": ("AHAPLBAH08", 357), 9: ("AHAPLBAV09", 402), 12: ("AHAPLBAV12", 433), 16: ("AHAPLBAV16", 455), 18: ("AHAPLBAV18", 473)}),
    ("Combined Plates - Grey with Rose Gold", {1: ("AHAPLBGV01", 148), 2: ("AHAPLBGV02", 148), 3: ("AHAPLBGV03", 200), 4: ("AHAPLBGV04", 229), 6: ("AHAPLBGV06", 336), 8: ("AHAPLBGV08", 430), "8H": ("AHAPLBGH08", 430), 9: ("AHAPLBGV09", 482), 12: ("AHAPLBGV12", 524), 16: ("AHAPLBGV16", 547), 18: ("AHAPLBGV18", 569)}),
    ("Combined Plates - Black with Rose Gold", {1: ("AHAPLBBV01", 148), 2: ("AHAPLBBV02", 148), 3: ("AHAPLBBV03", 200), 4: ("AHAPLBBV04", 229), 6: ("AHAPLBBV06", 336), 8: ("AHAPLBBV08", 430), "8H": ("AHAPLBBH08", 430), 9: ("AHAPLBBV09", 482), 12: ("AHAPLBBV12", 524), 16: ("AHAPLBBV16", 547), 18: ("AHAPLBBV18", 569)}),
    ("Combined Plates - Blue with Chrome Bezel", {1: ("AHAPLBUV01", 143), 2: ("AHAPLBUV02", 145), 3: ("AHAPLBUV03", 195), 4: ("AHAPLBUV04", 223), 6: ("AHAPLBUV06", 328), 8: ("AHAPLBUV08", 418), "8H": ("AHAPLBUH08", 418), 9: ("AHAPLBUV09", 470), 12: ("AHAPLBUV12", 511), 16: ("AHAPLBUV16", 532), 18: ("AHAPLBUV18", 553)}),
    ("Combined Plates - Champagne Gold with Rose Gold", {1: ("AHAPLBRV01", 148), 2: ("AHAPLBRV02", 150), 3: ("AHAPLBRV03", 200), 4: ("AHAPLBRV04", 229), 6: ("AHAPLBRV06", 336), 8: ("AHAPLBRV08", 430), "8H": ("AHAPLBRH08", 430), 9: ("AHAPLBRV09", 482), 12: ("AHAPLBRV12", 524), 16: ("AHAPLBRV16", 547), 18: ("AHAPLBRV18", 569)}),
    ("Combined Plates - Rustic Bronze with Rose Gold", {1: ("AHAPLBMV01", 148), 2: ("AHAPLBMV02", 150), 3: ("AHAPLBMV03", 200), 4: ("AHAPLBMV04", 229), 6: ("AHAPLBMV06", 336), 8: ("AHAPLBMV08", 430), "8H": ("AHAPLBMH08", 430), 9: ("AHAPLBMV09", 482), 12: ("AHAPLBMV12", 524), 16: ("AHAPLBMV16", 547), 18: ("AHAPLBMV18", 569)})
]

# ----------------- MAGNUS DATA -----------------
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

magnus_plates = [
    ("Combined Plates - Acrylic Steel Grey", {1: ("ACGPTOFV01", 292), 2: ("ACGPTOFV02", 292), 3: ("ACGPTOFV03", 349), 4: ("ACGPTOFV04", 427), 6: ("ACGPTOFV06", 579), 8: ("ACGPTOFV08", 760), "8H": ("ACGPTOFH08", 760), 12: ("ACGPTOFV12", 965), 16: ("ACGPTOFV16", 1252), 18: ("ACGPTOFV18", 1255)}),
    ("Combined Plates - Acrylic Brown", {1: ("ACGPTOAV01", 292), 2: ("ACGPTOAV02", 292), 3: ("ACGPTOAV03", 349), 4: ("ACGPTOAV04", 427), 6: ("ACGPTOAV06", 579), 8: ("ACGPTOAV08", 760), "8H": ("ACGPTOAH08", 760), 12: ("ACGPTOAV12", 965), 16: ("ACGPTOAV16", 1252), 18: ("ACGPTOAV18", 1255)}),
    ("Combined Plates - Acrylic Black", {1: ("ACGPTOBV01", 292), 2: ("ACGPTOBV02", 292), 3: ("ACGPTOBV03", 349), 4: ("ACGPTOBV04", 427), 6: ("ACGPTOBV06", 579), 8: ("ACGPTOBV08", 760), "8H": ("ACGPTOBH08", 760), 12: ("ACGPTOBV12", 965), 16: ("ACGPTOBV16", 1252), 18: ("ACGPTOBV18", 1255)}),
    ("Combined Plates - Acrylic White", {1: ("ACGPTOWW01", 292), 2: ("ACGPTOWV02", 292), 3: ("ACGPTOWV03", 349), 4: ("ACGPTOWV04", 427), 6: ("ACGPTOWV06", 579), 8: ("ACGPTOWV08", 760), "8H": ("ACGPTOWH08", 760), 12: ("ACGPTOWW12", 965), 16: ("ACGPTOWW16", 1252), 18: ("ACGPTOWW18", 1255)}),
    ("Combined Plates - Acrylic Sea Green", {1: ("ACGPTONV01", 292), 2: ("ACGPTONV02", 292), 3: ("ACGPTONV03", 349), 4: ("ACGPTONV04", 427), 6: ("ACGPTONV06", 579), 8: ("ACGPTONV08", 760), "8H": ("ACGPTONH08", 760), 12: ("ACGPTONV12", 965), 16: ("ACGPTONV16", 1252), 18: ("ACGPTONV18", 1255)}),
    ("Combined Plates - Acrylic Walnut Wood", {1: ("ACGPTODV01", 303), 2: ("ACGPTODV02", 303), 3: ("ACGPTODV03", 359), 4: ("ACGPTODV04", 441), 6: ("ACGPTODV06", 594), 8: ("ACGPTODV08", 782), "8H": ("ACGPTODH08", 782), 12: ("ACGPTODV12", 994), 16: ("ACGPTODV16", 1286), 18: ("ACGPTODV18", 1293)}),
    ("Combined Plates - Matt White", {1: ("ACGPPCWW01", 127), 2: ("ACGPPCWV02", 127), 3: ("ACGPPCWV03", 151), 4: ("ACGPPCWV04", 185), 6: ("ACGPPCWV06", 251), 8: ("ACGPPCWV08", 331), "8H": ("ACGPPCWH08", 331), 12: ("ACGPPCWW12", 418), 16: ("ACGPPCWW16", 544), 18: ("ACGPPCWW18", 545)}),
    ("Combined Plates - Matt Grey", {1: ("ACGPPCGV01", 149), 2: ("ACGPPCGV02", 149), 3: ("ACGPPCGV03", 179), 4: ("ACGPPCGV04", 218), 6: ("ACGPPCGV06", 296), 8: ("ACGPPCGV08", 386), "8H": ("ACGPPCGH08", 386), 12: ("ACGPPCGV12", 490), 16: ("ACGPPCGV16", 638), 18: ("ACGPPCGV18", 641)}),
    ("Combined Plates - Matt Gold", {1: ("ACGPPCLV01", 149), 2: ("ACGPPCLV02", 149), 3: ("ACGPPCLV03", 179), 4: ("ACGPPCLV04", 218), 6: ("ACGPPCLV06", 296), 8: ("ACGPPCLV08", 386), "8H": ("ACGPPCLH08", 386), 12: ("ACGPPCLV12", 490), 16: ("ACGPPCLV16", 638), 18: ("ACGPPCLV18", 641)})
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
        
        # Add Plates for Adiva
        story.append(Paragraph("<b>ADIVA SERIES - MODULAR COMBINED PLATES</b>", section_style))
        for group_name, pdict in adiva_plates:
            story.append(Paragraph(f"<b>{group_name}</b>", ParagraphStyle('SubSec', parent=styles['Heading3'], fontSize=9.5, textColor=colors.HexColor('#0D47A1'), spaceBefore=6, spaceAfter=2)))
            p_rows = []
            for size_key, (sap, lp) in pdict.items():
                p_res = calc_all_prices(lp)
                size_str = f"{size_key} M" if str(size_key).isdigit() else f"{size_key}"
                p_rows.append([f"Combined Plate - {size_str}", sap, f"{lp:.0f}", f"{p_res[0]:.1f}"] + [f"{val:.1f}" for val in p_res[1:]])
            story.append(build_table(headers, p_rows))
            story.append(Spacer(1, 6))

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
            
        # Add Plates for Magnus
        story.append(Paragraph("<b>MAGNUS SERIES - MODULAR COMBINED PLATES</b>", section_style))
        for group_name, pdict in magnus_plates:
            story.append(Paragraph(f"<b>{group_name}</b>", ParagraphStyle('SubSec', parent=styles['Heading3'], fontSize=9.5, textColor=colors.HexColor('#0D47A1'), spaceBefore=6, spaceAfter=2)))
            p_rows = []
            for size_key, (sap, lp) in pdict.items():
                p_res = calc_all_prices(lp)
                size_str = f"{size_key} M" if str(size_key).isdigit() else f"{size_key}"
                p_rows.append([f"Combined Plate - {size_str}", sap, f"{lp:.0f}", f"{p_res[0]:.1f}"] + [f"{val:.1f}" for val in p_res[1:]])
            story.append(build_table(headers, p_rows))
            story.append(Spacer(1, 6))

    doc.build(story)
    buffer.seek(0)

    st.success("পিডিএফ সফলভাবে তৈরি হয়েছে!")
    st.download_button(
        label=f"📥 {series_choice} Complete Rate Chart (With Plates) PDF ডাউনলোড করুন",
        data=buffer,
        file_name=f"{series_choice.lower()}_complete_rate_chart.pdf",
        mime="application/pdf"
    )
RIES - {color_label} ITEMS</b>", section_style))
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
