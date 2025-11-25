"""
Create a realistic sample invoice PDF for testing
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from datetime import datetime

# Create PDF
pdf = SimpleDocTemplate("sample_invoice.pdf", pagesize=letter,
                       rightMargin=0.5*inch, leftMargin=0.5*inch,
                       topMargin=0.5*inch, bottomMargin=0.5*inch)
story = []

# Styles
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))

# Company Header
story.append(Paragraph("<b><font size=18>TECHWAVE SOLUTIONS PVT LTD</font></b>", styles['Center']))
story.append(Paragraph("<font size=9>456 MG Road, Bangalore - 560001, Karnataka, India</font>", styles['Center']))
story.append(Paragraph("<font size=9>Phone: +91-80-4567-8900 | Email: billing@techwave.com</font>", styles['Center']))
story.append(Paragraph("<font size=9><b>GST No: 29AABCT1234A1Z5</b></font>", styles['Center']))
story.append(Spacer(1, 0.3*inch))

# Invoice Title
story.append(Paragraph("<b><font size=16 color='#366092'>TAX INVOICE</font></b>", styles['Center']))
story.append(Spacer(1, 0.2*inch))

# Invoice Details (two columns)
invoice_info = [
    [Paragraph("<b>Invoice No:</b> INV-2024-0847", styles['Normal']),
     Paragraph("<b>Date:</b> November 25, 2024", styles['Right'])],
    [Paragraph("<b>PO No:</b> PO/2024/3421", styles['Normal']),
     Paragraph("<b>Due Date:</b> December 10, 2024", styles['Right'])],
]
invoice_table = Table(invoice_info, colWidths=[3.5*inch, 3.5*inch])
invoice_table.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
]))
story.append(invoice_table)
story.append(Spacer(1, 0.3*inch))

# Bill To / Ship To
billing_info = [
    [Paragraph("<b>BILL TO:</b>", styles['Normal']),
     Paragraph("<b>SHIP TO:</b>", styles['Normal'])],
    [Paragraph("Global Retail Corp<br/>Attn: Accounts Payable<br/>789 Commercial Street<br/>Mumbai - 400013, Maharashtra<br/><b>GST: 27AAGCG1234H1ZN</b>", styles['Normal']),
     Paragraph("Global Retail Corp<br/>Warehouse 5<br/>Plot No. 45, MIDC Area<br/>Pune - 411019, Maharashtra", styles['Normal'])],
]
billing_table = Table(billing_info, colWidths=[3.5*inch, 3.5*inch])
billing_table.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8E8E8')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
]))
story.append(billing_table)
story.append(Spacer(1, 0.3*inch))

# Items Table
items_data = [
    ['Item', 'Description', 'HSN', 'Qty', 'Rate', 'Amount'],
    ['1', 'Cloud Server Hosting - Annual', '998314', '1', '₹85,000', '₹85,000'],
    ['2', 'SSL Certificate (Wildcard)', '998315', '2', '₹12,000', '₹24,000'],
    ['3', 'Technical Support - Premium', '998316', '12', '₹8,500', '₹1,02,000'],
    ['4', 'Data Backup Service', '998317', '1', '₹15,000', '₹15,000'],
]

items_table = Table(items_data, colWidths=[0.4*inch, 2.8*inch, 0.8*inch, 0.6*inch, 1*inch, 1.2*inch])
items_table.setStyle(TableStyle([
    # Header
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#366092')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    
    # Body
    ('ALIGN', (0, 1), (0, -1), 'CENTER'),
    ('ALIGN', (2, 1), (-1, -1), 'CENTER'),
    ('ALIGN', (4, 1), (-1, -1), 'RIGHT'),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
]))
story.append(items_table)
story.append(Spacer(1, 0.2*inch))

# Totals Table
totals_data = [
    ['', '', '', '', 'Subtotal:', '₹2,26,000'],
    ['', '', '', '', 'CGST @ 9%:', '₹20,340'],
    ['', '', '', '', 'SGST @ 9%:', '₹20,340'],
    ['', '', '', '', '<b>Total Amount:</b>', '<b>₹2,66,680</b>'],
]

totals_table = Table(totals_data, colWidths=[0.4*inch, 2.8*inch, 0.8*inch, 0.6*inch, 1*inch, 1.2*inch])
totals_table.setStyle(TableStyle([
    ('ALIGN', (4, 0), (-1, -1), 'RIGHT'),
    ('FONTNAME', (4, 3), (-1, 3), 'Helvetica-Bold'),
    ('FONTSIZE', (4, 3), (-1, 3), 11),
    ('LINEABOVE', (4, 3), (-1, 3), 1.5, colors.black),
    ('BACKGROUND', (4, 3), (-1, 3), colors.HexColor('#E8E8E8')),
]))
story.append(totals_table)
story.append(Spacer(1, 0.3*inch))

# Payment Terms
story.append(Paragraph("<b>Amount in Words:</b> Rupees Two Lakh Sixty-Six Thousand Six Hundred Eighty Only", styles['Normal']))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("<b>Payment Terms:</b> Net 15 days | Bank: HDFC Bank | A/C: 50200012345678 | IFSC: HDFC0001234", styles['Normal']))
story.append(Spacer(1, 0.3*inch))

# Footer
story.append(Paragraph("<font size=8><i>This is a computer-generated invoice and does not require a signature.</i></font>", styles['Center']))

# Build PDF
pdf.build(story)

print("✅ Created: sample_invoice.pdf")
print("   Run 'python digitalise_image_pdf.py' to process it!")
