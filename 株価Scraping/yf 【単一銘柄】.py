import requests
from bs4 import BeautifulSoup

def get_stockprice(code):
    base_url = "http://stocks.finance.yahoo.co.jp/stocks/detail/"
    query = {}
    query["code"] = code + ".T"
    ret = requests.get(base_url,params=query)
    soup = BeautifulSoup(ret.content,"lxml")
    stocktable =  soup.find('table', {'class':'stocksTable'})
    symbol =  stocktable.findAll('th', {'class':'symbol'})[0].text
    stockprice = stocktable.findAll('td', {'class':'stoksPrice'})[1].text
    return symbol,stockprice
if __name__ == "__main__":
    symbol,stockprice = get_stockprice("6758")
    print (symbol,stockprice)