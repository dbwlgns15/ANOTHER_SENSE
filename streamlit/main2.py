import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import datetime

st.set_page_config(page_title = 'Ants MIND', layout="wide")

st.experimental_set_query_params(TEAM=['AnotherSense'],Project=['AntsMIND'])

st.sidebar.subheader(':sparkles: Team Another Sense :sunglasses:')

comp = st.sidebar.selectbox('🏢 회사를 선택해주세요. ',('NAVER', '카카오'))

option = st.sidebar.selectbox('열람할 페이지를 선택해주세요.',('메인 홈 Main Home', '기업정보 Company Information', '개미 동향 Ants MIND','기사 News','예측 Prediction'))

if option == '개미 동향 Ants MIND':
    op_emoji = ':ant:'
    st.sidebar.subheader(f'{op_emoji} {option} 페이지입니다')
    st.write(f'# :cupid: {comp} 공포/탐욕 지수')

    if comp == '카카오':
        df = pd.read_csv('./score_kakao.csv')
    else:
        df = pd.read_csv('./score_naver.csv')
    df['날짜'] = pd.to_datetime(df['날짜'])
    df2 = df.copy()
    df['공포탐욕'] = df['BERT'] + df['LSTM']
    df['공포탐욕'] = df['공포탐욕'] - df['공포탐욕'].mean()
    df = df[['날짜','공포탐욕']]
    df = (df.groupby('날짜').mean().rolling(7).mean()*100).dropna()
    df2 = (df2.groupby('날짜').mean().rolling(7).mean()*100-50).dropna() 
    
    col1, col2 = st.columns([1, 2])
    d = col1.date_input("공포탐욕지수가 궁금한 날을 입력해주세요."
    ,value=datetime.date.today()
    ,min_value=datetime.date.today() - datetime.timedelta(days=365)
    ,max_value=datetime.date.today())
    x = df['공포탐욕'][d.isoformat()]
    if x >= 5:
        chk = 4
    elif 5 > x >= 0:
        chk = 3
    elif 0 > x >= -3:
        chk = 2
    else:
        chk = 1
    image = Image.open(f'./img/{chk}.png')
    col1.image(image)
    

    col3, col4 = st.columns([1, 3])
    period_check = col3.select_slider('기간 설정',
    options=['1주', '2주' ,'1개월', '3개월', '6개월', '1년'])
    period_dict = {'1주':2, '2주':3, '1개월':5, '3개월':13, '6개월':25, '1년':52}
    day = (datetime.date.today() - datetime.timedelta(weeks=period_dict[period_check])).isoformat()

    col4.line_chart(df[df.index >= day],height=300)
    col4.line_chart(df2[df2.index >= day],height=300)