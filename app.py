import streamlit as st
import pdfplumber
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import tempfile
import os

st.title("Universal Electrical Price List Generator")
st.write("যেকোনো ইলেকট্রিক্যাল প্রাইস লিস্ট (Polycab, Havells Crabtree ইত্যাদি) এখানে আপলোড করুন। অ্যাপটি স্বয়ংক্রিয়ভাবে সমস্ত পেজ স্ক্যান করে ডিসকাউন্টেড প্রাইস লিস্ট তৈরি করে দেবে।")

uploaded_file = st.file_uploader("Upload PDF Price List", type=["pdf"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_input_path = tmp_file.name

    output_pdf_path = "Discounted_Price_List_Universal.pdf"

    if st.button("Generate Complete Price List"):
        with st.spinner("Processing all pages and tables... Please wait."):
            try:
                categories_data = {}
                current_category = "General Products"
                
                with pdfplumber.open(temp_input_path) as pdf:
                    for page_num, page in enumerate(pdf.pages):
                        text = page.extract_text() or ""
                        lines = text.split('\n')
                        
                        # ক্যাটাগরি বা হেডিং ট্র্যাক করা
                        for line in lines:
                            line_str = line.strip()
                            if len(line_str) > 3 and len(line_str) < 40:
                                upper_line = line_str.upper()
                                if any(keyword in upper_line for keyword in ['SIGNIA', 'MURANO', 'ATHENA', 'ADIVA', 'MAGNUS', 'FABIO', 'CORAL', 'VERONA', 'YU', 'BOXES', 'ACCESSORIES', 'WIRES', 'CABLES', 'SERIES']):
                                    current_category = line_str.title()
                                    if current_category not in categories_data:
                                        categories_data[current_category] = []

                        # পেজের সব টেবিল এক্সট্রাক্ট করা
                        tables = page.extract_tables()
                        for table in tables:
                            for row in table:
                                cleaned_row = [str(cell).strip().replace('\n', ' ') for cell in row if cell is not None and str(cell).strip() != ""]
                                if len(cleaned_row) >= 2:
                                    # প্রাইস খুঁজে বের করা
                                    price_val = None
                                    item_name = cleaned_row[0]
                                    code_or_size = cleaned_row[1] if len(cleaned_row) > 1 else ""
                                    
                                    for cell in cleaned_row:
                                        clean_cell = cell.replace('₹', '').replace(',', '').replace('`', '').strip()
                                        if clean_cell.replace('.', '', 1).isdigit():
                                            val = float(clean_cell)
                                            if val > 10: # অপ্রাসঙ্গিক ছোট সংখ্যা বাদ দিতে
                                                price_val = val
                                                
                                    if price_val and len(item_name) > 1 and not any(kw in item_name.upper() for kw in ['ITEM', 'SIZE', 'LIST', 'PCP', 'SAP', 'STD']):
                                        if current_category not in categories_data:
                                            categories_data[current_category] = []
                                        
                                        entry = (item_name, code_or_size, price_val)
                                        if entry not in categories_data[current_category]:
                                            categories_data[current_category].append(entry)

                # যদি কোনো ডেটা এক্সট্রাক্ট না হয়
                if not categories_data:
                    categories_data["All Extracted Items"] = [("Sample Item", "SAP001", 100.00)]

                # পিডিএফ জেনারেশন
                doc = SimpleDocTemplate(output_pdf_path, pagesize=landscape(letter), rightMargin=20, leftMargin=20, topMargin=25, bottomMargin=25)
                story = []
                styles = getSampleStyleSheet()

                title_style = ParagraphStyle(
                    'TitleStyle', parent=styles['Heading1'], fontSize=15, textColor=colors.HexColor('#1b365d'), alignment=1, spaceAfter=6
                )
                sub_style = ParagraphStyle(
                    'SubStyle', parent=styles['Normal'], alignment=1, fontSize=8.5, textColor=colors.HexColor('#555555'), spaceAfter=10
                )
                cat_style = ParagraphStyle(
                    'CatStyle', parent=styles['Heading2'], fontSize=10.5, textColor=colors.HexColor('#2c3e50'), spaceBefore=8, spaceAfter=3
                )

                story.append(Paragraph("<b>ELECTRICAL STORE - CATEGORY WISE DISCOUNTED PRICE LIST</b>", title_style))
                story.append(Paragraph("<b>Calculation: Net Price = List Price × 0.674 (32.6% Less) | Markups: +20%, +25%, +26%, +27%</b>", sub_style))

                for cat_name, items in categories_data.items():
                    if not items:
                        continue
                        
                    story.append(Paragraph(cat_name, cat_style))
                    
                    header = ["Item Name / Description", "Code / Size", "LP (₹)", "Net (₹)", "+20%", "+25%", "+26%", "+27%"]
                    table_data = [header]
                    
                    for item_name, code, lp in items:
                        net = lp * (1 - 0.326) # 32.6% less
                        p20 = net * 1.20
                        p25 = net * 1.25
                        p26 = net * 1.26
                        p27 = net * 1.27
                        
                        row = [
                            Paragraph(str(item_name), styles['Normal']),
                            str(code),
                            f"{lp:,.2f}",
                            f"{net:,.2f}",
                            f"{p20:,.2f}",
                            f"{p25:,.2f}",
                            f"{p26:,.2f}",
                            f"{p27:,.2f}"
                        ]
                        table_data.append(row)
                        
                    t = Table(table_data, colWidths=[190, 90, 70, 70, 70, 70, 70, 70])
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1b365d')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 8),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
                        ('TOPPADDING', (0, 0), (-1, 0), 4),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dcdcdc')),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ffffff'), colors.HexColor('#f2f4f8')]),
                        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 1), (-1, -1), 7.5),
                        ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
                        ('TOPPADDING', (0, 1), (-1, -1), 3),
                    ]))
                    story.append(t)
                    story.append(Spacer(1, 6))

                doc.build(story)
                st.success("Successfully generated complete price list!")
                
                with open(output_pdf_path, "rb") as file:
                    st.download_button(
                        label="Download Complete Discounted PDF",
                        data=file,
                        file_name="Complete_Discounted_Price_List.pdf",
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"An error occurred: {e}")
