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
    with open('Symbols.csv','r') as f:
        for line in iter(f.readline, ''):
            sym = line.split("\t")[1]
            sym = sym.rstrip("\n\r\f")
            #print(sym)
            try:
                doc = FinanceSummary.getItem(sym,[])
                if evalItem(doc):
                    print("%s\t%s\t%s\t%s\t%s" % (doc['summaryProfile']['sector'],doc['summaryProfile']['industry'],doc['financialData']['currentPrice']['raw'],doc['price']['symbol'],doc['price']['longName']))#,doc['financialData']['debtToEquity']['fmt']))
            except Exception:
                None #print("Bad symbol in database? " + sym)

if __name__ == "__main__":
    main()
