#!/usr/bin/python
import argparse
from pymongo import MongoClient
from FinanceSummary import refreshDb

def main():

  parser = argparse.ArgumentParser()
  parser.add_argument("symbol")
  args = parser.parse_args()
  refreshDb(args.symbol)


if __name__ == "__main__":
    main()
