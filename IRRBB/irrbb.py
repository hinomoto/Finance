#https://qiita.com/sawadybomb/items/43c514ee002aafc72f71
#

import datetime
import math
import numpy as np

# 基礎数値を設定(オリックス社債第195回)
maturity_date = datetime.datetime(2028, 11, 8)
base_date = datetime.datetime(2019, 3, 8)
coupon = 0.454
freq = 2  # 利払い回数


zanzon = (maturity_date - base_date).days / 365

# 残存年数から利払い頻度に応じた期間を引いていく
cashflow = []
i = 0
while zanzon - (1 / freq) * i > 0:
    cashflow.append(
        (zanzon - (1 / freq) * i, coupon / freq + (100 if i == 0 else 0))
    )
    i += 1
# 文法メモ"100 if i == 0 else 0"→iが0ならば100　iが0でなければ0


# バケットの中心時点を設定
buckets_timing = [0.0028, 0.0417, 0.1667, 0.375, 0.625, 0.875, 1.25, 1.75, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 12.5, 17.5, 25]

# バケットへの割当金額を初期化
buckets_amount = [0 for t in buckets_timing]

for t, a in cashflow:
    # CFの発生時期を元に前後のバケット時点を取得する
    prev_timing = max([b for b in buckets_timing if b < t])
    next_timing = min([b for b in buckets_timing if b > t])

    # tとの距離に比例して配分率を決める(近いほど配分率が大きい)
    prev_bucket_ratio = 1 - (t - prev_timing) / (next_timing - prev_timing)
    next_bucket_ratio = 1 - (next_timing - t) / (next_timing - prev_timing)

    prev_bucket_cf = a * prev_bucket_ratio
    next_bucket_cf = a * next_bucket_ratio

    # 前後のバケットに割当CF金額を加算する
    buckets_amount[buckets_timing.index(prev_timing)] += prev_bucket_cf
    buckets_amount[buckets_timing.index(next_timing)] += next_bucket_cf


# イールドカーブ上の金利を求める関数を作成
# べき乗分母
x = 4.0

# パラレルシフトシナリオ
def change_parallel(parallel):
    return parallel

# スティープ化シナリオ
def change_steepner(t, rshort, rlong):
    return -0.65 * (rshort * math.e ** (-t / x)) + 0.9 * (rlong * (1 - math.e ** (-t / x)))

# フラット化シナリオ
def change_flattener(t, rshort, rlong):
    return 0.8 * (rshort * math.e ** (-t / x)) - 0.6 * (rlong * (1 - math.e ** (-t / x)))

# 短期金利変化シナリオ
def change_short(t, rshort):
    return rshort * math.e ** (-t / x)


base_rate = -0.00035

# 長短金利とパラレル変動幅
parallel = 0.01
rshort = 0.01
rlong = 0.01

# 変化量を取得する
senario = [
    [(t, 0) for t in buckets_timing], # 変化なし
    [(t, change_parallel(parallel)) for t in buckets_timing], # 上方パラレルシフト
    [(t, change_parallel(parallel * -1)) for t in buckets_timing], # 下方パラレルシフト
    [(t, change_steepner(t, rshort, rlong)) for t in buckets_timing], # スティープ化
    [(t, change_flattener(t, rshort, rlong)) for t in buckets_timing], # フラット化
    [(t, change_short(t, rshort)) for t in buckets_timing], # 短期金利上昇
    [(t, change_short(t, rshort * -1)) for t in buckets_timing] #短期金利低下
]

discount_factors = [[ 1 / ((1 + r / freq) ** (t * freq)) for t, r in change ] for change in senario]

pvs = [ sum(buckets_amount  * np.array(df)) for df in discount_factors ]

for i, pv in enumerate(pvs):
    print(i, pv - pvs[0])