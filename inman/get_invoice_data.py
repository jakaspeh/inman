from inman.google_sheet import get_raw_data_from_google_sheets
from inman.config import get_invoice_spreadsheet_id
from inman.months import month_to_string


def get_general_invoice_data():
    sheet_id = get_invoice_spreadsheet_id()
    tab = 'main'
    value_range = '!A2:B20'

    raw_value = get_raw_data_from_google_sheets(sheet_id, tab, value_range)

    general_data = {}
    for line in raw_value:
        if len(line) == 2:
            key = line[0].lower()
            general_data[key] = line[1]

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
            name = name + ' (per hour, ' + hours + ' hours)'
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
    return {**general_data, **month_data}

