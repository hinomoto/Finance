import requests
from bs4 import BeautifulSoup

from openpyxl import load_workbook

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

   filename = '銘柄コード.xlsx'

wb = load_workbook(filename, read_only=True)
print(f'{filename} のワークシート情報を読み込みます')

ws0 = wb.worksheets[0]        #←最初のワークシートを取得する
print(f'{ws0.title} のセルを1行ずつ表示します')
for row in ws0:        #←行を読み込む
    values = [str(column.value) for column in row]        #←列を読み込む
    print(values)
    print(type(values))
    mojiretsu = ','.join(values)
    symbol,stockprice = get_stockprice(mojiretsu)
    print(symbol,stockprice)
    
   #mojiretsu = ','.join(values)    #list を文字列に変換
   #print(mojiretsu)
   #print(type(mojiretsu))

#     for el in values:
#	     symbol,stockprice = get_stockprice(el)
#	     print(symbol,stockprice)