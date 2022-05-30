from pymongo import MongoClient
import pandas as pd
from pykrx import stock
from datetime import datetime,timedelta
from googletrans import Translator
import numpy as np
import requests
import re
import bs4
from transformers import pipeline
import time

my_client = MongoClient('mongodb://localhost:27017')
mydb = my_client['final_project']


'''
# sample
# pykrx_stock_data : initial year setting
company_number = '035720' #: kakao

temp = [datetime.strftime(i.date(),'%Y-%m-%d') for i in pd.date_range(datetime.today()-timedelta(days=365),periods=366).to_list()]

for i in range(len(temp)):
    try:

        pykrx_df = stock.get_market_ohlcv_by_date(fromdate=temp[i],
                                                  todate=temp[i],
                                                  ticker=company_number)

        pykrx_df.reset_index(inplace=True)
        mycol.insert_one({'date':datetime.strftime(pykrx_df.iloc[0,0].date(), '%Y-%m-%d'),
                          'start':int(pykrx_df.iloc[0,1]),
                          'high':int(pykrx_df.iloc[0,2]),
                          'low':int(pykrx_df.iloc[0,3]),
                          'close':int(pykrx_df.iloc[0,4]),
                          'volume':int(pykrx_df.iloc[0,5])})

    except:
        mycol.insert_one({'date':temp[i]})

my_client = MongoClient('mongodb://localhost:27017')
mydb = my_client['final_project']
pykrx_df = pd.DataFrame(mydb.kakao_pykrx_stock_data.find({})).drop('_id',axis=1)
pykrx_df.fillna(method='ffill',inplace=True)
pykrx_df.fillna(method='bfill',inplace=True)
'''

qa = pipeline("question-answering")
zs = pipeline('zero-shot-classification')


import warnings
warnings.filterwarnings('ignore')


def craw(comp):
    if comp == 'kakao':
        code = '035720'  # kakao
    else:
        code = '035420'  # naver

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32'}

    date_list = []
    title_list = []
    info_list = []
    url_list = []

    sub_date_list = []
    sub_title_list = []
    sub_info_list = []
    sub_url_list = []

    for page in range(1, 3):
        url = f'https://finance.naver.com/item/news_news.naver?code={code}&page={page}&sm=title_entity_id.basic&clusterId='
        res = requests.get(url, headers=headers)
        bs = bs4.BeautifulSoup(res.text, 'html.parser')

        # 뉴스 전체 크롤링
        art_cnt = len(bs.find_all('td', {'class': 'title'}))
        for i in range(art_cnt):
            date_list.append(bs.find_all('td', {'class': 'date'})[i].text.split()[0].replace('.', '-'))
            title_list.append(bs.find_all('td', {'class': 'title'})[i].text.replace('\n', ''))
            info_list.append(bs.find_all('td', {'class': 'info'})[i].text)
            url_list.append('https://finance.naver.com' + bs.find_all('td', {'class': 'title'})[i].find('a')['href'])

        # 관련 뉴스만 크롤링
        chk = 1
        while True:
            try:
                chk_len = len(bs.find_all('table', {'class': 'type5'})[chk].find_all('td', {'class': 'title'}))
                for i in range(chk_len):
                    sub_date_list.append(
                        bs.find_all('table', {'class': 'type5'})[chk].find_all('td', {'class': 'date'})[i].text.split()[
                            0].replace('.', '-'))
                    sub_title_list.append(
                        bs.find_all('table', {'class': 'type5'})[chk].find_all('td', {'class': 'title'})[
                            i].text.replace('\n', ''))
                    sub_info_list.append(
                        bs.find_all('table', {'class': 'type5'})[chk].find_all('td', {'class': 'info'})[i].text)
                    sub_url_list.append('https://finance.naver.com' +
                                        bs.find_all('table', {'class': 'type5'})[chk].find_all('td',
                                                                                               {'class': 'title'})[
                                            i].find('a')['href'])
                chk += 1
            except:
                break
    df = pd.DataFrame()
    df['날짜'] = date_list
    df['제목'] = title_list
    df['정보제공'] = info_list
    df['링크'] = url_list

    df2 = pd.DataFrame()  # 관련기사
    df2['날짜'] = sub_date_list
    df2['제목'] = sub_title_list
    df2['정보제공'] = sub_info_list
    df2['링크'] = sub_url_list

    result = pd.concat([df,df2])
    result = result.drop_duplicates('제목',keep=False)
    result = result[result['날짜']==datetime.strftime(datetime.now().date(), '%Y-%m-%d')]

    # sub
    url_list = result['링크'].to_list()
    #print(url_list)
    art_list = []
    for i in range(len(url_list)):
        url = url_list[i]
        res = requests.get(url, headers = headers)
        bs = bs4.BeautifulSoup(res.text, 'html.parser')
        art_list.append(bs.find_all('div',{'class':'scr01'})[0].text)
        print(i)

    tst = []
    for art in art_list:
        tp = art.replace('\n|\t|\xa0|\u200b',' ') # \n,\t,\xa0,\u200b 삭제
        tp = tp.replace("'|‘|’",'"') # 따옴표 모두 큰따옴표로 통일
        tp = tp.replace('↑','상승').replace('↓','하락') # ↑↓ 치환
        tp = tp.replace('\([^\(\)]*?\)|\[[^\[\]]*?\]|<[^<>]*?>',' ').replace('\([^\(\)]*?\)|\[[^\[\]]*?\]|<[^<>]*?>',' ') # (),[],<> 제거
        tp = tp.replace('·+',',') # ·을 ,로 치환
        tp = tp.replace('[가-힣]{2,3} ?기자',' ') # 홍길동 기자 삭제
        tp = tp.replace('[a-z0-9]+@',' ') # 기자 태그 삭제
        tp = tp.replace('사진=|사진 ?제공=',' ') # 사진 태그 삭제
        tp = tp.replace('[^ 0-9ㄱ-ㅎ가-힣a-zA-Z"%&,.~-]', ' ')  # 특수문자 삭제
        tp = tp.replace('\.+', '.')  # . 2개 이상이면 1개만 남김
        tp = tp.replace(' +', ' ')  # 공백 2개 이상이면 1개만 남김
        tp = tp.replace("\'","")
        tp = tp.strip()  # 좌우 공백 제거
        tst.append(tp)

    translator = Translator()

    cnt = 0
    trs_art = []
    for i in tst:
        cnt += 1
        try:
            entext = translator.translate(i, src = 'ko', dest = 'en').text
            trs_art.append(entext)
        except:
            trs_art.append('')
            print(f'{cnt}번째는 번역 실패')


    #label = ['fear','greed']
    #cnt = 0
    #question = 'Will the stock price of cacao go up?'
    return result,trs_art


def daily_score(result,trs_art,question,label):
    score = []

    for sequence in trs_art:
        if sequence == '':
            pass
        else:
            sequence = qa(question=question,context=sequence)
            temp = zs(sequence.get('answer'),label)
            temp_score = abs(temp['scores'][0]-temp['scores'][1])
            #cnt += 1

            if temp['labels'][0] == label[0]:
                score.append(-temp_score)
                #print(f'{cnt}/{len(trs_art)}' + f': append -{temp_score}')
            else:
                score.append(temp_score)
                #print(f'{cnt}/{len(trs_art)}' + f': append {temp_score}')

    return result['날짜'],score

def daily_mongo_update(comp,db_location):
    #comp = 'kakao'
    result,trs_art = craw(comp)
    if trs_art:
        print('score1')
        question1 = f'Has the price of {comp} stock increased from the previous day?'
        label1 = ['price positive', 'price negative']
        res, tp1 = daily_score(result,trs_art, question1, label1)

        print('score2')
        question2 = f'Will the situation for the {comp} company improve in the future?'
        label2 = ['situation POSITIVE','situation NEGATIVE']
        res, tp2 = daily_score(result,trs_art,question2,label2)

        print('score3')
        question3 = f'Can {comp} Grow in the Future?'
        label3 = ['grow POSITIVE', 'grow NEGATIVE']
        res, tp3 = daily_score(result,trs_art, question3, label3)
        # label (negative mean,positive mean)
        # import FinanceDataReader as fdr
        temp = res.reset_index().drop('index',axis=1).to_dict() # article_url

        df = pd.DataFrame(columns=['날짜','score1','score2','score3'])
        df['날짜'] = res
        df['score1'] = tp1
        df['score2'] = tp2
        df['score3'] = tp3
        df.fillna(0)
        df = df.groupby('날짜').mean().reset_index()

        mycol = mydb[db_location]
        mycol.insert_one({'date': df['날짜'][0], 'score1': df['score1'][0],
                          'score2': df['score2'][0], 'score3': df['score3'][0]})
        # time delta
        # mycol.delete_many({'date':datetime.strftime((datetime.now()-timedelta(days=365)).date(), '%Y-%m-%d')})
        print('mongo update ^^7')

    else:
        print('Have no article')

def initial_year_score():
    sample1 = pd.read_csv('/Users/junho/Downloads/kakao기사_전처리_번역_score1&2&3.csv').drop('Unnamed: 0',axis=1) # 5/24
    sample2 = pd.read_csv('/Users/junho/Downloads/naver기사_전처리_번역_score1&2&3.csv').drop('Unnamed: 0',axis=1) # 5/25
    sample1 = sample1.loc[:,['날짜','score1','score2','score3']]
    sample2 = sample2.loc[:,['날짜','score1','score2','score3']]
    sample1 = sample1.groupby('날짜').mean()
    sample2 = sample2.groupby('날짜').mean()
    sample1 = sample1.reset_index()
    sample2 = sample2.reset_index()

    mycol = mydb['kakao_score']
    for i in range(len(sample1)):
        mycol.insert_one({'date':sample1['날짜'][i],'score1':sample1['score1'][i],
                          'score2':sample1['score2'][i],'score3':sample1['score3'][i]})

    mycol = mydb['naver_score']
    for i in range(len(sample2)):
        mycol.insert_one({'date':sample2['날짜'][i],'score1':sample2['score1'][i],
                          'score2':sample2['score2'][i],'score3':sample2['score3'][i]})



daily_mongo_update('kakao','kakao_score') # 하루에 특정 시점 한번 실행 company, collection
daily_mongo_update('naver','naver_score')


pd.DataFrame(mydb['kakao_score'].find())
pd.DataFrame(mydb['naver_score'].find())

