from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import pandas as pd

with open("stock_holders.csv", "w", encoding="UTF-8") as f:
    f.write("Ts_code,Holder_name,Holder_amount,Hold_ratio\n")

stock_basic = pd.read_csv('stock_basic.csv', encoding='UTF-8')
url_list = ['https://f10.9fzt.com/views/gdyj.html?gilcode=', '', '&theme=white&type=0&name=', '', '&keyghost=false']

option = ChromeOptions()
option.add_argument('--headless')
wd = webdriver.Chrome(options=option)
wd.implicitly_wait(10)

for i in range(len(stock_basic)):
    url_list[1] = stock_basic.values[i][0]
    url_list[3] = stock_basic.values[i][2]
    url = ''.join(url_list)
    wd.get(url)
    stock_TScode = stock_basic.values[i][0]
    holders = wd.find_elements(By.CSS_SELECTOR, '#sdgd #tr')
    for holder in holders:
        attributes = holder.find_elements(By.CSS_SELECTOR, 'td')
        if ',' in attributes[0].text[1:]:
            name = ''.join(['"', attributes[0].text[1:], '"'])
        else:
            name = attributes[0].text[1:]
        with open("stock_holders.csv", "a", encoding="UTF-8") as f:
            f.write(stock_TScode + ',' + name + ','
                    + attributes[1].text + ',' + attributes[2].text + '\n')

wd.quit()
