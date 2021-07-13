# Python 3.7.6

import pandas as pd
import numpy as np
import sklearn
from sklearn.decomposition import TruncatedSVD




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






#將天心銷售資料第一階段清理
#drop na, add ';' after 商品名稱
def data_cleasing(df,col_item):
    df = df.dropna()
    df['tmp'] = ';'
    df[col_item] = df[col_item] + df['tmp']
    df = df.drop(['tmp'], axis=1)

    return df






#input:dataframe after group by, column name of item
#output: list of item(不重複)
def get_item(df_cust, col_item):
    df_cust[col_item] = df_cust[col_item].str.split(';')
    item_list = df_cust[col_item].values.tolist()

    #get unique
    record = []
    for i in item_list:
        record = record + i
    while '' in record:
        record.remove('')

    set_unique = set(record)
    record = list(set_unique)

    return record




#input: dataframe after group, column name of item and customer, list of item

#output1: sparse matrix for CF after transpose
#output2:  dataframe after group drop col_item(不然後面矩陣shape會不一樣)
def get_sparse_matrix(df_cust,col_cust,col_item,record):
    new_col = df_cust.columns.tolist()
    new_col = new_col + record
    df_cust = df_cust.reindex(columns=new_col)
    df_cust = df_cust.fillna(0)

    # set first column as index, and drop it
    df_cust = df_cust.set_index(col_cust)

    # 填入商品的購買次數，轉成spare matrix
    for item, position in zip(df_cust[col_item], range(len(df_cust[col_item]))):
        for j in item:
            if j in record:
                df_cust[j][position] = df_cust[j][position] + 1   #這邊會跳warning因為pandas 官方不建議[][]的形式
                # print(df_cust[j])

    #最後才能把品名這column刪除
    df_cust = df_cust.drop([col_item], axis=1)
    sparse_matrix = df_cust.T
    return sparse_matrix, df_cust




#input: sparse matrix, SVD parameters
#uotput: correlation matrix of items
def get_corr_matrix(sparse_matrix, comp_num, rand_stat):
    #Truncated SVD 取出主成分，降維處理(類似pca)
    SVD = TruncatedSVD(n_components=comp_num, random_state=rand_stat)
    resultant_matrix = SVD.fit_transform(sparse_matrix)
    corr_mat = np.corrcoef(resultant_matrix)



    var_explained = SVD.explained_variance_ratio_.sum()
    #顯示模型解釋力
    print(var_explained)
    return corr_mat




#input: 推薦商品名單，, 商品在dataframe的位置, 參照的dataframe, 推薦數量
#output:推薦結果
def reccomend_result(col_item_list, corr_mat,df_cust, num_item):
    df_result = pd.DataFrame()

    for item in col_item_list:
        col_idx = df_cust.columns.get_loc(item)
        corr_specific = corr_mat[col_idx]

        df_tmp = pd.DataFrame({'推薦分數:{0}'.format(item): corr_specific, '推薦名單:{0}'.format(item): df_cust.columns}) \
        .sort_values('推薦分數:{0}'.format(item), ascending=False)\



        df_tmp = df_tmp.head(num_item + 1)


        df_tmp = df_tmp.reset_index()
        df_tmp = df_tmp.drop(['index'],axis=1)
        df_result = pd.concat([df_result,df_tmp], axis=1)
        # print(df_tmp)
        # print(df_result)
    return df_result




if __name__ == '__main__':
    df = pd.read_csv('./銷貨明細表_test.csv')
    df = df.dropna()
    col_item ='品名'
    col_date = '銷貨日期'
    col_cust = '客戶'

    df = change_calendar(df,col_date)

    df = data_cleasing(df,col_item)

    df_cust = df.groupby(col_cust).agg({col_item: 'sum'}).reset_index()

    record = get_item(df_cust,col_item)

    sparse_matrix,df_cust = get_sparse_matrix(df_cust,col_cust,col_item,record)


    comp_num = 10
    rand_stat = 7
    corr_mat = get_corr_matrix(sparse_matrix,comp_num,rand_stat)

    col_item_list = ['統欣膠原蛋白粉20入袋裝','日香冬筍餅(中)']

    #推薦顯示10個
    num_item = 10
    df_result = reccomend_result(col_item_list,corr_mat,df_cust,num_item)

    df_result.to_csv('./協同過濾推薦結果.csv',encoding='utf_8_sig')
