from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import pandas as pd

with open("stock_concept.csv", "w", encoding="UTF-8") as f:
    f.write("Id,Concept_name,Ts_code\n")

stock_basic = pd.read_csv('stock_basic.csv', encoding='UTF-8')
url_list = ['https://f10.9fzt.com/views/index.html?gilcode=', '', '&type=4&name=', '']

option = ChromeOptions()
option.add_argument('--headless')
wd = webdriver.Chrome(options=option)
wd.implicitly_wait(10)

Id = 0
concept_id_dic = {}
for i in range(len(stock_basic)):
    url_list[1] = stock_basic.values[i][0]
    url_list[3] = stock_basic.values[i][2]
    url = ''.join(url_list)
    wd.get(url)
    stock_TScode = stock_basic.values[i][0]
    concepts = wd.find_element(By.CSS_SELECTOR, '#sjgl')
    while concepts.text == '':
        pass
    concepts_list = concepts.text.split(sep=',')
    with open("stock_concept.csv", "a", encoding="UTF-8") as f:
        for concept in concepts_list:
            if concept_id_dic.get(concept) is None:
                concept_id_dic[concept] = 'TS' + str(Id)
                Id += 1
            f.write(concept_id_dic[concept] + ',' + concept + ',' + stock_TScode + '\n')

wd.quit()
