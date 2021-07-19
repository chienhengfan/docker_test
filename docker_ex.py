# python version: Python 3.7.6



# this is easy docker exaple, merely use pandas to read csv( from kaggle) groupby and show
import pandas as pd

df = pd.read_csv('./supermarket_sales - Sheet1.csv')

df_gp = df.groupby(['City']).agg({'Total':'sum'})

print(df_gp)


