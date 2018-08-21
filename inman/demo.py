from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Table, SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import datetime
import calendar

from inman.getData import get_working_hours
from inman.months import Month, month_to_long_name
from inman.config import get_invoice_spreadsheet_id

styleSheet = getSampleStyleSheet()

breaks = 30


def get_day_name(date):
    data = date.split(".")
    day = int(data[0])
    month = int(data[1])
    year = 2018
    d = datetime.date(year, month, day)
    return calendar.day_name[d.weekday()]


def parse_time(time_str):
    data = time_str.split(":")
    hours = int(data[0])
    minutes = int(data[1])
    return hours, minutes


def format_time(hours, minutes):
    minutes_str = "00" if minutes == 0 else str(minutes)
    return str(hours) + ":" + minutes_str


def convert_to_minutes(hours, minutes):
    return 60 * hours + minutes


def minutes_to_time(minutes):

    h = minutes // 60
    m = minutes % 60

    return h, m


def compute_time(start_hours, start_minutes, end_hours, end_minutes, breaks):
    s_minutes = convert_to_minutes(start_hours, start_minutes)
    e_minutes = convert_to_minutes(end_hours, end_minutes)

    diff = e_minutes - s_minutes - breaks
    return minutes_to_time(diff)


def get_time_data(d):
    data = [["Date", "", "Start", "", "End", "Lunch Break", "Total"]]
    data.append([])
    style = []
    total_minutes = 0
    for i, entry in enumerate(d):
        entry_data = []

        date = entry["date"]
        entry_data.append(date)

        day_name = get_day_name(date)
        entry_data.append(day_name)

        if "start" in entry:
            start_h, start_min = parse_time(entry["start"])
            entry_data.append(format_time(start_h, start_min))

            if "end" not in entry:
                raise ValueError("End without start")

            entry_data.append("--")
            end_h, end_min = parse_time(entry["end"])
            entry_data.append(format_time(end_h, end_min))

            entry_data.append("-0:30")

            hours, minutes = compute_time(start_h, start_min, end_h, end_min, breaks)
            total_minutes += convert_to_minutes(hours, minutes)
            entry_data.append(format_time(hours, minutes))

        if "note" in entry:
            entry_data.append(entry["note"])
            style.append(("SPAN", (2, i + 2), (-1, i + 2)))
        data.append(entry_data)

    hours, minutes = minutes_to_time(total_minutes)
    data.append([])   # empty line
    data.append(['Total', '', '', '', '', '', format_time(hours, minutes)])
    return data, style


def get_working_hours_table(month):
    raw_data = get_working_hours(month)
    data, style = get_time_data(raw_data)
    style.append(('FONTSIZE', (0, 0), (-1, -1), 11))
    style.append(('ALIGN', (0, 0), (0, -1), 'RIGHT'))
    style.append(('TOPPADDING', (0, 0), (-1, 0), 17))
    column_widths = [2 * cm, 3.5 * cm, 1 * cm, 0.5 * cm, 2.5 * cm, 3.5 * cm, 2 * cm]
    return Table(data, colWidths=column_widths, style=style)


def create_working_hours_sheet(month, pdf_path):

    doc = SimpleDocTemplate(pdf_path, page=A4, title='Working hours')

    elements = []

    text = 'Working hours ' + month_to_long_name(month) + '\n'
    heading_style = styleSheet["Title"]
    p = Paragraph(text, heading_style)
    elements.append(p)

    table = get_working_hours_table(month)
    elements.append(table)

    doc.build(elements)


def main():
    path = r"C:\Users\Jaka\workspace\generatePDF\demo.pdf"
    create_working_hours_sheet(Month.Jul, path)
    print('Created a new file {}'.format(path))


if __name__ == "__main__":
    main()
