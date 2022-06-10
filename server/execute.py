import streamlit as st
import pandas as pd
from datetime import datetime,timedelta
import bs4
import requests
from pykrx import stock
import matplotlib.pyplot as plt
import numpy as np
from pymongo import MongoClient
import re
from PIL import Image
from datetime import date, timedelta


from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression # 앙상블 조합용
from sklearn.neighbors import KNeighborsClassifier # 앙상블 조합용
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
import xgboost as xgb

from sklearn.preprocessing import *
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM, GRU
from sklearn.metrics import mean_squared_error, r2_score
import tensorflow as tf

#@st.cache(suppress_st_warning=True)

class SideTab():
    def __init__(self):
        #self.data1 = pd.read_csv('/Users/junho/Desktop/stream/data/data_not_scaled.csv')
        #self.data2 = pd.read_csv('/Users/junho/Desktop/stream/data/카카오 투자자별 매매동향.csv', encoding='cp949')
        
        pass
    '''
    def sidebar_price_widget(self):
        data = self.data1.iloc[-2:,[5,6,2]]
        with st.sidebar:
            for col in range(len(data.columns)):
                st.metric(label=f'{data.columns[col]}', value=f'{data.iloc[1,col]} P',
                          delta=f'{round(data.iloc[1,col]-data.iloc[0,col],2)} '
                                f'({round(round(data.iloc[1,col]-data.iloc[0,col],2)/round(data.iloc[0,col],2)*100,2)}%)',
                          delta_color='off')

    def sidebar_volume_widget(self):
        data = self.data2
        data = pd.DataFrame(data.iloc[0,[1,3,4]])
        data = data.transpose()

        with st.sidebar:
            for col in range(len(data.columns)):
                st.metric(label=f'{data.columns[col]}', value=f'{data.iloc[0,col]}',
                          delta_color='off')
    '''
    def sidebar_price_now(self,comp,comp_code):
        my_client = MongoClient('mongodb://18.181.49.139:27017')
        mydb = my_client['final_project']
        tp = pd.DataFrame(mydb['company_price'].find({})).drop('_id',axis=1)
        tp.set_index('code',inplace=True)
        rate = round(tp.loc[comp_code,'등락률'],2)
        yesterday_price = tp.loc[comp_code,'전일비']
        with st.sidebar:
            st.metric(label=comp,
                      value=f"{tp.loc[comp_code,'종가']} 원",
                          delta=f'{yesterday_price}({rate}%)',
                          delta_color='off')
        '''
        url = f'https://finance.naver.com/item/main.naver?code={comp_code}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}

        res = requests.get(url, headers=headers)
        bs_obj = bs4.BeautifulSoup(res.text)
        today = bs_obj.find_all('p', {'class': 'no_today'})
        exday = bs_obj.find_all('p', {'class': 'no_exday'})
        temp0 = [i.text for i in today][0].split('\n')
        temp = [i.text for i in exday][0].split('\n')

        tp = -int(temp[5].replace(',',''))

        if '하락' in temp:
            with st.sidebar:
                st.metric(label=comp,
                          value=f"{temp0[2]} 원",
                          delta=f'{tp} (-{temp[-4]}%)',
                          delta_color='off')
        elif '상승' in temp:
            with st.sidebar:
                st.metric(label=comp,
                    value=f"{temp0[2]} 원",
                    delta=f'{temp[5]} ({temp[-4]}%)',
                    delta_color='off')
        '''
    def sidebar_price_widget(self,comp,comp_code):
        my_client = MongoClient('mongodb://18.181.49.139:27017')
        mydb = my_client['final_project']
        tp = pd.DataFrame(mydb['side_price'].find({})).drop('_id',axis=1)
        tp.set_index('code',inplace=True)
        rate = round(tp.loc[comp_code,'등락률'],2)
        yesterday_price = round(tp.loc[comp_code,'전일비'],2)
        with st.sidebar:
            st.metric(label=comp,
                      value=f"{tp.loc[comp_code,'종가']}",
                          delta=f'{yesterday_price}({rate}%)',
                          delta_color='off')
        '''
        url = 'http://www.krx.co.kr/main/main.jsp'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}

        res = requests.get(url, headers=headers)
        bs_obj = bs4.BeautifulSoup(res.text)
        data = bs_obj.find_all('div', {'class': 'section-wap-top'})

        temp = [i.text for i in data][0].split('\n')
        columns = []
        ls = []

        for i in range(len(temp)):
            if not temp[i]:
                continue
            else:
                if temp[i][0] == 'K':
                    columns.append(temp[i])
                else:
                    ls.append(temp[i].split())

        for i in ls:
            if "▼" in i[0]:
                i[0] = i[0].replace('▼', '')
                i[1] = -float(i[1])
                i[2] = i[2].strip('(').strip(')')
            else:
                i[0] = i[0].replace('▲', '')
                i[2] = i[2].strip('(').strip(')')

        columns = [columns[1], columns[3]]
        ls = [ls[1], ls[3]]

        with st.sidebar:
            for col in range(len(columns)):
                st.metric(label=f'{columns[col]}',
                          value=f'{ls[col][0]} P',
                          delta=f'{ls[col][1]} ({ls[col][2]}%)',
                          delta_color='off')

        '''
class Article():
    def __init__(self,company):
        if company == '카카오':
            company = 'kakao'
        else:
            company = 'naver'
        my_client = MongoClient('mongodb://18.181.49.139:27017')
        mydb = my_client['final_project']
        self.data = pd.DataFrame(mydb[f'{company}_article'].find({}))
        
        '''
        date_list = []
        title_list = []
        info_list = []
        url_list = []

        if company == '카카오':
            code = '035720' # kakao
        else:
            code = '035420' # naver
        page = 1

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.32'}

        url = f'https://finance.naver.com/item/news_news.naver?code={code}&page={page}&sm=title_entity_id.basic&clusterId='
        res = requests.get(url, headers=headers)
        bs = bs4.BeautifulSoup(res.text, 'html.parser')

        while datetime.strftime(datetime.now().date() + timedelta(days=-day), '%Y-%m-%d') not in date_list:
            url = f'https://finance.naver.com/item/news_news.naver?code={code}&page={page}&sm=title_entity_id.basic&clusterId='
            res = requests.get(url, headers=headers)
            bs = bs4.BeautifulSoup(res.text, 'html.parser')

            date_list.extend([i.text.split()[0].replace('.', '-') for i in bs.find_all('td', {'class': 'date'})])
            title_list.extend([i.text.replace('\n', '') for i in bs.find_all('td', {'class': 'title'})])
            info_list.extend([i.text for i in bs.find_all('td', {'class': 'info'})])
            url_list.extend(
                ['https://finance.naver.com' + i.find('a')['href'] for i in bs.find_all('td', {'class': 'title'})])

            page += 1

        self.data = pd.DataFrame([date_list, title_list, info_list, url_list], index=['날짜', '제목', '정보제공', '링크']).transpose()
        self.data = self.data.drop_duplicates('제목')
        '''

    def company_list(self):
        return list(self.data.value_counts('정보제공').reset_index()['정보제공'])  # 17

    def recent_article(self,head):
        companys = list(pd.DataFrame(self.data.value_counts('정보제공')).reset_index()['정보제공'])
        stream_show = []
        for company in companys:
            stream_show.append(self.data.groupby('정보제공').get_group(company).head(head))
        return stream_show

    def recent_article_mark(self,data,head=30):
        #recent = self.recent_article(head)
        recent = data
        article_setting = []
        for compnum in range(len(recent)):
            temp = []
            for dnum in ['날짜', '제목', '링크']:
                temp.append(list(recent[compnum].loc[:, ['날짜', '제목', '링크']][dnum]))
            article_setting.append(temp)
        return article_setting

    def company_article(self):
        head = 10

        col1, col2 = st.columns(2)

        art = self.recent_article_mark(self.recent_article(head), head)
        cl = self.company_list()
        cnt = 0
        for company in range(len(cl)):
            if cnt == 0:
                with col1:
                    st.markdown(f'# 👉 {cl[company]}')
                    for i in range(head):
                        try:
                            st.markdown(f'({art[company][0][i]}) [{art[company][1][i]}]({art[company][2][i]})')
                        except:
                            break
                cnt += 1
            else:
                with col2:
                    st.markdown(f'# 👉 {cl[company]}')
                    for i in range(head):
                        try:
                            st.markdown(f'({art[company][0][i]}) [{art[company][1][i]}]({art[company][2][i]})')
                        except:
                            break
                cnt = 0

    def range_article(self):
        #t1 = datetime.now()

        #data['time label'] = [(t1 - datetime.strptime(data.loc[i, '날짜'], '%Y-%m-%d')).days >= days for i in
        #                      range(len(data))]
        #data = data[data['time label'] == False]
        data = self.data.loc[:, ['날짜', '제목', '링크']]

        cnt = 0
        for idx in range(30):
            try:
                if idx <= 30:
                    st.markdown(f'({data.iloc[idx,0]}) [{data.iloc[idx,1].replace("[","").replace("]","")}]({data.iloc[idx,2]})')
            except:
                break

        expanders = st.expander("See explanation")
        for idx in range(30,len(data)):
            expanders.markdown(f'({data.iloc[idx,0]}) [{data.iloc[idx,1]}]({data.iloc[idx,2]})')

    def range_article_data(self,days):
        data = self.data
        t1 = datetime.now()

        data['time label'] = [(t1 - datetime.strptime(data.loc[i, '날짜'], '%Y-%m-%d')).days >= days for i in
                              range(len(data))]
        data = data[data['time label'] == False]
        data = data.loc[:, ['날짜', '제목', '링크']]
        return data



class Company():
    # 기업 정보 가져오는 함수
    def __init__(self):
        pass

    def get_company_info(self, code):  # 종목코드와 회사명을 인자로 받음
        url = f'https://finance.naver.com/item/main.naver?code={code}'

        # header 정보 받고 파싱
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
        res = requests.get(url, headers=headers)
        bs = bs4.BeautifulSoup(res.text, 'html.parser')

        table = bs.find('div', {'id': 'tab_con1'})

        total = table.find('em', {'id': '_market_sum'}).text.strip().replace('\t', '').replace('\n', '') + '억원'
        rank = table.find_all('em')[1].text + '위'
        stock = table.find_all('em')[2].text
        foreign = table.find_all('em')[5].text
        foreign_num = table.find_all('em')[6].text
        foreign_rate = table.find_all('em')[7].text
        opinion = table.find('span', {'class': 'f_up'}).text
        goal = table.find_all('em')[9].text
        high52 = table.find_all('em')[10].text
        low = table.find_all('em')[11].text
        # PER - 추가사항
        per = table.find_all('em')[12].text + '배'
        # EPS - 추가사항
        eps = table.find_all('em')[13].text + '원'

        # 데이터프레임으로 작성
        # df = pd.DataFrame([total, rank, stock, foreign, foreign_num, foreign_rate, opinion, goal, high52, low],
        #               index = ['시가총액','시가총액순위','상장주식수','외국인한도주식수','외국인보유주식수','외국인소진율','투자의견','목표주가','52주최고','최저'])
        # df.columns = [f'{company}']

        return total, rank, stock, foreign, foreign_num, foreign_rate, opinion, goal, high52, low, per, eps
        # return df

    def get_company_info_df(self, comp, total, rank, stock, foreign, foreign_num, foreign_rate, goal, high52, low, per,
                            eps):
        comp_df1 = pd.DataFrame({
            '시가총액': [f'{total:^20}'],
            '시가총액순위': [f'{rank:^20}'],
            '상장주식수': [f'{stock:^20}']}, index=[f'{comp}'])
        comp_df2 = pd.DataFrame({
            '외국인한도주식수(A)': [f'{foreign:^20}'],
            '외국인보유주식수(B)': [f'{foreign_num:^20}'],
            '외국인소진율(B/A)': [f'{foreign_rate:^20}']}, index=[f'{comp}'])
        comp_df3 = pd.DataFrame({
            '목표주가': [f'{goal:^20}'],
            '52주최고': [f'{high52:^20}'],
            '최저': [f'{low:^20}']}, index=[f'{comp}'])
        comp_df4 = pd.DataFrame({
            'PER': [f'{per:^30}'],
            'EPS': [f'{eps:^30}']}, index=[f'{comp}'])

        return comp_df1.style.set_properties(**{'background-color': '#898EA2',
                                                'color': 'white',
                                                'border-color': '#35455C',
                                                'text-align': 'center'}), comp_df2.style.set_properties(
            **{'background-color': '#898EA2',
               'color': 'white',
               'border-color': '#35455C',
               'text-align': 'center'}), comp_df3.style.set_properties(**{'background-color': '#898EA2',
                                                                          'color': 'white',
                                                                          'border-color': '#35455C',
                                                                          'text-align': 'center'}), comp_df4.style.set_properties(
            **{'background-color': '#898EA2',
               'color': 'white',
               'border-color': '#35455C',
               'text-align': 'center'})
                                                                          
    def get_company_class(self, code='035720'):
        url = f'https://comp.kisline.com/hi/HI0100M010GE.nice?stockcd={code}&nav=1'
        
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
        res = requests.get(url, headers = headers)
        bs = bs4.BeautifulSoup(res.text, 'html.parser')
        
        # 회사등급 정보 테이블
        table = bs.find('div', {'class': 'grade'})
        class_tab = table.findAll('article')
        opinion = table.find('ul') 
        opinion = opinion.findAll('li')

        # 회사채등급
        bond_rate = class_tab[0].text.strip()

        # 기업어음등급 commercial paper
        cp = class_tab[1].text.strip()

        # 현금흐름등급 cash flow
        cf = class_tab[2].text.strip()

        # AI 등급
        ai = class_tab[3].text.strip()
        
        # 등급 의견
        bond_op = opinion[0].text.split('등급정의')[1]
        cp_op = opinion[1].text.split('등급정의')[1]
        cf_op = opinion[2].text.split('등급정의')[1]
        ai_op = opinion[3].text.split('등급정의')[1]

        c_list = [bond_rate, cp, cf, ai]
        class_list = ['회사채등급', '기업어음등급', '현금흐름등급', 'AI등급']
        class_info = [] # 기업등급 
        date = [] # 재무기준일
        date2 = [] # 평가일
        organ = [] # 평가기관

        for info, class_name in zip(c_list, class_list): # 등급 정보 담기
            try:
                class_info.append(info.split(f'{class_name}')[1].split('재')[0])
            except:
                class_info.append('-')
        for info in c_list: # 재무기준일 담기
            try:
                date.append(info.split('재무기준일')[1].split('평')[0])
            except:
                date.append('-')
        for info in c_list: # 평가일 담기
            try:
                date2.append(info.split('평가일')[1].split('평')[0])
            except:
                date2.append('-')
        for info in c_list: # 평가기관 담기
            try:
                organ.append(info.split('평가기관')[1].split()[0])
            except:
                organ.append('-')

        class_df = pd.DataFrame(columns = ['등급', '재무기준일','평가일','평가기관', '상세설명'], index = class_list)
        class_df['등급'] = class_info
        class_df['재무기준일'] = date
        class_df['평가일'] = date2
        class_df['평가기관'] = organ
        class_df['상세설명'] = [bond_op, cp_op, cf_op, ai_op]
        
        return class_df.style.set_properties(**{'background-color': '#898EA2',
                                                'color': 'white',
                                                'border-color': '#35455C',
                                                'text-align': 'center'})
        
    def get_company_summary(self, code = '035720'):
        url = f'https://comp.kisline.com/hi/HI0100M010GE.nice?stockcd={code}&nav=1'
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
        res = requests.get(url, headers = headers)
        bs = bs4.BeautifulSoup(res.text, 'html.parser')
        table = bs.find_all('section',{'class':'con'})
        title = table[6].find('thead',{'class':'aln_l'})
        summ_title = title.find_all('th')[0].text # 개요 제목
        pres_title = title.find_all('th')[1].text # 현황 제목
        
        content = table[6].find('tbody')
        summ_content = content.find_all('td')[0].text.strip().split('.')[:-1]
        pres_content = content.find_all('td')[1].text.strip().split('.')[:-1]
        
        # 데이터 프레임 만들기
        summ_df = pd.DataFrame()
        summ_df[f'{summ_title}'] = summ_content
        summ_df[f'{pres_title}'] = pres_content
        
        return summ_title, pres_title, summ_content, pres_content
    
    
    def get_consensus(self, code = '035720'):
        url = f'https://comp.kisline.com/cn/CN0100M010GE.nice?stockcd={code}&nav=5'
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
        res = requests.get(url, headers = headers)
        bs = bs4.BeautifulSoup(res.text, 'html.parser')
        table = bs.find_all('div',{'class','tbl'})[11]
        table = table.find('tbody', {'class':'aln_r'})
        lines = table.find_all('tr')

        info = []
        for i in range(0, len(lines)):
            text = re.sub(r'\(\s[0-9]\.0\)', '', lines[i].text.strip())
            info.append(text.split(' '))
            
        op_df = pd.DataFrame(columns = ['기관명','추정일자','적정주가','직전적정주가','증감률','투자의견','직전투자의견'])

        for idx in range(0, len(info)):
            op_df.loc[idx] = info[idx]
        op_df = op_df.set_index('기관명')
        
        return op_df.style.set_properties(**{'background-color': '#898EA2',
                                                'color': 'white',
                                                'border-color': '#35455C',
                                                'text-align': 'center'})
class Prediction():
    def __init__(self,company): # input : classifier,features
        my_client = MongoClient('mongodb://18.181.49.139:27017')
        self.mydb = my_client['final_project']
        self.basic_numeric = pd.DataFrame(self.mydb[f'{company}_all'].find()).drop(['_id'],axis=1)
        self.numeric = self.basic_numeric.loc[:len(self.basic_numeric),['vix','코스피','코스닥','개인매수량',
                                                                         '기관합계매수량','외국인합계매수량','score1', 'score2','score3','등락률']]
        self.numeric = self.numeric.astype('float64')

        self.pred_target =self.basic_numeric.iloc[-1,:]
        # df 모양
        label_list = list(self.numeric['등락률'])
        tp = []

        for i in label_list:
            if i > 0:
                tp.append(1)
            else:
                tp.append(0)
        self.label = pd.DataFrame(tp)
        self.company = company
        
    # bundle(dtc(),)
    def bundle(self, classifier, features, test_size):

        total_tbl_train = self.numeric.loc[:, features]
        total_tbl_label = self.label.iloc[:, 0]

        X_train, X_test, y_train, y_test = train_test_split(total_tbl_train
                                                            , total_tbl_label
                                                            , test_size=test_size,
                                                            random_state=10)

        #DecisionTree = DecisionTreeClassifier(random_state=10)
        #Logistic = LogisticRegression(random_state=10)
        #KNeighbors = KNeighborsClassifier(n_neighbors=4)
        #Voting = VotingClassifier(estimators=[('LR', Logistic), ('KN', KNeighbors)], voting='hard')
        #RandomForest = RandomForestClassifier(random_state=10)
        #GradientBoosting = GradientBoostingClassifier(random_state=10)
        #XGB = xgb.XGBClassifier(random_state=10)
        #choice = {'DecisionTree': self.dtc(), 'Logistic': Logistic, 'KNeighbors': KNeighbors,
        #          'Voting': Voting, 'RandomForest': RandomForest, 'GradientBoosting': GradientBoosting,
        #          'XGB': XGB}

        clf = classifier
        clf.fit(X_train, y_train)  # classifier
        acc_pred = clf.predict(X_test)
        acc = np.round(accuracy_score(y_test, acc_pred), 4)

        pred = clf.predict(np.array(self.pred_target[features]).reshape(1,-1))
        if int(pred) == 1:
            st.success(f'데이터는 {datetime.strftime((datetime.now()).date()-timedelta(days=1), "%Y-%m-%d")} 까지의 데이터 입니다. 오늘 {self.company} 주가는 상승할것으로 예측됩니다. 예측 정확도는 {round(acc * 100, 2)}% 입니다.')
        elif int(pred) == 0:
            st.success(f'데이터는 {datetime.strftime((datetime.now()).date()-timedelta(days=1), "%Y-%m-%d")} 까지의 데이터 입니다. 오늘 {self.company} 주가는 하락할것으로 예측됩니다. 예측 정확도는 {round(acc * 100, 2)}% 입니다.')
        
        return round(acc * 100, 2),pred

    def dtc(self,max_depth,min_samples_leaf,min_samples_split):

        return DecisionTreeClassifier(random_state=10,
                                      max_depth=max_depth,
                                      min_samples_leaf=min_samples_leaf,
                                      min_samples_split=min_samples_split)

    def logi(self,l1_ratio):
        return LogisticRegression(random_state=10,penalty='elasticnet',l1_ratio=l1_ratio,solver='saga')

    def kNN(self,n_neighbors):
        return KNeighborsClassifier(n_neighbors=n_neighbors)

    def Vote(self):
        return VotingClassifier(estimators=[('LR', self.logi(0.5)), ('KN', self.kNN(4))])

    def RanF(self,max_depth,min_samples_leaf,min_samples_split,max_samples):
        return RandomForestClassifier(random_state=10,
                                      max_depth=max_depth,
                                      min_samples_leaf=min_samples_leaf,
                                      min_samples_split=min_samples_split,
                                      bootstrap=True,
                                      max_samples=max_samples)

    def GradB(self,max_depth,min_samples_leaf,min_samples_split,learning_rate):
        return GradientBoostingClassifier(random_state=10,
                                          max_depth=max_depth,
                                          min_samples_leaf=min_samples_leaf,
                                          min_samples_split=min_samples_split,
                                          learning_rate=learning_rate)

    def xgB(self):
        return xgb.XGBClassifier(random_state=10)
    
class visualization():

    def __init__(self):
        pass

    def volume(self,code):
        # 매매동향 데이터
        try:
            pykrx_df = stock.get_market_trading_volume_by_investor(
                fromdate=datetime.strftime(
                    (datetime.now()-timedelta(days=1)).date(), '%Y-%m-%d'),
                todate=datetime.strftime(
                    (datetime.now()).date(), '%Y-%m-%d'),
                ticker=code)
        except:
            pykrx_df = stock.get_market_trading_volume_by_investor(
                fromdate=datetime.strftime(
                    (datetime.now() - timedelta(days=2)).date(), '%Y-%m-%d'),
                todate=datetime.strftime(
                    (datetime.now() - timedelta(days=1)).date(), '%Y-%m-%d'),
                ticker=code)

        pykrx_df = pykrx_df.loc[['기관합계','개인','외국인'],'순매수']
        # 기타법인,기타외국인 제외
        x = pykrx_df.index
        fig, ax = plt.subplots(facecolor="#9aa6bc")
        ax = plt.bar(x,pykrx_df)
        plt.ylabel('volume')
        st.pyplot(fig)

    def mean_price(self,code):
        try:
            pykrx_df = stock.get_market_ohlcv_by_date(
                fromdate=datetime.strftime(
                    (datetime.now()-timedelta(days=365)).date(), '%Y-%m-%d'),
                todate=datetime.strftime(
                    (datetime.now()).date(), '%Y-%m-%d'),
                ticker=code,
                adjusted=False)
        except:
            pykrx_df = stock.get_market_ohlcv_by_date(
                fromdate=datetime.strftime(
                    (datetime.now() - timedelta(days=366)).date(), '%Y-%m-%d'),
                todate=datetime.strftime(
                    (datetime.now() - timedelta(days=1)).date(), '%Y-%m-%d'),
                ticker=code,
                adjusted=False)

        x = pykrx_df.index
        fig, ax = plt.subplots(facecolor="#9aa6bc")
        plt.plot(x, pykrx_df['종가'], color='#5d81df')
        plt.plot(x, pykrx_df['종가'].rolling(window=20).mean(), color='#fdaaf8')
        plt.plot(x, pykrx_df['종가'].rolling(window=60).mean(), color='#58e4da')  # acc9b7 연두
        plt.plot(x, pykrx_df['종가'].rolling(window=120).mean(), color='#feff0f')



        plt.grid()
        plt.xlabel('day')
        plt.ylabel('price')
        plt.legend(['Close','20days','60days','120days'])

        st.pyplot(fig)

    def price(self,code):
        try:
            pykrx_df = stock.get_market_ohlcv_by_date(
                fromdate=datetime.strftime(
                    (datetime.now()-timedelta(days=365)).date(), '%Y-%m-%d'),
                todate=datetime.strftime(
                    (datetime.now()).date(), '%Y-%m-%d'),
                ticker=code,
                adjusted=False)
        except:
            pykrx_df = stock.get_market_ohlcv_by_date(
                fromdate=datetime.strftime(
                    (datetime.now() - timedelta(days=366)).date(), '%Y-%m-%d'),
                todate=datetime.strftime(
                    (datetime.now() - timedelta(days=1)).date(), '%Y-%m-%d'),
                ticker=code,
                adjusted=False)

        x = pykrx_df.index
        fig, ax = plt.subplots(facecolor="#9aa6bc")
        ax = plt.plot(x, pykrx_df['종가'])

        plt.grid()
        plt.xlabel('day')
        plt.ylabel('price')

        st.pyplot(fig)
        

class deeplearning():
    def __init__(self):
        my_client = MongoClient('mongodb://18.181.49.139:27017')
        self.mydb = my_client['final_project']

    def get_data(self, comp):
        data = pd.DataFrame(self.mydb[f'{comp}_all'].find()).drop('_id',axis=1)
        data.set_index("날짜",inplace=True)
        data_idx = data.index
        return data, data_idx

    def min_max(self, data, features, labels):
        feature_scaler = MinMaxScaler()
        label_scaler = MinMaxScaler()
        ms_feaures = feature_scaler.fit_transform(data[features])
        ms_label = label_scaler.fit_transform(data[labels].values.reshape(-1,1))
        df_ms_feaures = pd.DataFrame(ms_feaures, columns=features)
        df_ms_labels = pd.DataFrame(ms_label, columns=labels)

        return df_ms_feaures, df_ms_labels, label_scaler

    def make_dataset(self, data, label, window_size=20):
        feature_list = []
        label_list = []
        for i in range(len(data) - window_size):
            feature_list.append(np.array(data.iloc[i:i+window_size]))
            label_list.append(np.array(label.iloc[i+window_size]))
        return np.array(feature_list), np.array(label_list)

    def lstm_model(self,data,idx,feature,label,train,epoch,batch,sequence,act,opt):
        tf.random.set_seed(56)
        data_feature, data_label, label_scaler = self.min_max(data,feature,label)
        train_feature, train_label= self.make_dataset(data_feature[:train],data_label[:train],sequence)
        test_feature, test_label = self.make_dataset(data_feature[train:],data_label[train:],sequence)
        x_train, x_valid, y_train, y_valid = train_test_split(train_feature, train_label, test_size=0.2,random_state=56)
        model = Sequential()
        model.add(LSTM(32,
                    input_shape=(train_feature.shape[1], train_feature.shape[2]),
                    activation=act,
                    return_sequences=False)
                )
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer=opt, metrics=["mean_squared_error"])
        history = model.fit(x_train, y_train, 
                            epochs=epoch, 
                            batch_size=batch,
                            validation_data=(x_valid, y_valid))

        pred_test = model.predict(test_feature)

        # rescaled
        # 실제값
        rescaled_actual = data[label].iloc[-len(test_label):]
        # 예측값
        rescaled_pred = label_scaler.inverse_transform(np.array(pred_test).reshape(-1,1))
        idx = list(idx)
        df = pd.DataFrame(rescaled_pred,columns=["종가"])
        df.index = idx[train+sequence:]
        # 내일예측값
        data_tm = []
        data_tm.append(np.array(data_feature.iloc[-sequence:]))
        data_tm = np.array(data_tm)
        pred_price = model.predict(data_tm)
        rescaled_pred_price = label_scaler.inverse_transform(np.array(pred_price).reshape(-1,1))
        predict_price = rescaled_pred_price[0][0]
        
        c_rate = predict_price/df["종가"].iloc[-1]
        c_price = rescaled_actual.iloc[-1] * c_rate
        rate = (c_rate * 100) - 100
        return rescaled_actual, df, int(round(c_price,-2)), np.round(rate,2)

    def gru_model(self,data,idx,feature,label,train,epoch,batch,sequence,act,opt):
        tf.random.set_seed(56)
        data_feature, data_label, label_scaler = self.min_max(data,feature,label)
        train_feature, train_label= self.make_dataset(data_feature[:train],data_label[:train],sequence)
        test_feature, test_label = self.make_dataset(data_feature[train:],data_label[train:],sequence)
        x_train, x_valid, y_train, y_valid = train_test_split(train_feature, train_label, test_size=0.2,random_state=56)
        model = Sequential()
        model.add(GRU(32,
                    input_shape=(train_feature.shape[1], train_feature.shape[2]),
                    activation=act,
                    return_sequences=False)
                )
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer=opt, metrics=["mean_squared_error"])
        history = model.fit(x_train, y_train, 
                            epochs=epoch, 
                            batch_size=batch,
                            validation_data=(x_valid, y_valid))

        pred_test = model.predict(test_feature)

        # rescaled
        # 실제값
        rescaled_actual = data[label].iloc[-len(test_label):]
        # 예측값
        rescaled_pred = label_scaler.inverse_transform(np.array(pred_test).reshape(-1,1))
        idx = list(idx)
        df = pd.DataFrame(rescaled_pred,columns=["종가"])
        df.index = idx[train+sequence:]
        # 내일예측값
        data_tm = []
        data_tm.append(np.array(data_feature.iloc[-sequence:]))
        data_tm = np.array(data_tm)
        pred_price = model.predict(data_tm)
        rescaled_pred_price = label_scaler.inverse_transform(np.array(pred_price).reshape(-1,1))
        predict_price = rescaled_pred_price[0][0]
        
        c_rate = predict_price/df["종가"].iloc[-1]
        c_price = rescaled_actual.iloc[-1] * c_rate
        rate = (c_rate * 100) - 100
        return rescaled_actual, df, int(round(c_price,-2)), np.round(rate,2)

    def make_graph(self, act, pred):
        fig, ax = plt.subplots(facecolor="#9aa6bc")
        ax = plt.plot(act, label='실제 주가')
        ax = plt.plot(pred, label='예측 주가')
        plt.rc('font',family = 'Malgun Gothic')
        plt.xlabel(xlabel="날짜",size = 8)
        plt.ylabel(ylabel="가격",size = 8)
        plt.xticks(range(0,len(act),int(len(act)/10)), rotation = 30, size = 7)
        plt.yticks(size=6)
        plt.legend()
        st.pyplot(fig)

    def do_predict(self,act,pred):
        rmse = np.sqrt(mean_squared_error(act,pred))
        r2 = r2_score(act,pred)
        return np.round(rmse,2), np.round(r2,2)
    
class feargreed():
    def __init__(self, comp):
        my_client = MongoClient('mongodb://18.181.49.139:27017')
        mydb = my_client['final_project']
        if comp == '카카오':
            df = pd.DataFrame(mydb['kakao_feargreed'].find({})).drop('_id',axis=1)
        else:
            df = pd.DataFrame(mydb['naver_feargreed'].find({})).drop('_id',axis=1)
            
        df['날짜'] = pd.to_datetime(df['날짜'])
        
        df = df.sort_values(by='날짜', ascending=False).reset_index(drop=True)
        
        df['공포탐욕'] = df['BERT'] + df['LSTM']
        df['공포탐욕'] = df['공포탐욕'] - df['공포탐욕'].mean()
        self.df = df
        self.df_fg = (df[['날짜','공포탐욕']].groupby('날짜').mean().rolling(7).mean()*100).dropna()
        self.df_lb = (df[['날짜','LSTM','BERT']].groupby('날짜').mean().rolling(7).mean()*100-50).dropna() 
        
    def load_img(self,day):
        x = self.df_fg['공포탐욕'][day.isoformat()]
        if x >= 5:
            chk = 4
        elif 5 > x >= 0:
            chk = 3
        elif 0 > x >= -3:
            chk = 2
        else:
            chk = 1
        return Image.open(f'data/feargreed_{chk}.png')

    def get_comments(self,day):
        df = self.df
        greed_comments = df[df['날짜'] == day.isoformat()].sort_values(by='공포탐욕')['댓글'].head(7).to_list()
        fear_comments = df[df['날짜'] == day.isoformat()].sort_values(by='공포탐욕')['댓글'].tail(7).to_list()
        return fear_comments, greed_comments
    
    def get_period_df(self,period_check):
        period_dict = {'1주':2, '2주':3, '1개월':5, '3개월':13, '6개월':25, '1년':52}
        day = (date.today() - timedelta(weeks=period_dict[period_check])).isoformat()
        df2, df3 = self.df_fg, self.df_lb
        df2, df3 = df2[df2.index >= day], df3[df3.index >= day]
        return df2, df3
    
    def get_fg_score(self,day):
        def chk_fg(x):
            if x >= 5:
                return '매우 탐욕'
            elif 5 > x >= 0:
                return '탐욕'
            elif 0 > x >= -3:
                return '공포'
            else:
                return '매우 공포'
        df2 = self.df_fg    
        x = df2[df2.index >= (date.today()-timedelta(days=day)).isoformat()]['공포탐욕'].mean()
        return chk_fg(x), f': {round(x,2)}점'

#my_client = MongoClient('mongodb://localhost:27017')
#mydb = my_client['final_project']
#pd.DataFrame(mydb['kakao_score'].find())
