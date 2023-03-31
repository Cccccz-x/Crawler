from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import pandas as pd

with open("stock_announcements.csv", "w", encoding="UTF-8") as f:
    f.write("Ts_code,Ann_date,Title\n")

stock_basic = pd.read_csv('stock_basic.csv', encoding='UTF-8')
url_list = ['https://stock.9fzt.com/index/', '', '.html']

option = ChromeOptions()
option.add_argument('--headless')
wd = webdriver.Chrome(options=option)
wd.implicitly_wait(10)

for i in range(len(stock_basic)):
    url_list[1] = stock_basic.values[i][0][-2:].lower() + '_' + stock_basic.values[i][0][:-3]
    url = ''.join(url_list)
    wd.get(url)
    stock_TScode = stock_basic.values[i][0]
    announcements = wd.find_elements(By.CSS_SELECTOR,
                                     '.float-right [style="height:257px;padding:8px;color:#333333"] div>div:nth-child(odd)')
    dates = wd.find_elements(By.CSS_SELECTOR,
                             '.float-right [style="height:257px;padding:8px;color:#333333"] div>div:nth-child(even)')
    with open("stock_announcements.csv", "a", encoding="UTF-8") as f:
        for j in range(len(announcements)):
            f.write(stock_TScode + ',' + announcements[j].text + ',' + dates[j].text + '\n')

wd.quit()
