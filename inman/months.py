from enum import Enum


class Month(Enum):
    Jan = 'jan'
    Feb = 'feb'
    Mar = 'mar'
    Apr = 'apr'
    May = 'may'
    Jun = 'jun'
    Jul = 'jul'
    Aug = 'aug'
    Sep = 'sep'
    Oct = 'oct'
    Nov = 'nov'
    Dec = 'dec'


def month_to_string(month):
    return month.value


def month_to_long_name(month):
    if month == Month.Jan:
        return 'January'
    elif month == Month.Feb:
        return 'February'
    elif month == Month.Mar:
        return 'March'
    elif month == Month.Apr:
        return 'April'
    elif month == Month.May:
        return 'May'
    elif month == Month.Jun:
        return 'June'
    elif month == Month.Jul:
        return 'July'
    elif month == Month.Aug:
        return 'August'
    elif month == Month.Sep:
        return 'September'
    elif month == Month.Oct:
        return 'October'
    elif month == Month.Nov:
        return 'November'
    elif month == Month.Dec:
        return 'December'
    else:
        raise ValueError('Undefined month: {}'.format(month))
