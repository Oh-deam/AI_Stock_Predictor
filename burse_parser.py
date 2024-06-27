from creds import API_KEY
from datetime import datetime, timedelta
from funs import time_period
import requests
import json


print(time_period())


# for i in range(13):


# def get_data(function:str):
#     url = "https://www.alphavantage.co/query?"

#     # function = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={API_KEY}"

#     r = requests.get(url + function)

#     data = r.json()


#     with open("data.json", "w") as file:
#         json.dump(data, file, ensure_ascii=True, indent=4)


# def time_period(start:str, finish:str) -> list :
#     # применить функцию для парсинга по списку дат (get_data)
# print(start)
