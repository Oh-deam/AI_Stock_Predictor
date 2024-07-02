from funs import time_period, add_record
from creds import API_KEY
import requests


url = "https://www.alphavantage.co/query?"


bases = ["IBMStock1", "GOOGLStock1", "TSCDYStock1"]
symbols = ["IBM", "GOOGL", "MSFT"]
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


print("Data fetching completed.")
