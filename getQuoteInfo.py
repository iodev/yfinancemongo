#!/usr/bin/python
import argparse
from FinanceSummary import pprintItem
def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("symbol")
  parser.add_argument("info",nargs='*')
  # add arg for listing all
  args = parser.parse_args()
  pprintItem(args.symbol,args.info)

if __name__ == "__main__":
    main()
