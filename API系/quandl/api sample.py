import datetime
import quandl
import pandas as pd

# 各種設定
## 取得したい日付レンジの指定
start = datetime.datetime(2007, 1, 1)
end = datetime.datetime(2019, 1, 19)

# 取得したい会社のティックシンボルを記載します。
## 例えばの武田薬品工業の場合　TSE/4502 となります。
## https://www.quandl.com/data/TSE/4502-Takeda-Pharmaceutical-Co-Ltd-4502
company_id = 'TSE/4502'

# APIキーの設定
quandl.ApiConfig.api_key = '●'

# データ取得
df = quandl.get(company_id ,start_date=start,end_date=end)

print(df)


df.to_csv('api test_hino.csv')
