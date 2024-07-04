import requests

import datetime as dt

from airflow.models import DAG
from airflow.operators.python import PythonOperator


from funs import time_period, add_record, is_record

from cred_airflow import API_KEY
from settings import db_names, db_to_stock


def get_data(symbol: str, date: str) -> bool:

    url = "https://www.alphavantage.co/query?"

    bases = ["IBMStock1", "GOOGLStock1", "TSCDYStock1"]
    symbols = ["IBM", "GOOGL", "MSFT"]
    interval = "5min"
    outputsize = "full"

    streack = time_period()

    for i in range(len(symbols)):
        for month in streack:
            function = f"function=TIME_SERIES_INTRADAY&symbol={symbols[i]}&interval={interval}&month={month}&outputsize={outputsize}&apikey={API_KEY}"
            response = requests.get(url + function)
            data = response.json()

            if "Time Series (5min)" in data:
                for datetime_str, value in data["Time Series (5min)"].items():
                    # print(type(datetime_str))
                    # date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                    dt = list(value.values())
                    add_record(datetime_str, dt, symbols[i])


def start():

    symbols = []

    for name in db_names:
        if not is_record(name):
            symbols.append(db_to_stock[name])

    if len(symbols) != 0:
        print(f"empty databases: {symbols}")
        dates = time_period()
        for symbol in symbols:
            for date in dates:
                if not get_data(symbol, date):
                    break
                else:
                    print(f"{symbol} for {date} was handled")


args = {
    "owner": "airflow",  # Информация о владельце DAG
    "start_date": dt.datetime.now(),  # Время начала выполнения пайплайна
    "retries": 1,  # Количество повторений в случае неудач
    "retry_delay": dt.timedelta(days=1),  # Пауза между повторами
    "depends_on_past": False,  # Зависимость от успешного окончания предыдущего запуска
}

with DAG(dag_id="dag_fill_db", schedule_interval="@daily", default_args=args) as dag:

    fill_db = PythonOperator(task_id="fill_db", python_callable=start, dag=dag)

    fill_db
