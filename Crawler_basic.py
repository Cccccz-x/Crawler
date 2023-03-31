from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver import ChromeOptions

with open("stock_basic.csv", "w", encoding="UTF-8") as f:
    f.write("TS代码,股票代码,股票名称,行业\n")

home_url = 'https://www.9fzt.com/marketCenter/aStockMarket.html?tab=0'

option = ChromeOptions()
option.add_argument('--headless')
wd = webdriver.Chrome(options=option)
wd.implicitly_wait(5)
wd.get(home_url)
mainWindow = wd.current_window_handle

wd.find_element(By.CSS_SELECTOR, '[param="1"]').click()
sleep(0.1)

stock_code = 0
# page_num = int(wd.find_element(By.CSS_SELECTOR, '.c-pagination div:nth-last-of-type(1)').text[1:-1])
page_num = 5
for page in range(page_num):
    sleep(0.1)
    num = len(wd.find_elements(By.CSS_SELECTOR, '.table-body>*'))
    for i in range(num):
        css = '.table-body>*:nth-child(' + str(i + 1) + ')'
        stock = wd.find_element(By.CSS_SELECTOR, css)
        wd.execute_script("arguments[0].click();", stock)
        for handle in wd.window_handles:
            if handle != mainWindow:
                wd.switch_to.window(handle)
                break
        stock_code += 1
        stock_name = wd.find_element(By.CSS_SELECTOR, '#__next [style="float:left"] span:nth-child(1)')
        stock_TScode = wd.find_element(By.CSS_SELECTOR, '#__next [style="float:left"] span:nth-child(2)')
        company_contents = wd.find_elements(By.CSS_SELECTOR, '.Company_content__1b6_z>div')
        stock_industry = company_contents[1].find_element(By.CSS_SELECTOR, 'span:nth-child(2)')
        with open("stock_basic.csv", "a", encoding="UTF-8") as f:
            f.write(
                stock_TScode.text + ',' + str(stock_code) + ',' + stock_name.text + ',' + stock_industry.text + '\n')
        # print(stock_TScode.text, stock_code, stock_name.text, stock_industry.text)
        wd.close()
        wd.switch_to.window(mainWindow)
    next_page = wd.find_element(By.CSS_SELECTOR, '.c-pagination [name="whj_nextPage"] img')
    wd.execute_script("arguments[0].click();", next_page)

wd.find_element(By.CSS_SELECTOR, '[param="2"]').click()
sleep(0.1)

for page in range(page_num):
    sleep(0.1)
    num = len(wd.find_elements(By.CSS_SELECTOR, '.table-body>*'))
    for i in range(num):
        css = '.table-body>*:nth-child(' + str(i + 1) + ')'
        stock = wd.find_element(By.CSS_SELECTOR, css)
        wd.execute_script("arguments[0].click();", stock)
        for handle in wd.window_handles:
            if handle != mainWindow:
                wd.switch_to.window(handle)
                break
        stock_code += 1
        stock_name = wd.find_element(By.CSS_SELECTOR, '#__next [style="float:left"] span:nth-child(1)')
        stock_TScode = wd.find_element(By.CSS_SELECTOR, '#__next [style="float:left"] span:nth-child(2)')
        company_contents = wd.find_elements(By.CSS_SELECTOR, '.Company_content__1b6_z>div')
        stock_industry = company_contents[1].find_element(By.CSS_SELECTOR, 'span:nth-child(2)')
        with open("stock_basic.csv", "a", encoding="UTF-8") as f:
            f.write(
                stock_TScode.text + ',' + str(stock_code) + ',' + stock_name.text + ',' + stock_industry.text + '\n')
        # print(stock_TScode.text, stock_code, stock_name.text, stock_industry.text)
        wd.close()
        wd.switch_to.window(mainWindow)
    next_page = wd.find_element(By.CSS_SELECTOR, '.c-pagination [name="whj_nextPage"] img')
    wd.execute_script("arguments[0].click();", next_page)

wd.quit()
