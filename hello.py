import csv
import json
import argparse
from pprint import pprint
from pymongo import MongoClient
import boto3
from botocore.exceptions import ClientError

from urllib.request import Request, urlopen
from urllib.parse import urlencode

import yfinance as yf
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter
class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
   pass

session = CachedLimiterSession(
   limiter=Limiter(RequestRate(2, Duration.SECOND*5)),  # max 2 requests per 5 seconds
   bucket_class=MemoryQueueBucket,
   backend=SQLiteCache("yfinance.cache"),
)
dynamodb = boto3.resource(
    'dynamodb'
)
intervals = ['1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo']
periods = ['1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max']
def main():
    symbols = []
    with open("NasdaqSymbols.csv", 'r') as syms:
        rdr = csv.reader(syms)
        # read the rows, both columns, first, second column may have quotes
        for row in rdr:
            if row[0] == "Symbol":
                continue
            symbol = row[0]
            cname = row[1].replace('"', '')
            symbols.append(symbol)
    for symbol in symbols:
        for i in intervals:
            try:
                # get the data from yfinance
                doc = yf.Ticker(symbol, session=session)

                # doc.get_financials(as_dict=True)
                # doc.get_balance_sheet(as_dict=True)
                # doc.get_cashflow(as_dict=True)
                # doc.get_earnings(as_dict=True)
                # doc.get_splits(as_dict=True)
                
                jdoc = doc.history(period="1mo", interval=i).to_json()
                print(f"got jdoc for {symbol}: {jdoc}")

                # write all to a file 
                #doc.to_pickle(f"{symbol}_{i}.pkl")
                #print("Added %s to pickle" % symbol)

                # write the data to dynamodb
                table = dynamodb.Table('stock-price')
                table.put_item(Item={'symbol': symbol, 'densityId': i, 'data': jdoc})
                print("Added %s to dynamodb" % symbol)

                # convert the data to json
                # doc.to_json(f"{symbol}_{i}.json")
                # print("Added %s to json" % symbol)

                # write the data to s3
                # s3 = boto3.client('s3') #s3://stocktrade-versioned/symboldata/
                # s3.put_object(Bucket='stocktrade-versioned/symboldata', Key=f"{symbol}_{i}.json", Body=json.dumps(doc))
            except Exception as e:
                print(e)


if __name__ == "__main__":
    main()
