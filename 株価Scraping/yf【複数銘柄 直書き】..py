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
	l = []
	l.append("8411")
	l.append("8306")
	l.append("3103")
	l.append("6803")
	l.append("6502")
	l.append("4689")
	l.append("8107")
	l.append("8303")
	l.append("9101")
	l.append("8604")
	l.append("6501")
	l.append("9972")
	l.append("6753")
	l.append("7201")
	l.append("6752")
	l.append("9501")
	l.append("7011")
	l.append("7647")
	l.append("7211")
	l.append("9104")

	for el in l:
	   symbol,stockprice = get_stockprice(el)
	   print(symbol,stockprice)