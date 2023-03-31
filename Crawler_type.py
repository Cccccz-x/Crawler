import pandas as pd

with open("stock_type.csv", "w", encoding="UTF-8") as f:
    f.write("Ts_code,Hs_type\n")
stock_basic = pd.read_csv('stock_basic.csv', encoding='UTF-8')
for i in stock_basic.values:
    with open("stock_type.csv", "a", encoding="UTF-8") as f:
        f.write(i[0]+','+i[0][-2:]+'\n')
