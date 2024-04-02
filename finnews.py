import os
from dotenv import load_dotenv
load_dotenv()
import requests
from termcolor import colored  
import json

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

if status_code != 200:
    print(f"Error: Unable to fetch news data")
    print(f"Status code: {status_code}")
    exit()

news = json.loads(result)
ARTICLE_TITLE_COLOR = "yellow"
ARTICLE_DESCRIPTION_COLOR = "green"
ARTICLE_URL_COLOR = "blue"
ARTICLE_ATTR_COLOR = "grey"

if news['data']:
    for article in news['data']:
        print(colored(article['title'], ARTICLE_TITLE_COLOR))
        print(colored(article['description'], ARTICLE_DESCRIPTION_COLOR))
        print(colored(article['url'], ARTICLE_URL_COLOR))
        print(colored(f"Published: {article['published_at']}", ARTICLE_ATTR_COLOR))
        print(colored(f"Source: {article['source']}", ARTICLE_ATTR_COLOR))
        print(colored(f"Tickers: {article['tickers']}", ARTICLE_ATTR_COLOR))
        print(colored(f"Tags: {article['tags']}", ARTICLE_ATTR_COLOR))
        print()
