from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from create_db import (
    IBMStock1,
    GOOGLStock1,
    MSFTStock1,
    IBMStock2,
    GOOGLStock2,
    MSFTStock2,
)
from settings import PREDICT_TIME, N_DAYS_BEFORE_FOR_MODEL
from cred_airflow import DB_URL
import pandas as pd
import numpy as np
import joblib
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


def create_dbsession():
    engine = create_engine(DB_URL)

    SessionClass = sessionmaker(bind=engine)
    return SessionClass()


def add_db(file_name):
    with open(file, "r") as file:
        data = json.load(file)

    records = []


def add_record(date, row: list, symbol: str):
    try:
        engine = create_engine(DB_URL)
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
    conn = create_engine(DB_URL).connect()
    return conn


def create_columns() -> list:
    time_before_for_predict = 1000
    new_columns = ["date"]
    columns = ["open", "high", "low", "close"]
    time_before_for_predict = 3
    for i in range(time_before_for_predict, 0, -1):
        for col in columns:
            new_columns.append(col + "_" + str(i) + "b")
    return new_columns


def pred(row, symbol, target):
    model = joblib.load(f"/opt/airflow/dags/models/model_{symbol}_{target}.pkl")
    pred = model.predict(np.array(row).reshape(1, -1))
    return pred[0]


def start_predict(row, symbol):
    results = []

    for i in range(PREDICT_TIME):

        row.append(pred(row, symbol, "open"))

        row.append(pred(row, symbol, "high"))

        row.append(pred(row, symbol, "low"))

        row.append(pred(row, symbol, "close"))

        results.append(row[-4:])

        row = row[4:]

    return results


def convert_to_one_row(row: list) -> list:

    result_row = []

    for i in range(N_DAYS_BEFORE_FOR_MODEL - 1, -1, -1):
        for j in range(1, len(row[i])):
            result_row.append(row[i][j])
    return result_row


def make_date_range(start: str):
    start_date = datetime.strptime(str(start), "%Y-%m-%d %H:%M:%S")
    date_range = []

    date_now = start_date
    for i in range(PREDICT_TIME):
        date_now += timedelta(minutes=5)
        date_range.append(date_now)
    return date_range


def get_predict_data(symbol):
    last_row = list(
        create_cursor().execute(
            f"SELECT date,open,high,low,close FROM public.{symbol} order by date DESC limit {PREDICT_TIME}"
        )
    )

    row = convert_to_one_row(last_row)

    dates = np.array(make_date_range(last_row[0][0]))

    result_predicts = start_predict(row, symbol)
    df = pd.DataFrame(result_predicts)
    df.insert(0, "date", dates)
    # print(df.head(10))
    df.columns = ["date", "open", "high", "low", "close"]

    return df


def add_row_predict(row: list, symbol: str):

    try:
        db_session = create_dbsession()
        if symbol == "ibm_stock":
            new_row = IBMStock2()
            print("ibm")

        elif symbol == "msft_stock":
            new_row = MSFTStock2()
            print("msft")

        elif symbol == "googl_stock":
            new_row = GOOGLStock2()
            print("googl")

        print(row[0])
        new_row.date = row[0]
        new_row.open = row[1]
        new_row.high = row[2]
        new_row.low = row[3]
        new_row.close = row[4]
        db_session.add(new_row)
        db_session.commit()
    except Exception as e:
        print(f"Error with add row {symbol} : {e}")


def get_last_date(symbol) -> str:
    last_date = list(
        create_cursor().execute(
            f"SELECT date FROM public.{symbol} order by date DESC limit 1"
        )
    )[0][0]

    return str(last_date)


def delete_from_table(name_table):
    try:
        last_row = list(
            create_engine(DB_URL).connect().execute(f"DELETE FROM {name_table}")
        )
        return "succes delete"
    except:
        return "Error"


# def get_last_date(symbol):

#     db_session = create_dbsession()
#     if symbol == "ibm":
#         last_date = db_session.query(IBMStock1).order_by(desc(IBMStock1.date)).first().date
#     elif symbol == "apple":
#         last_date = db_session.query(GOOGLStock1).order_by(desc(GOOGLStock1.date)).first().date
#     else:
#         last_date = (
#             db_session.query(MSFTStock1).order_by(desc(MSFTStock1.date)).first().date
#         )
#     return last_date


def is_record(symbol: str) -> bool:

    count = list(
        create_cursor().execute(f"SELECT count(date) FROM public.{symbol} limit 1")
    )[0][0]

    print(count)
    if count == 0:
        return False
    else:
        return True
