from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from create_db import IBMStock1
from creds import db_path
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


def create_dbsession(db_path=None):
    engine = create_engine(db_path)

    SessionClass = sessionmaker(bind=engine)
    return SessionClass()


def add_db(file_name):
    with open(file, "r") as file:
        data = json.load(file)

    records = []


# # Чтение данных из файла JSON
# with open("IBM_data.json", "r") as file:
#     data = json.load(file)

# # Преобразование данных в объекты SQLAlchemy
# records = []
# for datetime_str, values in data.items():
#     record = IBMStock(
#         datetime=datetime_str,
#         open=values.get("open"),
#         high=values.get("high"),
#         low=values.get("low"),
#         close=values.get("close"),
#         volume=values.get("volume")
#     )
#     records.append(record)

# # Добавление данных в сессию и фиксация
# session.bulk_save_objects(records)
