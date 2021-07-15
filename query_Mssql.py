# Python 3.7.6

import pyodbc
import pandas as pd


class MSSQL:

    #insert:condition
    #output:dataframe of your query
    def get_data(host,user,pw,DB,query):
        conn = pyodbc.connect('DRIVER=ODBC Driver 17 for SQL Server;SERVER={0};DATABASE={3};UID={1};PWD={2}'.format(
         host,user, pw,DB
        ))

        query = query

        df = pd.read_sql(query, conn)

        conn.close()
        return df

    #insert:codition
    #output: dataframe of check data inserted
    # def insert_data(host,user,pw,DB,columns,target_table,source_table,tuple_CUS_NO):
    #     conn = pyodbc.connect('DRIVER=ODBC Driver 17 for SQL Server;SERVER={0};DATABASE={3};UID={1};PWD={2}'.format(
    #         host, user, pw, DB
    #     ))
    #
    #     cursor = conn.cursor()
    #
    #     cursor.execute("INSERT INTO {0}({1}) SELECT {1} FROM {2} WHERE CUS_NO IN {3}".format(target_table,columns,source_table,tuple_CUS_NO))
    #     df_check = pd.read_sql("SELECT * FROM {0} WHERE CUS_NO IN {1}".format(target_table,tuple_CUS_NO),conn)
    #
    #     cursor.close()
    #     conn.close()
    #     return df_check



def read_json(location,file):
    with open(location+file,'r') as f:
        text = f.read()
    return text




if __name__ == '__main__':
    host = read_json('D:/secret/sunlike_DB/','host.txt')
    user = read_json('D:/secret/sunlike_DB/','user.txt')
    pw = read_json('D:/secret/sunlike_DB/','password.txt')

    DB = 'DB_WH01'
    query1 = "SELECT * FROM TF_POS"

    df_cust_wh01 = MSSQL.get_data(host,user,pw,DB,query1)
    df_cust_wh01.to_csv('./MF_BOM_WH01.csv',encoding='utf_8_sig')


    #
    # DB2 = 'DB_WUHU'
    # query2 = "SELECT * FROM DB_WUHU.dbo.CUST"
    #
    # df_cust_wh01 = MSSQL.get_data(host, user, pw, DB2, query2)
    # df_cust_wh01.to_csv('./CUST_WUHU.csv',encoding='utf_8_sig')
