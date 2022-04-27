import time

import pandas as pd
import requests
from selenium import webdriver
import bs4
'''
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

pd.DataFrame(a_href).to_csv('/Users/junho/Desktop/data/final_csv/url.csv')
#
len(a_href)
len(set(a_href))

article = []
for i in range(len(a_href)):
    res = requests.get(a_href[i], headers={'User-Agent':'Mozilla/5.0'})
    bs_obj = bs4.BeautifulSoup(res.text)
    temp = bs_obj.find('div',{'id':'dic_area'}).text
    article.append(temp.replace('\n',' ').replace('\t',' ').replace('\'','')
                   .replace('\xa0',' ').replace('[파이낸셜뉴스]','').replace('/','')
                   .replace('사진=','').strip())
    print(f'process : {i+1}/{len(a_href)}')
article
'''




# 채원 news_link 검색 : 파이낸셜뉴스,카카오 주가
# 검색어,회사명 옵션

import requests
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome('/Users/junho/Downloads/chromedriver')

url = 'https://search.naver.com/search.naver?where=news&query=%EC%B9%B4%EC%B9%B4%EC%98%A4%20%EC%A3%BC%EA%B0%80&sm=tab_opt&sort=1&photo=0&field=0&pd=5&ds=&de=&docid=&related=0&mynews=1&office_type=1&office_section_code=3&news_office_checked=1014&nso=so%3Add%2Cp%3A1y&is_sug_officeid=0'
driver.get(url)

headers = {'User-Agent':'Mozilla/5.0'}
res = requests.get(url, headers=headers)
bs = BeautifulSoup(res.text, 'html.parser')

news_link = []
final = bs.find('a', {'class': 'btn_next'})['aria-disabled']

while True:
    if final == 'true':
        news_body = bs.find('div', {'class': 'group_news'})
        links = news_body.find_all('a', {'class': 'info'})
        for link in links:
            if link.text == '네이버뉴스':
                news_link.append(link['href'])
        break
    news_body = bs.find('div', {'class': 'group_news'})
    links = news_body.find_all('a', {'class': 'info'})
    for link in links:
        if link.text == '네이버뉴스':
            news_link.append(link['href'])
    next_url = 'https://search.naver.com/search.naver' + bs.find('a', {'class': 'btn_next'})['href']
    driver.find_element_by_class_name('btn_next').click()

    # 다음 페이지 url 탐색
    res = requests.get(next_url, headers=headers)
    bs = BeautifulSoup(res.text, 'html.parser')
    final = bs.find('a', {'class': 'btn_next'})['aria-disabled']  # 이렇게 하면 바로 while문을 탈출하여 마지막 페이지는 크롤링이 안 되는 문제
#########
import pandas as pd
import bs4


raw_article = []
for i in range(len(news_link)):
    res = requests.get(news_link[i], headers=headers)
    bs_obj = bs4.BeautifulSoup(res.text)
    temp = bs_obj.find('div',{'id':'dic_area'}).text
    raw_article.append(temp.replace('\n', ' ').replace('\t', ' ')
                   .replace('\xa0', ' ').replace('\u','').replace('/', '')
                   .replace('↑',' 상승').replace('↓', ' 하락').strip())
    print(f'process : {i+1}/{len(news_link)}')
pd.DataFrame(raw_article).to_csv('/Users/junho/Desktop/data/final_csv/raw_article.csv')

raw_article
#raw_article = pd.read_csv('/Users/junho/Desktop/data/final_csv/raw_article.csv')
#list(raw_article['0'])
raw_article = list(pd.read_csv('/Users/junho/Desktop/data/final_csv/raw_article.csv')['0'])
raw_article

import re
processing_article = []

for idx in raw_article:
    text = idx
    text = re.sub('\([^\(\)]+\)|\[[^\[\]]+\]|<[^<>]+>','',text)
    text = re.sub('[=+,#/\?:^*\"※&!』…》ⓒ▶■]','', text)
    processing_article.append(text)

raw_article
processing_article
len(processing_article)



raw_article
