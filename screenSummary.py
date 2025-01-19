#!/usr/bin/python
import FinanceSummary

def evalItem(doc):
     off52wkBy50pct = doc['defaultKeyStatistics']['52WeekChange']['raw'] < -0.50
     priceLtBook = doc['financialData']['currentPrice']['raw'] < doc['defaultKeyStatistics']['bookValue']['raw']
     peForwBackRatio = doc['summaryDetail']['forwardPE']['raw'] > doc['summaryDetail']['trailingPE']['raw']
     peWasLt10 = doc['summaryDetail']['trailingPE']['raw'] < 10.00
     excludeOil = doc['summaryProfile']['sector'] != "Basic Materials"
     return (off52wkBy50pct and priceLtBook and peForwBackRatio and peWasLt10 and excludeOil)

def main():
    # TODO: add the monthly download of the Symbols.csv file from https://www.cboe.com/us/options/symboldir/?download=csv
    # load the symbols and send them thru getItem
    with open('Symbols.csv','r') as f:
        # data is quoted strings, comma-delimited, 4 columns
        for line in iter(f.readline, ''):
            # if line is header, skip
            if line.startswith("Company"): # header = 'Company Name, Stock Symbol, DPM Name, Post/Station'
                continue
            sym = line.split('","')[1]
            sym = sym.rstrip("\n\r\f")
            print(sym)
            try:
                doc = FinanceSummary.getItem(sym,[])
                if evalItem(doc):
                    print("%s\t%s\t%s\t%s\t%s" % (doc['summaryProfile']['sector'],doc['summaryProfile']['industry'],doc['financialData']['currentPrice']['raw'],doc['price']['symbol'],doc['price']['longName']))#,doc['financialData']['debtToEquity']['fmt']))
            except Exception:
                None #print("Bad symbol in database? " + sym)

if __name__ == "__main__":
    main()
