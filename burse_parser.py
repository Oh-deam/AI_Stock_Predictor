from creds import API_KEY
import requests
import json


url = "https.alphavantage.co/query?"
function = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={API_KEY}"

r = requests.get(function)

data = r.json()


with open("data.json", "w") as file:
    json.dump(data, file, ensure_ascii=True, indent=4)
