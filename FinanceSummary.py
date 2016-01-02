import json
import argparse
from pymongo import MongoClient
from pprint import pprint

try:
  # py3
  from urllib.request import Request, urlopen
  from urllib.parse import urlencode
except ImportError:
  # py2
  from urllib2 import Request, urlopen
  from urllib import urlencode


def getKeys(symbol,args):
    doc = getDoc(symbol)
    if len(argsinfo) > 0 and argsinfo[0] in doc['data'].keys():
        data = recurseItem(doc['data'],argsinfo,0)
        if isinstance(data,dict()):
            return data.keys()
        else:
            return {}
    else:
        return doc['data'].keys()

def recurseItem(doc,argsinfo,n):
    if len(argsinfo) > n+1 and argsinfo[n+1] in doc[argsinfo[n]].keys():
        return recurseItem(doc[argsinfo[n]],argsinfo,n+1)
    else:
        return doc[argsinfo[n]]

def main_example():
  parser = argparse.ArgumentParser()
  parser.add_argument("symbol")
  parser.add_argument("info",nargs='*')
  # add arg for listing all
  args = parser.parse_args()
  pprintItem(args.symbol,args.info)

def getDoc(symbol):
  client = MongoClient()
  db = client.finance
  coll = db['summary']
  return coll.find({'symbol': symbol})[0]

def getItem(symbol,argsinfo):
  doc = getDoc(symbol)
  if len(argsinfo) > 0 and argsinfo[0] in doc['data'].keys():
      return (recurseItem(doc['data'],argsinfo,0))
  else:
      return (doc['data'])

def pprintItem(symbol,argsinfo):
  pprint(getItem(symbol,argsinfo))

def _request(symbol):
  url = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/%s' % (symbol)
  url = url + '?formatted=true&crumb=PUgrfiU145z&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2Cprice%2CsummaryDetail%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=beta.finance.yahoo.com'
  req = Request(url)
  resp = urlopen(req)
  content = resp.read()
  jcontent = json.loads(content)
  result = json.loads('{}')
  if 'quoteSummary' in jcontent.keys():
    if not jcontent['quoteSummary']['error']:
      jresult = jcontent['quoteSummary']['result'][0]
      result = json.loads('{"symbol": "%s", "data": %s}' % (symbol, json.dumps(jresult)))
    else:
      pprint(jcontent['quoteSummary']['error'])
  return result

def refreshDb(symbol):
  result = _request(symbol)
  # pprint(result)
  client = MongoClient()
  db = client.finance
  coll = db['summary']
  if 'symbol' in result.keys():
     print("Inserting symbol=%s" % symbol)
     coll.replace_one({'symbol': symbol},result,upsert=True)
  else:
     print("Error getting symbol=%s" % symbol)


