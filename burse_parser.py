from funs import time_period
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from creds import API_KEY, db_path
import requests
import json
import os


url = "https://www.alphavantage.co/query?"


bases = ["IBMStock1", "GOOGLStock1", "TSCDYStock1"]
symbols = ["IBM", "GOOGL", "TSCDY"]
interval = "5min"
outputsize = "full"

streack = time_period()

# for symbol in symbols:
#     for month in streack:
#         function = f"function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&month={month}&outputsize=full&apikey={API_KEY}"
#         response = requests.get(url + function)
#         data = response.json()
#         with open(f"{symbol}_data.json", "a") as f:
#             json.dump(data, f, ensure_ascii=True, indent=4)

engine = create_engine(db_path)
SessionClass = sessionmaker(bind=engine)
db_session = SessionClass()


for symbol in symbols:
    for model in bases:
        for month in streack:
            function = f"function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&month={month}&outputsize={outputsize}&apikey={API_KEY}"
            response = requests.get(url + function)
            data = response.json()

            if "Time Series (5min)" in data:
                for datetime_str, values in data["Time Series (5min)"].items():
                    record_datetime = datetime.strptime(
                        datetime_str, "%Y-%m-%d %H:%M:%S"
                    )
                    record = model(
                        datetime=record_datetime,
                        open=float(values.get("1. open", 0)),
                        high=float(values.get("2. high", 0)),
                        low=float(values.get("3. low", 0)),
                        close=float(values.get("4. close", 0)),
                        volume=int(values.get("5. volume", 0)),
                    )
                    db_session.add(record)
db_session.commit()


# for symbol in symbols:
#     file_name = f"{symbol}_data.json"

#     # Чтение существующих данных из файла, если файл не пустой
#     existing_data = {}
#     try:
#         with open(file_name, "r") as f:
#             file_content = f.read().strip()
#             if file_content:
#                 existing_data = json.loads(file_content)
#     except (FileNotFoundError, json.JSONDecodeError):
#         existing_data = {}

#     for month in streack:
#         # Формирование параметров запроса
#         function = f"function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&month={month}&outputsize={outputsize}&apikey={API_KEY}"
#         response = requests.get(url + function)
#         new_data = response.json()

#         if "Time Series (5min)" in new_data:
#             if "Time Series (5min)" not in existing_data:
#                 existing_data["Time Series (5min)"] = {}
#             existing_data["Time Series (5min)"].update(new_data["Time Series (5min)"])

#     # Запись обновленных данных в файл
#     with open(file_name, "w") as f:
#         json.dump(existing_data, f, ensure_ascii=False, indent=4)

# print("Data fetching completed.")
