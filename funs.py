from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from create_db import IBMStock1, GOOGLStock1, MSFTStock1
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


def add_record(date, row: list, symbol: str):
    try:
        engine = create_engine(db_path)
        SessionClass = sessionmaker(bind=engine)
        db_session = SessionClass()
        if symbol == "IBM" or symbol == "ibm":
            new_row = IBMStock1()
        elif symbol == "GOOGL":
            new_row = GOOGLStock1()
        elif symbol == "MSFT":
            new_row = MSFTStock1()

        new_row.date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        new_row.open = row[0]
        new_row.high = row[1]
        new_row.low = row[2]
        new_row.close = row[3]
        new_row.volume = row[4]
        db_session.add(new_row)
        db_session.commit()

    except Exception as e:
        print(f"Error with add row {symbol} : {e}")

    def create_cursor():
        conn = create_engine(db_path).connect()
        return conn

    def delete_from_table(name_table):
        try:
            last_row = list(
                create_engine(DB_URL).connect().execute(f"DELETE FROM {name_table}")
            )
            return "succes delete"
        except:
            return "Error"

    def add_row_predict(row: list, symbol: str):
        try:
            db_session = create_session()
            if symbol == "ibm":
                new_row = ibm_predict()

            elif symbol == "microsoft":
                new_row = microsoft_predict()

            elif symbol == "apple":
                new_row = apple_predict()

            new_row.date = row[0]
            new_row.open = row[1]
            new_row.high = row[2]
            new_row.low = row[3]
            new_row.close = row[4]
            db_session.add(new_row)
            db_session.commit()
        except Exception as e:
            print(f"Error with add row {symbol} : {e}")
