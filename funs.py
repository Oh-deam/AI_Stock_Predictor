from datetime import datetime, timedelta
import json


def time_period() -> list:
    year = datetime.now().year
    month = datetime.now().month

    finish = f"{year}-{str(month).zfill(2)}"
    start = f"{year-1}-{str(month).zfill(2)}"

    finish_dt = datetime.strptime(f"{year}-{str(month).zfill(2)}", "%Y-%m")
    start_dt = datetime.strptime(f"{year-1}-{str(month).zfill(2)}", "%Y-%m")

    dates = []
    first_dt = start_dt
    while first_dt <= finish_dt:
        dates.append(first_dt.strftime("%Y-%m"))
        next_month = first_dt.month + 1
        next_year = first_dt.year
        if next_month > 12:
            next_month = 1
            next_year += 1
        first_dt = first_dt.replace(year=next_year, month=next_month)
    return dates
