from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, FrameBreak, Table
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
styleSheet = getSampleStyleSheet()


def create_invoice_pdf(month, pdf_path):
    doc = BaseDocTemplate(pdf_path, pagesize=A4, showBoundary=True)

    invoice_template = get_invoice_template(doc)
    doc.addPageTemplates([invoice_template])
    elements = get_invoice_text()
    doc.build(elements)


def get_invoice_text():
    styleSheet = getSampleStyleSheet()
    invoice_style = ParagraphStyle(name='InbvoiceStype', parent=styleSheet['Normal'], fontSize=10)


    return [
        get_address_paragraph(invoice_style),
        FrameBreak(),
        get_invoice_paragraph(invoice_style),
        FrameBreak(),
        get_service_table(),
        FrameBreak(),
        get_method_of_payment_paragraph(invoice_style),
        FrameBreak(),
        get_amount_table(),
        FrameBreak(),
        get_legal_paragraph(invoice_style)]


def get_address_paragraph(style):
    text = '''Consulting <br />
    address
    '''

    return Paragraph(text, style)


def get_invoice_paragraph(style):
    text = '''INVOICE<br />
    Invoice number
    '''
    return Paragraph(text, style)


def get_service_table():
    table_data = [
        ['Nr.', 'Name of Service', 'Units', 'Price per\nUnit', 'Value\n(without\nTAX)', 'TAX\nrate', 'Tax\nValue', 'Value'],
        [],
        ['1.', 'Software Development', '', '', '', '', '', ''],
        []
    ]
    table_style = [
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]
    return Table(table_data, style=table_style)


def get_method_of_payment_paragraph(style):
    text = '''Method of Payment<br />
    Money transfer to bank account<br />
    '''
    return Paragraph(text, style)


def get_amount_table():
    table_data = [
        ['Total value excluding VAT:', ''],
        ['Total VAT:', ''],
        [],
        ['TOTAL VALUE:', ''],
        ['Already paid:', ''],
        ['Remain for Payment:', '']
    ]
    return Table(table_data)


def get_legal_paragraph(style):
    text = ''
    return Paragraph(text, style)


def get_invoice_template(doc):
    x1 = doc.leftMargin
    y1 = doc.rightMargin
    w = doc.width
    h = doc.height
    space = 6

    half_width = w / 2 - space

    sep1_y = y1 + h * 2 / 3
    sep1_x = x1 + w / 2 + space
    height1 = h * 1 / 3 - space
    address = Frame(x1, sep1_y, half_width, height1, id='address')
    invoice_data = Frame(sep1_x, sep1_y, half_width, height1, id='invoice_data')

    sep2_y = y1 + h * 1 / 3
    service = Frame(x1, sep2_y, w, height1, id='service')

    sep3_y = y1 + h * 1 / 20
    height3 = h * 1 / 3 - h * 1 / 20 - space
    payment = Frame(x1, sep3_y, half_width, height3, id='payment')
    amount = Frame(sep1_x, sep3_y, half_width, height3, id='amount')

    height4 = h * 1 / 20 - space
    legal = Frame(x1, y1, w, height4, id='legal')

    frames = [address, invoice_data, service, payment, amount, legal]
    return PageTemplate(id='invoice_template', frames=frames)
