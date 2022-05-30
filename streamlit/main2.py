import streamlit as st
import pandas as pd
import numpy as np

# 웹페이지 기본 설정
st.set_page_config(page_title = 'Ants MIND', layout="wide")

# 웹주소 설정
st.experimental_set_query_params(
     TEAM=['AnotherSense'],
     Project=['AntsMIND']
)

st.sidebar.subheader(':sparkles: Team Another Sense :sunglasses:')
# 사이드바1 - 회사 선택 (최상위 선택지)
comp = st.sidebar.selectbox('🏢 회사를 선택해주세요. ',
                 ('NAVER', '카카오')) # comp = 기업이름

if comp == '카카오':
    codenum = '035720'
else:
    codenum = '035420'

option = st.sidebar.selectbox(
    '열람할 페이지를 선택해주세요.',
    ('메인 홈 Main Home', '기업정보 Company Information', '개미 동향 Ants MIND','기사 News','예측 Prediction')
)

if option == '개미 동향 Ants MIND': ## fear&greed와 댓글 분석 페이지
    op_emoji = ':ant:'
    st.sidebar.subheader(f'{op_emoji} {option} 페이지입니다')
    st.write(f'''
             # :cupid: {comp} 개미 투자자 심리
             ''')
    ant_col1, ant_col2 = st.columns(2)
    
    ant_col1.write('# 시험용')
    ant_col1.write("> 사람의 마음")

    df = pd.read_csv('./score_kakao.csv')
    df['날짜'] = pd.to_datetime(df['날짜'])
    st.line_chart(df.groupby('날짜').mean().rolling(7).mean().round(2)*100,height=300)
    st.line_chart((0.5+(df.groupby('날짜').mean()['LSTM']-0.5)*(1+df.groupby('날짜').mean()['BERT'])).rolling(7).mean().round(2)*100,height=300)
    st.line_chart(((df.groupby('날짜').mean()['BERT']+df.groupby('날짜').mean()['LSTM'])/2).rolling(7).mean().round(2)*100,height=300)