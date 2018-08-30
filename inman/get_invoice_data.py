from inman.google_sheet import get_raw_data_from_google_sheets
from inman.config import get_invoice_spreadsheet_id
from inman.months import month_to_string


class Customer:

    def __init__(self):
        self.name = ''
        self.address = ''
        self.post = ''
        self.country = ''
        self.vat_number = ''

    def __str__(self):
        s1 = 'Customer {}\naddress: {}\n'.format(self.name, self.address)
        s2 = 'post: {}\ncountry{}\nvat nr.{}\n'.format(self.post, self.country, self.vat_number)
        return s1 + s2

    @classmethod
    def create_customer(cls, general_data, customer_number):
        i = str(customer_number)
        customer = cls()
        customer.name = general_data['customer_' + i]
        customer.address = general_data['customer_address_' + i]
        customer.post = general_data['customer_post_' + i]
        customer.country = general_data['customer_country_' + i]
        customer.vat_number = general_data['customer_vat_nr_' + i]

        return customer


class Me:

    def __init__(self):
        self.name = ''
        self.address = ''
        self.post = ''
        self.country = ''

        self.email = ''
        self.telephone = ''

        self.vat_number = ''
        self.reg_number = ''

        self.bank = ''
        self.iban = ''
        self.bic = ''

    def __str__(self):
        s1 = 'Myself: {}\naddress {}, {}, {}\n\n'.format(self.name, self.address, self.post, self.country)
        s2 = 'email: {}\ntelephone: {}\n\n'.format(self.email, self.telephone)
        s3 = 'vat. number: {}\nreg. number: {}\n\n'.format(self.vat_number, self.reg_number)
        s4 = 'bank {}\niban: {}bic: {}\n'.format(self.bank, self.iban, self.bic)
        return s1 + s2 + s3 + s4

    @classmethod
    def create_me(cls, general_data):
        me = cls()
        me.name = general_data['my_name']
        me.address = general_data['my_address']
        me.post = general_data['my_post']
        me.country = general_data['my_country']

        me.email = general_data['my_email']
        me.telephone = general_data['my_telephone']

        me.vat_number = general_data['my_vat_number']
        me.reg_number = general_data['my_reg_number']

        me.bank = general_data['my_bank']
        me.iban = general_data['my_iban']
        me.bic = general_data['my_bic']

        return me


class Service:

    def __init__(self):
        self.name_of_service = ''
        self.units = ''
        self.price_per_unit = ''

    def __str__(self):
        s = 'Name of service: {}\n'.format(self.name_of_service)
        s += 'Units: {}\n'.format(self.units)
        s += 'Price per unit: {}\n'.format(self.price_per_unit)
        return s

    def get_value(self):
        units = int(self.units)
        price_per_unit = float(self.price_per_unit)
        return units * price_per_unit

    @classmethod
    def create_service(cls, data):
        service = cls()
        service.name_of_service = data['name']
        service.units = data['units']
        service.price_per_unit = data['price per unit']
        return service


class InvoiceData:

    def __init__(self, general_data, month_data):
        self.me = Me.create_me(general_data)
        self.customers = []

        i = 1
        while True:
            token = 'customer_' + str(i)
            if token in general_data:
                customer = Customer.create_customer(general_data, i)
                self.customers.append(customer)
                i += 1
            else:
                break
        self.customer_number = None
        self.set_customer_number(month_data['customer'])

        self.invoice_number = month_data['invoice_number']
        self.invoice_date = month_data['date']
        self.date_of_service = month_data['date_of_service']
        self.payment_due = month_data['payment_due']
        self.payment_reference = month_data['payment_reference']

        self.services = []
        self.set_services(month_data['services'])

    def set_services(self, services_data):
        for data in services_data:
            service = Service.create_service(data)
            self.services.append(service)

    def set_customer_number(self, costumer_number_str):
        n = int(costumer_number_str) - 1
        if not (0 <= n < len(self.customers)):
            raise ValueError('The customer number ({}) is not valid.'.format(n))
        self.customer_number = n

    def get_customer(self):
        return self.customers[self.customer_number]

    def get_value(self):
        return sum(service.get_value() for service in self.services)

    def __str__(self):
        s = 'Invoice data:\n' + str(self.me) + '\n'
        for customer in self.customers:
            s += str(customer) + '\n'
        s += 'Customer number: {}\n'.format(self.customer_number)
        s += 'Invoice number: {}\n'.format(self.invoice_number)
        s += 'Invoice date: {}\n'.format(self.invoice_date)
        s += 'Date of service: {}\n'.format(self.date_of_service)
        s += 'Payment due: {}\n'.format(self.payment_due)
        s += 'Payment reference: {}\n'.format(self.payment_reference)
        return s


def get_general_invoice_data():
    sheet_id = get_invoice_spreadsheet_id()
    tab = 'main'
    value_range = '!A2:B40'

    raw_value = get_raw_data_from_google_sheets(sheet_id, tab, value_range)

    general_data = {}
    for line in raw_value:
        if len(line) == 2:
            key = line[0].lower().strip()
            general_data[key] = line[1].strip()

    return general_data


def get_month_invoice_data(month):
    sheet_id = get_invoice_spreadsheet_id()
    tab = month_to_string(month)
    value_range = '!A3:B40'

    raw_value = get_raw_data_from_google_sheets(sheet_id, tab, value_range)

    month_data = {}
    services = []
    is_service = False
    for line in raw_value:
        if is_service:
            if len(line) == 1 and 'service' in line[0].lower():
                services.append({})
            elif len(line) == 2:
                key = line[0].lower()
                services[-1][key] = line[1]
        else:
            if len(line) == 1 and 'service' in line[0].lower():
                services.append({})
                is_service = True
            elif len(line) == 2:
                key = line[0].lower()
                month_data[key] = line[1]

    new_services = []
    for service in services:
        if 'hours' in service:
            hours = service['hours']
            name = service['name']
            name = name + '\n(per hour, ' + hours + ' hours)'
            units = hours
            price_per_unit = service['price per hour']
            new_services.append({'name': name, 'units': units, 'price per unit': price_per_unit})
        elif 'amount' in service:
            name = service['name']
            units = '1'
            price_per_unit = service['amount']
            new_services.append({'name': name, 'units': units, 'price per unit': price_per_unit})

    month_data['services'] = new_services
    return month_data


def get_invoice_data(month):
    general_data = get_general_invoice_data()
    month_data = get_month_invoice_data(month)
    invoice_data = InvoiceData(general_data, month_data)
    return invoice_data

