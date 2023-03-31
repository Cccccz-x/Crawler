from pandas import DataFrame
import pandas as pd

stock = pd.read_csv('stock_basic.csv', encoding="UTF-8")
stock = stock.drop(["股票代码"],axis=1)

stock.to_csv('stock_basic1.csv',index=False)