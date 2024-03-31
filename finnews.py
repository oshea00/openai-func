import os
from dotenv import load_dotenv
load_dotenv()
import requests
tickers = "msft,ms,nvda"
keywords = ""
limit = 50
daterange = "thisweek" # today, yesterday, thisweek, thismonth, or yyyy-MM-dd, or yyyy-MM-dd,yyyy-MM-dd
finnews_api_key = os.getenv("APILAYER_API_KEY")
url = f"https://api.apilayer.com/financelayer/news?tickers={tickers}&limit={limit}&offset=10&keywords={keywords}&fallback=off&date={daterange}"

payload = {}
headers= {
  "apikey": f"{finnews_api_key}"
}

response = requests.request("GET", url, headers=headers, data = payload)

status_code = response.status_code
result = response.text
print(result)