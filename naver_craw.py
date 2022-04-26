import time

import pandas as pd
import requests
from selenium import webdriver
import bs4

driver = webdriver.Chrome('/Users/junho/Downloads/chromedriver')
url = 'https://search.naver.com/search.naver?where=news&query=%EC%B9%B4%EC%B9%B4%EC%98%A4%20%EC%A3%BC%EA%B0%80&sm=tab_opt&sort=1&photo=0&field=0&pd=5&ds=&de=&docid=&related=0&mynews=1&office_type=1&office_section_code=3&news_office_checked=1014&nso=so%3Add%2Cp%3A1y&is_sug_officeid=0'
driver.get(url)

a_href = []
while 1:
    bs_obj = bs4.BeautifulSoup(driver.page_source)
    target = bs_obj.find('div', {'class': 'group_news'})
    atags = target.find_all('a')
    cnt = 0
    for a in atags:
        if 'news.naver.com' in str(a):
            a_href.append(a['href'])
            cnt += 1
    driver.find_element_by_xpath('//*[@id="main_pack"]/div[2]/div/a[2]').click()
    if cnt != 10:
        break

a_href
len(a_href)
len(set(a_href))

article = []
for i in range(len(a_href)):
    res = requests.get(a_href[i], headers={'User-Agent':'Mozilla/5.0'})
    bs_obj = bs4.BeautifulSoup(res.text)
    temp = bs_obj.find('div',{'id':'dic_area'}).text
    article.append(temp.replace('\n',' ').replace('\t',' ').replace('\'','')
                   .replace('\xa0',' ').strip())
    print(f'process : {i+1}/{len(a_href)}')
article


