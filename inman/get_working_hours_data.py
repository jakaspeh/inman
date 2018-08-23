from inman.config import get_working_hours_spreadsheet_id
from inman.months import month_to_string
from inman.google_sheet import get_raw_data_from_google_sheets


def check_date(raw_day):
    n = len(raw_day)
    if n == 0:
        raise ValueError('A day has no date.')
    raw_date = raw_day[0]
    lst = raw_date.split('.')
    day = int(lst[0])
    month = int(lst[1])
    if not (1 <= day <= 31 and 1 <= month <= 12):
        raise ValueError('A day has wrong date: {0}.{1}'.format(day, month))
    return raw_date


def is_non_working_day(raw_day):
    n = len(raw_day)
    if n == 2 or n == 3:
        return True
    elif n == 4:
        return False
    else:
        raise ValueError('A day has wrong format {}'.format(raw_day))


def day_has_note(raw_day):
    return len(raw_day) == 3


def get_note(raw_day):
    return raw_day[2]


def check_time(time):
    lst = time.split(":")
    if len(lst) != 2:
        raise ValueError('Time has wrong format {}'.format(time))

    hour = lst[0]
    if not (0 <= int(hour) < 24):
        raise ValueError('Hour is not between 0 and 24: {}'.format(hour))

    minute = lst[1]
    if not (0 <= int(minute) < 60):
        raise ValueError('Minute is not between 0 and 60: {}'.format(minute))


def get_working_time(raw_day):
    start = raw_day[2]
    check_time(start)
    end = raw_day[3]
    check_time(end)
    return start, end


def parse_day(raw_day):

    date = check_date(raw_day)
    day_data = {'date': date}

    if is_non_working_day(raw_day):
        if day_has_note(raw_day):
            note = get_note(raw_day)
            day_data['note'] = note
    else:
        start, end = get_working_time(raw_day)
        day_data['start'] = start
        day_data['end'] = end

    return day_data


def get_working_hours(month):

    spreadsheet_id = get_working_hours_spreadsheet_id()
    tab = month_to_string(month)
    value_range = '!A3:D40'

    values = get_raw_data_from_google_sheets(spreadsheet_id, tab, value_range)

    working_hours = []

    if not values:
        raise ValueError('No data found.')
    else:
        for row in values:
            working_hours.append(parse_day(row))

    return working_hours
