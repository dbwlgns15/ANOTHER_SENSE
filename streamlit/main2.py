import streamlit as st
from datetime import date, timedelta
from PIL import Image
import execute2

st.set_page_config(page_title = 'Ants MIND', layout="wide")

comp = st.sidebar.selectbox('회사를 선택해주세요. ',('NAVER', '카카오'))

op_emoji = ':ant:'
st.write(f'# :cupid: {comp} 공포/탐욕 지수')

feargreed = execute2.feargreed(comp)

col1, col2, col3 = st.columns([1, 1, 1])

input_day = col1.date_input("공포탐욕지수가 궁금한 날을 입력해주세요."
    ,value=feargreed.df['날짜'][0]
    ,min_value=feargreed.df['날짜'][0] - timedelta(days=365)
    ,max_value=feargreed.df['날짜'][0])

col1.image(feargreed.load_img(input_day))

fear_comments, greed_comments = feargreed.get_comments(input_day)
col2.write("#### 공포댓글")
for comment in greed_comments:
    col2.text(comment)
col3.write("#### 탐욕댓글")
for comment in fear_comments:
    col3.text(comment)

col4, col5 = st.columns([1, 4])

period_check = col4.select_slider('기간 설정', options=['1주', '2주' ,'1개월', '3개월', '6개월', '1년'])

with col4.expander("오늘 공포탐욕지수"):
    st.write(feargreed.get_fg_score(0)[0],feargreed.get_fg_score(0)[1])
with col4.expander("어제 공포탐욕지수"):
    st.write(feargreed.get_fg_score(1)[0],feargreed.get_fg_score(1)[1])
with col4.expander("지난 한주 공포탐욕지수"):
    st.write(feargreed.get_fg_score(7)[0],feargreed.get_fg_score(7)[1])
with col4.expander("지난 한달 공포탐욕지수"):
    st.write(feargreed.get_fg_score(30)[0],feargreed.get_fg_score(30)[1])

period_df = feargreed.get_period_df(period_check)
col5.line_chart(period_df[0],height=250)
col5.line_chart(period_df[1],height=250)

with st.expander("공포탐욕지수 측정 방법"):
    flow_img = Image.open('./data/feargreed_flow.png')
    st.image(flow_img)
    st.write('''
    #### LSTM 모델 \n
    네이버 종목토론실 댓글은 레이블링이 되어있지 않는 비정형데이터입니다. 모델 학습에는 레이블링이 필요하기 때문에, 
    공포탐욕사전을 만들어서 단어의 빈도수를 분석하여 레이블링을 진행하였습니다. (ex 망했다:공포, 가즈아:탐욕)
    이렇게 생성된 학습데이터를 통해서 LSTM모델을 학습하고, 댓글의 공포탐욕지수를 분석했습니다. \n
    #### BERT 모델 \n
    사전학습된 BERT(bert-base-multilingual-cased)모델을 네이버 영화 리뷰 댓글(nsmc)로 Fine-Tuning을 통해 미세조정을 거쳐서
    학습하고, 댓글의 공포탐욕지수를 분석했습니다. \n
    #### 공포탐욕지수 산출식
    ''')
    st.latex(r'LstmScore = S_{l} \big(0 \leq S_{l} \leq 1 \big)')
    st.latex(r'BertScore = S_{b} \big(0 \leq S_{b} \leq 1 \big)')
    st.latex(r'DayCount = N')
    st.latex(r'Score = \big(S_{l}+S_{b}-\frac{\sum \big(S_{l}+S_{b}\big)}{N} \big) \times 100')

    st.latex(r'예측등락률 = \frac{내일의 예측가}{오늘의 예측가}')
    st.latex(r'보정가격 = 오늘의 실제가 \times 예측등락률')