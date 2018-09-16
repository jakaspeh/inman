from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, FrameBreak, Table
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from inman.get_invoice_data import get_invoice_data

styleSheet = getSampleStyleSheet()


def create_invoice_pdf(month, pdf_path):
    show_boundary = False
    doc = BaseDocTemplate(pdf_path, pagesize=A4, showBoundary=show_boundary)

    invoice_template = get_invoice_template(doc)
    doc.addPageTemplates([invoice_template])
    elements = get_invoice_text(month)
    doc.build(elements)


def get_invoice_text(month):

    invoice_style = ParagraphStyle(name='InbvoiceStype', parent=styleSheet['Normal'], fontSize=10)
    invoice_data = get_invoice_data(month)
    return [
        get_address_paragraph(invoice_data),
        FrameBreak(),
        get_invoice_title(),
        get_invoice_table(invoice_data, invoice_style),
        FrameBreak(),
        get_service_table(invoice_data),
        FrameBreak(),
        get_method_of_payment_paragraph(invoice_style),
        get_method_of_payment_table(invoice_data),
        FrameBreak(),
        get_amount_table(invoice_data),
        FrameBreak(),
        get_legal_paragraph(invoice_style)]


def get_address_paragraph(invoice_data):
    s = ParagraphStyle('address', fontSize=12, leading=16)

    me = invoice_data.me
    text = '{}<br />'.format(me.name)
    text += '{}, {}, {}<br />'.format(me.address, me.post, me.country)
    text += 'VAT Nr.: {}<br />'.format(me.vat_number)
    text += '<a href="mailto:{0}"><font color="blue">{0}</font></a><br />'.format(me.email)
    text += 'Tel.: {}<br /><br /><br />'.format(me.telephone)
    text += '<br /><br /><br />'

    customer = invoice_data.get_customer()
    text += '{}<br />'.format(customer.name)
    text += '{}<br />'.format(customer.address)
    text += '{}<br />'.format(customer.post)
    text += '{}<br />'.format(customer.country)
    text += 'VAT Nr.: {}<br />'.format(customer.vat_number)
    return Paragraph(text, s)


def get_invoice_title():
    invoice_title_style = styleSheet['title']
    return Paragraph('<br /><br /><br />INVOICE<br />', style=invoice_title_style)


def get_invoice_table(invoice_data, style):
    table_data = [
        ['Invoice Number:', invoice_data.invoice_number],
        [],
        ['Invoice Date:', invoice_data.invoice_date],
        ['Order Number:'],
        ['Date of Service:', invoice_data.date_of_service],
        ['Date of Sale:'],
        [],
        ['Payment Due:', invoice_data.payment_due],
        ['Payment Reference:', invoice_data.payment_reference]
    ]
    table_style = [('FONTSIZE', (0, 0), (-1, -1), 12)]
    return Table(table_data, style=table_style, rowHeights=16)


def get_service_table(invoice_data):
    table_data = [
        ['Nr.', 'Name of Service', 'Units', 'Price per\nUnit', 'Value\n(without\nTAX)', 'TAX\nrate', 'Tax\nValue', 'Value'],
        [],
    ]

    for i, service in enumerate(invoice_data.services):
        number = '{}.'.format(i + 1)
        value = service.get_value()
        value_str = '{0:.2f} €'.format(value)
        price_per_unit = float(service.price_per_unit)
        price_per_unit_str = '{0:.2f} €'.format(price_per_unit)

        lst = [number, service.name_of_service, service.units, price_per_unit_str,
               value_str, '0.00 %', '0.00 €', value_str]
        table_data.append(lst)

    table_data.append([])

    table_style = [
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]
    return Table(table_data, style=table_style)


def get_method_of_payment_paragraph(style):
    text = '''Method of Payment:<br /><br />
    Money Transfer to the Bank Account:<br />
    '''
    return Paragraph(text, style)


def get_method_of_payment_table(invoice_data):
    me = invoice_data.me

    table = [['Bank:', me.bank],
             ['IBAN:', me.iban],
             ['BIC:', me.bic],
             ['Reference:', invoice_data.payment_reference],
             [],
             ['VAT Number:', me.vat_number],
             ['Reg. Number:', me.reg_number]]

    return Table(table)


def get_amount_table(invoice_data):
    total_value = '{0:.2f} €'.format(invoice_data.get_value())
    zero_value = '0.00 €'

    table_data = [
        ['Total value excluding VAT:', total_value],
        ['Total VAT:', zero_value],
        [],
        ['TOTAL VALUE:', total_value],
        ['Already paid:', zero_value],
        ['Remain for Payment:', total_value]
    ]
    return Table(table_data)


def get_legal_paragraph(style):
    text = 'VAT reverse charge according to Paragraph 1 of Article 25 of ZDDV-1'
    return Paragraph(text, style)


def get_invoice_template(doc):
    x1 = doc.leftMargin
    y1 = doc.rightMargin
    w = doc.width
    h = doc.height
    space = 6

    w_address = 13
    w_service = 10
    w_payment = 8
    w_legal = 2
    total = w_address + w_service + w_payment + w_legal

    h_address = w_address / total
    h_service = w_service / total
    h_payment = w_payment / total
    h_legal = w_legal / total

    half_width = w / 2 - space

    sep1_y = y1 + h * (1 - h_address)
    sep1_x = x1 + w / 2 + space
    height1 = h * h_address - space
    address = Frame(x1, sep1_y, half_width, height1, id='address')
    invoice_data = Frame(sep1_x, sep1_y, half_width, height1, id='invoice_data')

    sep2_y = y1 + h * (1 - h_address - h_service)
    height2 = h * h_service - space
    service = Frame(x1, sep2_y, w, height2, id='service')

    sep3_y = y1 + h * (1 - h_address - h_service - h_payment)
    height3 = h * h_payment - space
    payment = Frame(x1, sep3_y, half_width, height3, id='payment')
    amount = Frame(sep1_x, sep3_y, half_width, height3, id='amount')

    height4 = h * h_legal - space
    legal = Frame(x1, y1, w, height4, id='legal')

    frames = [address, invoice_data, service, payment, amount, legal]
    return PageTemplate(id='invoice_template', frames=frames)
