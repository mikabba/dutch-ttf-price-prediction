import calendar
from datetime import datetime, timedelta

def decrement_month(start_time, end_time):
    # Converte le stringhe in oggetti datetime
    start_datetime = datetime.strptime(start_time, "%Y%m%d%H%M")
    end_datetime = datetime.strptime(end_time, "%Y%m%d%H%M")

    month = start_datetime.month - 1
    if month == 0:
        month = 12
        year = start_datetime.year - 1
    else:
        year = start_datetime.year

    days_in_prev_month = calendar.monthrange(year, month)[1]
    start_datetime -= timedelta(days=days_in_prev_month)

    month = end_datetime.month - 1
    if month == 0:
        month = 12
        year = end_datetime.year - 1
    else:
        year = end_datetime.year

    days_in_prev_month = calendar.monthrange(year, month)[1]
    end_datetime -= timedelta(days=days_in_prev_month)

    # Formatta le date come stringhe
    start_time = start_datetime.strftime("%Y%m%d%H%M")
    end_time = end_datetime.strftime("%Y%m%d%H%M")

    return start_time, end_time

def decrement_days(start_time, end_time, days=5):
    # Convert strings to datetime objects
    start_datetime = datetime.strptime(start_time, "%Y%m%d%H%M")
    end_datetime = datetime.strptime(end_time, "%Y%m%d%H%M")

    # Decrement start and end time by specified number of days
    start_datetime -= timedelta(days=days)
    end_datetime -= timedelta(days=days)

    # Format dates as strings
    start_time = start_datetime.strftime("%Y%m%d%H%M")
    end_time = end_datetime.strftime("%Y%m%d%H%M")

    return start_time, end_time

start_time = "202301040000"
end_time = "202302030000"
start_time, end_time = decrement_days(start_time, end_time)

print("Start time:", start_time)
print("End time:", end_time)