"""Generates a test fixture PDF with wrapped names, glued tokens, and a page break."""

import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_fixture_pdf(output_path="tests/fixtures/ksamb_sample.pdf"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading2'], fontSize=12, leading=14)
    normal_style = ParagraphStyle('Normal', parent=styles['Normal'], fontSize=8, leading=10)

    story = []

    # Page 1 Header
    story.append(Paragraph("Commoditywise Daily Market Report For 11/11/2026", title_style))
    story.append(Spacer(1, 10))

    # Market 1
    story.append(Paragraph("1] MARKET: ANNIGERI", title_style))
    story.append(Spacer(1, 5))

    # Table 1 with wrapped commodity name and non-quintal unit
    data_p1 = [
        ["Commodity", "Variety", "Grade", "Arrivals", "Units", "Min (Rs.)", "Max (Rs.)", "Modal (Rs.)"],
        ["Cotton", "BT", "Medium", "1044", "Quintal", "9050", "9600", "9320"],
        ["Coconut (Per\n1000)", "Medium", "Medium", "500", "Numbers", "30000", "30000", "30000"],
        ["Tomato", "Tomato", "Average", "25", "Quintal", "1500", "2200", "1900"]
    ]
    t1 = Table(data_p1, colWidths=[90, 75, 55, 45, 50, 50, 50, 50])
    t1.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t1)

    # Page Break
    story.append(PageBreak())

    # Page 2: Glued token before market header "1900 2] MARKET: C.R.PATNA"
    story.append(Paragraph("1900 2] MARKET: C.R.PATNA", title_style))
    story.append(Spacer(1, 5))

    data_p2 = [
        ["Commodity", "Variety", "Grade", "Arrivals", "Units", "Min (Rs.)", "Max (Rs.)", "Modal (Rs.)"],
        ["Beans\n(Whole)", "Beans (Whole)", "Small", "17", "Quintal", "4000", "4500", "4100"],
        ["Onion", "Local", "Medium", "100", "Quintal", "3000", "4000", "3500"]
    ]
    t2 = Table(data_p2, colWidths=[90, 75, 55, 45, 50, 50, 50, 50])
    t2.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t2)

    doc.build(story)
    print(f"Generated test fixture at {output_path}")

if __name__ == "__main__":
    generate_fixture_pdf()
