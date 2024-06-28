from datetime import datetime, timedelta
from funs import time_period
from creds import API_KEY
import requests
import json
import os


url = "https://www.alphavantage.co/query?"


symbols = ["IBM", "GOOGL", "TSCDY"] GOOGL
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


for symbol in symbols:
    file_name = f"{symbol}_data.json"

    # Чтение существующих данных из файла, если файл не пустой
    existing_data = {}
    try:
        with open(file_name, "r") as f:
            file_content = f.read().strip()
            if file_content:
                existing_data = json.loads(file_content)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = {}

    for month in streack:
        # Формирование параметров запроса
        function = f"function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&month={month}&outputsize={outputsize}&apikey={API_KEY}"
        response = requests.get(url + function)
        new_data = response.json()

        if "Time Series (5min)" in new_data:
            if "Time Series (5min)" not in existing_data:
                existing_data["Time Series (5min)"] = {}
            existing_data["Time Series (5min)"].update(new_data["Time Series (5min)"])

    # Запись обновленных данных в файл
    with open(file_name, "w") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

print("Data fetching completed.")
