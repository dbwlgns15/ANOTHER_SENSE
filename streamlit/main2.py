import streamlit as st
from datetime import date, timedelta
from PIL import Image
import execute2

st.set_page_config(page_title = 'Ants MIND', layout="wide")

comp = st.sidebar.selectbox('회사를 선택해주세요. ',('NAVER', '카카오'))

option = st.sidebar.selectbox('',('개미 동향 Ants MIND',''))

if option == '개미 동향 Ants MIND':
    op_emoji = ':ant:'
    st.sidebar.subheader(f'{op_emoji} {option} 페이지입니다')
    st.write(f'# :cupid: {comp} 공포/탐욕 지수')

    feargreed = execute2.feargreed(comp)
    
    col1, col2, col3 = st.columns([1, 1, 1])

    input_day = col1.date_input("공포탐욕지수가 궁금한 날을 입력해주세요."
        ,value=feargreed.df['날짜'][0]
        ,min_value=feargreed.df['날짜'][0] - timedelta(days=365)
        ,max_value=feargreed.df['날짜'][0])

    col1.image(feargreed.load_img(input_day))

    fear_comments, greed_comments = feargreed.get_comments(input_day)
    with col2.expander("공포댓글"):
        for comment in greed_comments:
            st.write(comment)
    with col3.expander("탐욕댓글"):
        for comment in fear_comments:
            st.write(comment)
    
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
        flow_img = Image.open(f'./data/feargreed_flow.png')
        st.image(flow_img)
        st.latex(r'LSTM = S_{l} \big(0 \leq S_{l} \leq1\big)')
        st.latex(r'BERT = S_{b} \big(0 \leq S_{b} \leq1\big)')
        st.latex(r'Score = \big(S_{l}+S_{b}-\frac{\sum \big(S_{l}+S_{b}\big)}{N} \big) \times 100')