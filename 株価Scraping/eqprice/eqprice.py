import pandas as pd
import pandas_datareader.data as web
import datetime
import os


# a取得する日の範囲を指定する

#date = datetime.date(2020, 2, 18)
date = datetime.date.today()
#date = str(input('Enter a day 2019, 11, 1'))

#株価結果を入れる空のデータフレームを準備
data_frame = pd.DataFrame()

#1列目をindexとしたい場合”index_col=0’とする

#index_col=None でカラム名を設定。1列目1行目に指定した文字列"CODE"等
df = pd.read_excel('銘柄コード.xlsx',index_col=None)

for i in df.CODE.items():
   
    
    #文字列変換
    i=str(i[1])
    
    
    f = web.DataReader(i+'.t', '●データソース元入力●', date, date)
    
    
    print(f)
    #空のデータフレームに代入
    data_frame=data_frame.append(f)
    
    
data_frame.to_excel('eqprice_result.xlsx')

#改めてデータフレームを構築
file1 = pd.read_excel('eqprice_result.xlsx')
file2 = pd.read_excel('銘柄コード.xlsx')


#横方向に連結
df_concat = pd.concat([file1, file2] ,axis=1)

print(df_concat)
    
df_concat.to_excel('Result.xlsx')


#'eqprice_result.xlsx'ファイルを削除（不要の為）
os.remove('eqprice_result.xlsx')