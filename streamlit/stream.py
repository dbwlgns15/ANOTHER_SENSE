import streamlit as st
import function

today = function.get_today()
st.header('ANT MIND')
st.sidebar.header(f'{today}')
symbol = st.sidebar.text_input('주식종목이름을  입력해주세요.')

with st.spinner(f'{symbol}의  공포탐욕지수를  분석중입니다...'):
    fg,wc = function.get_feargreed_wordcloud(symbol)

if fg:
    st.write(f'{symbol}의  공포탐욕지수:  {fg}')
else:
    st.write('주식종목이름을  다시  확인해주세요.')

st.write(f'가장 자주 등장한 상위 단어 5개:  ',wc)
