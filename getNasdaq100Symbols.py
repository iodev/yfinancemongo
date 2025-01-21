from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup
import csv
import json
# URL of the webpage
#url = "https://www.nasdaq.com/solutions/global-indexes/nasdaq-100/companies"
url = "https://api.nasdaq.com/api/quote/list-type/NASDAQ100?limit=20&sortOrder=ASC&queryString=sectorInfo"
#also = "https://api.nasdaq.com/api/quote/list-type/NASDAQ100?limit=20&sortOrder=ASC&queryString=marketCap"
#also = "https://api.nasdaq.com/api/quote/list-type/NASDAQ100?limit=20&sortOrder=ASC&queryString=percentageChange"

# Send a GET request to the webpage
# response = requests.get(url,timeout=10, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0'})

# response = requests.get(also, timeout=10, headers={    
#     "accept": "*/*",
#     "accept-language": "en-US,en;q=0.9",
#     "cache-control": "no-cache",
#     "pragma": "no-cache",
#     "priority": "u=1, i",
#     "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Microsoft Edge\";v=\"132\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\"",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-site",
#     "referrer": "https://www.nasdaq.com/"
#     })
req = Request(url, headers={    
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Microsoft Edge\";v=\"132\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "referrer": "https://www.nasdaq.com/"
    })
resp = urlopen(req, timeout=10)
content = resp.read()
jcontent = json.loads(content)
result = json.loads('{}')
if 'data' in jcontent.keys():
    if 'rows' in jcontent['data'].keys():
        rows = jcontent['data']['rows']
        # Prepare a list to store the data
        data = []
        for row in rows:
            data.append([row['symbol'],row['companyName'],row['marketCap'],row['percentageChange'],row['lastSalePrice']])
        # Save the data to a CSV file
        with open("nasdaq100_companies.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(data)
