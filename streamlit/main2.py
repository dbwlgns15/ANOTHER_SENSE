import streamlit as st
import pandas as pd
import numpy as np
import datetime

# 웹페이지 기본 설정
st.set_page_config(page_title = 'Ants MIND', layout="wide")
# 웹주소 설정
st.experimental_set_query_params(TEAM=['AnotherSense'],Project=['AntsMIND'])

st.sidebar.subheader(':sparkles: Team Another Sense :sunglasses:')
# 사이드바1 - 회사 선택 (최상위 선택지)
comp = st.sidebar.selectbox('🏢 회사를 선택해주세요. ',('NAVER', '카카오')) # comp = 기업이름

if comp == '카카오':
    codenum = '035720'
else:
    codenum = '035420'

option = st.sidebar.selectbox('열람할 페이지를 선택해주세요.',('메인 홈 Main Home', '기업정보 Company Information', '개미 동향 Ants MIND','기사 News','예측 Prediction'))

if option == '개미 동향 Ants MIND':
    op_emoji = ':ant:'
    st.sidebar.subheader(f'{op_emoji} {option} 페이지입니다')
    st.write(f'# :cupid: {comp} 개미 투자자 심리')

    ant_col1, ant_col2 = st.columns(2)
    ant_col1.write('시험용')
    ant_col1.write("사람의 마음")
    
    period_check = st.select_slider('공포탐욕지수 차트 기간 설정',
    options=['1주', '2주' ,'1개월', '3개월', '6개월', '1년'])
    period_dict = {'1주':2,'2주':3,'1개월':5,'3개월':13,'6개월':25,'1년':52}
    day = (datetime.date.today() - datetime.timedelta(weeks=period_dict[period_check])).isoformat()

    if comp == '카카오':
        df = pd.read_csv('./score_kakao.csv')
    else:
        df = pd.read_csv('./score_naver.csv')
    df['날짜'] = pd.to_datetime(df['날짜'])
    df = df[df['날짜'] >= day]
    df = df.groupby('날짜').mean().rolling(7).mean()*100
    df = df.dropna()
    st.line_chart(df,height=300)