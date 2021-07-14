#Python 3.7.6
import pandas as pd




#將民國日期轉乘西園日期
#input: dataframe, column name of date
def change_calendar(df,col_date):
    df2 = df[col_date]
    df2 = df2.str.split('-', expand=True)
    df2[0] = df2[0].astype(int) + 1911
    df2[0] = df2[0].astype(str)
    df2[0] = df2[0] + '-' + df2[1] + '-' + df2[2]
    df2[0] = pd.to_datetime(df2[0])
    df[col_date] = df2[0]
    return df





#input:銷售資料
#uotput: RFM, 消費次數；最近一次消費時間；平均消費金額；總消費金額
def get_RFM(df):
    df_rfm = pd.DataFrame()
    df_group = df.groupby('客戶', as_index=False) \
        .agg({'單號': ['count'], '未稅本位幣': ['sum'], '銷貨日期': ['max']})

    df_rfm['客戶'] = df_group['客戶']
    df_rfm['消費次數'] = df_group['單號']
    df_rfm['總消費金額'] = df_group['未稅本位幣']
    df_rfm['平均消費金額'] = df_rfm['總消費金額'] / df_rfm['消費次數']
    df_rfm['最近一次消費時間'] = df_group['銷貨日期']
    return df_rfm


# 欄位加上年份跟月份
def rename_col(df, year, mon):
    col_lst = df.columns.values.tolist()
    for i in range(len(col_lst)):
        if col_lst[i] != '客戶':
            col_lst[i] = col_lst[i] + '_{0}-{1}'.format(year, mon)
    df.columns = col_lst
    return df


# 篩選時間
def select_period(df, year, mon):
    con1 = df['月份'] == mon
    con2 = df['年份'] == year
    return df[(con1 & con2)]


# 求出差異值&百分比
def get_diff(df_base, year, mon, df_compare, year_bf, mon_bf, key, col_compare):
    df_diff = pd.DataFrame()
    df_merge = df_base.merge(df_compare, how='outer', on=key)
    df_merge = df_merge.fillna(0)

    df_diff[key] = df_merge[key]

    for col in col_compare:
        df_diff[col + '差異'] = df_merge[col + '_{0}-{1}'.format(year, mon)] - df_merge[
            col + '_{0}-{1}'.format(year_bf, mon_bf)]
        df_diff[col + '成長率'] = df_diff[col + '差異'] / df_merge[col + '_{0}-{1}'.format(year_bf, mon_bf)]

        # 轉換百分比
        df_diff[col + '成長率'] = df_diff[col + '成長率'].apply(lambda x: format(x, '.2%'))
    return df_diff


if __name__ == '__main__':
    df = pd.read_csv('./銷貨明細表_test.csv')
    df = df.dropna()

    col_date = '銷貨日期'

    df = change_calendar(df,col_date)

    # 取得年、月份資料
    df['月份'] = pd.DatetimeIndex(df['銷貨日期']).month
    df['年份'] = pd.DatetimeIndex(df['銷貨日期']).year

    # 設定要觀察資料的月份、年分
    mon = 7
    year = 2021

    # 設定要比較資料的月份、年分
    mon_bf = 6
    year_bf = 2021

    df_base = select_period(df, year, mon)
    df_base_rfm = rename_col(get_RFM(df_base), year, mon)

    df_compare = select_period(df, year_bf, mon_bf)
    df_compare_rfm = rename_col(get_RFM(df_compare), year_bf, mon_bf)

    col_compare = ['消費次數', '總消費金額', '平均消費金額']
    key = '客戶'

    df_diff = get_diff(df_base_rfm, year, mon, df_compare_rfm, year_bf, mon_bf, key, col_compare)

    df_m1 = df_base_rfm.merge(df_compare_rfm, how='outer', on=key)
    df_result = df_m1.merge(df_diff, how='outer', on=key)

    df_result.to_csv('./6月&7月天心銷售資料比較.csv', encoding='utf_8_sig')