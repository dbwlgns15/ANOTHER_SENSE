import streamlit as st
import pandas as pd
from datetime import datetime,timedelta
import bs4
import requests
from pykrx import stock
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from pymongo import MongoClient


from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression # 앙상블 조합용
from sklearn.neighbors import KNeighborsClassifier # 앙상블 조합용
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
import xgboost as xgb


@st.cache(suppress_st_warning=True)

# 사용된 데이터 csv는 데이터 폴더로 축적
# 추후 몽고 연동
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
        url = f'https://finance.naver.com/item/main.naver?code={comp_code}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}

        res = requests.get(url, headers=headers)
        bs_obj = bs4.BeautifulSoup(res.text)
        today = bs_obj.find_all('p', {'class': 'no_today'})
        exday = bs_obj.find_all('p', {'class': 'no_exday'})
        temp0 = [i.text for i in today][0].split('\n')
        temp = [i.text for i in exday][0].split('\n')

        with st.sidebar:
            st.metric(label=comp,
                value=f"{temp0[2]} 원",
                delta=f'{temp[5]} ({temp[-4]}%)',
                delta_color='off')

    def sidebar_price_widget(self):
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

class Article():
    def __init__(self,company,day):
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

    def range_article(self,days):
        data = self.data
        #t1 = datetime.now()

        #data['time label'] = [(t1 - datetime.strptime(data.loc[i, '날짜'], '%Y-%m-%d')).days >= days for i in
        #                      range(len(data))]
        #data = data[data['time label'] == False]
        data = data.loc[:, ['날짜', '제목', '링크']]

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

class Prediction():
    def __init__(self,company): # input : classifier,features
        self.basic_numeric = pd.DataFrame(mydb[f'basic_numeric_{company}'].find()).drop(['_id','date'],axis=1)
        self.numeric = self.basic_numeric.iloc[:len(self.basic_numeric),:]
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


    def bundle(self, classifier, features, test_size, random):

        DecisionTree = DecisionTreeClassifier(random_state=10)
        Logistic = LogisticRegression(random_state=10)
        KNeighbors = KNeighborsClassifier(n_neighbors=4)
        Voting = VotingClassifier(estimators=[('LR', Logistic), ('KN', KNeighbors)], voting='hard')
        RandomForest = RandomForestClassifier(random_state=10)
        GradientBoosting = GradientBoostingClassifier(random_state=10)
        XGB = xgb.XGBClassifier(random_state=10)

        total_tbl_train = self.numeric.loc[:, features]
        total_tbl_label = self.label.iloc[:, 0]

        X_train, X_test, y_train, y_test = train_test_split(total_tbl_train
                                                            , total_tbl_label
                                                            , test_size=test_size,
                                                            random_state=random)
        choice = {'DecisionTree':DecisionTree,'Logistic':Logistic,'KNeighbors':KNeighbors,
                  'Voting':Voting,'RandomForest':RandomForest,'GradientBoosting':GradientBoosting,
                  'XGB':XGB}

        if classifier:

            clf = choice[classifier]
            clf.fit(X_train, y_train)  # classifier
            acc_pred = clf.predict(X_test)
            acc = np.round(accuracy_score(y_test, acc_pred), 4)

            pred = clf.predict(np.array(self.pred_target[features]).reshape(1,-1))
            if int(pred) == 1:
                st.success(f'다음날 주가는 상승할것으로 예측됩니다. 예측 정확도는 {round(acc * 100, 2)}% 입니다.')
            elif int(pred) == 0:
                st.success(f'다음날 주가는 하락할것으로 예측됩니다. 예측 정확도는 {round(acc * 100, 2)}% 입니다.')

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
        fig,ax = plt.subplots(facecolor="#9aa6bc")
        ax = plt.plot(x, pykrx_df['종가'],
                 x, pykrx_df['종가'].rolling(window=20).mean(),
                 x, pykrx_df['종가'].rolling(window=60).mean(),
                 x, pykrx_df['종가'].rolling(window=120).mean())

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

my_client = MongoClient('mongodb://localhost:27017')
mydb = my_client['final_project']
pd.DataFrame(mydb['kakao_score'].find())
