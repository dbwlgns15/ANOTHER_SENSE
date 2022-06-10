# Streamlit으로 웹서비스 구현하기 
import streamlit as st
from PIL import Image
import execute
import time
from datetime import datetime
import pandas as pd
from datetime import datetime, date, timedelta
import numpy as np

# 웹페이지 기본 설정
#st.set_page_config(page_title = 'Ants MIND', layout="wide")
im = Image.open('data/ant.png')
st.set_page_config(page_title = 'Ants MIND',page_icon=im, layout="wide",initial_sidebar_state="auto", menu_items=None)

# 웹주소 설정
st.experimental_set_query_params(
     MadeBy=['Team_AnotherSense'],
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

if comp == '카카오':
    naming = 'kakao'
else:
    naming = 'naver'

vis = execute.visualization()

# codenum = execute.get_company_code(comp) # codenum = 기업코드


# 사이드바2 - 카테고리 선택
option = st.sidebar.selectbox(
    '열람할 페이지를 선택해주세요.',
    ('메인 홈 Main Home', '기업정보 Company Information', '개미 동향 Ants MIND','기사 News','예측-분류모델 Classification Model',"예측-딥러닝모델 DeepLearning Model")
)


# 사이드바에서 선택한 카테고리에 따른 페이지뷰

# 메인 홈페이지

SideTab = execute.SideTab()


if option == '메인 홈 Main Home':
    op_emoji = ':house:'
    st.sidebar.subheader(f'{op_emoji} {option} 페이지입니다')
    SideTab.sidebar_price_now(comp,codenum)
    SideTab.sidebar_price_widget('KOSPI','1001')
    SideTab.sidebar_price_widget('KOSDAQ','2001')
    st.sidebar.subheader("krx 데이터에서 갱신됩니다.")
    
    # 메인 타이틀 Ants MIND
    st.title(':ant: Ants MIND :ant:')

    # 서브 헤더 - 팀명 Another Sense
    st.subheader(':sparkles: Team Another Sense :sunglasses:')
    st.write('') # 공백을 위한 줄바꿈
    
    img = Image.open(f'data/{comp}.png')
    st.image(img, width = 400)
    
    # 메인 홈페이지 텍스트
    st.write(f"""
             ## :house: {comp}의 메인 홈페이지 
             
             > 각 카테고리별 페이지를 소개해드릴게요!""")  
             
    comp_expand = st.expander("ℹ️ 기업정보 Company Information")         
    comp_expand.write("""
                👉 '기업정보 Company Information' 페이지에서는 내가 선택한 기업의 기본적인 정보를 얻을 수 있어요.  
                해당 기업의 __시가총액, 상장주식수, 간결한 투자의견__ 등을 확인하고 싶다면 이 페이지를 선택하여 열람해주세요!  
                """)
    ants_expand = st.expander('💘 개미 동향 Ants MIND')
    ants_expand.write("""         
                👉 '개미 동향 Ants MIND' 페이지에서는 내가 선택한 기업의 **개미 투자자 심리**를 엿볼 수 있어요.  
                OO 기업에 투자하셨다고요? 그렇다면 다른 개인 투자자들의 생각이 궁금하시겠군요! 이 페이지를 선택하여 열람해주세요!  
                """)
    news_expand = st.expander('📰 기사 News')
    news_expand.write("""         
                👉 '기사 News' 페이지에서는 내가 선택한 기업의 **각종 이슈를 보도한 기사**를 확인할 수 있어요.  
                기업 이슈는 주가와 직결되어 있는 만큼 투자자들에게 있어 큰 관심거리죠! 나의 다음 선택에 큰 도움을 줄 수 있답니다!  
                이 페이지를 선택하여 열람해주세요!  
                """)
    pred_expand = st.expander('🎯 예측 Prediction')
    pred_expand.write("""         
                👉 '예측 Prediction' 페이지에서는 내가 선택한 기업의 **미래**를 엿볼 수 있어요.  
                팀 어나더센스(Team Another Sense)에서는 다양한 데이터를 토대로 주가를 분석하여 해당 기업의 다음을 예측해보았어요. 
                궁금하시다면 이 페이지를 선택하여 열람해주세요!  
                #
                👇 __상세설명은 아래 내용 참고하기__ 👇
                
                저희가 사용한 방법은 크게 두 가지예요. 
                
                __✅ 1. 분류 모델 Classification Model__
                
               '예측 - 분류 모델 Classification Model' 페이지에서는 다음날 주가의 상승/하락을 예측하고 사용자 여러분이 ⚡직접⚡ 모델을 만들어서
                비교해볼 수 있어요!
                  
                #
                __✅ 2. 딥러닝 모델 DeepLearning Model__
                
                '예측 - 딥러닝 모델 DeepLearning Model' 페이지에서는 딥러닝 모델에 다양한 데이터를 학습시켜 다음날 주가가 
                어떤식으로 반영될지 확인하실 수 있답니다! 또한 사용자 여러분이 ⚡직접⚡ 모델을 만들어서 적용해볼 수도 있어요!
                  
                __단! 모든 예측이 항상 적중하는 것은 아니란 사실을 유념하세요! 투자의 책임은 언제나 스스로 지는 것이니까요!__          
             """)
    
        

# 개미 동향 페이지
elif option == '개미 동향 Ants MIND':
    op_emoji = ':ant:'
    st.sidebar.subheader(f'{op_emoji} {option} 페이지입니다')
    SideTab.sidebar_price_now(comp,codenum)
    SideTab.sidebar_price_widget('KOSPI','1001')
    SideTab.sidebar_price_widget('KOSDAQ','2001')
    st.sidebar.subheader("krx 데이터에서 갱신됩니다.")
    
    st.write(f'# :cupid: {comp} 공포/탐욕 지수')

    feargreed = execute.feargreed(comp)
    
    col1 ,x , col2, col3 = st.columns([3,0.5, 3, 3])

    input_day = col1.date_input("공포탐욕지수가 궁금한 날을 입력해주세요."
        ,value=feargreed.df['날짜'][0]
        ,min_value=feargreed.df['날짜'][0] - timedelta(days=365)
        ,max_value=feargreed.df['날짜'][0])

    col1.image(feargreed.load_img(input_day))

    fear_comments, greed_comments = feargreed.get_comments(input_day)
    col2.write("#### 😨 *공포댓글*")
    for comment in greed_comments:
        col2.text(comment)
    col3.write("#### 🤑 *탐욕댓글*")
    for comment in fear_comments:
        col3.text(comment)
    
    col4, col5 = st.columns([1, 4])

    period_check = col4.select_slider('기간 설정', options=['1주', '2주' ,'1개월', '3개월', '6개월', '1년'])

    with col4.expander("🔎 오늘 공포탐욕지수"):
        st.write(feargreed.get_fg_score(0)[0],feargreed.get_fg_score(0)[1])
    with col4.expander("🔎 어제 공포탐욕지수"):
        st.write(feargreed.get_fg_score(1)[0],feargreed.get_fg_score(1)[1])
    with col4.expander("🔎 지난 한주 공포탐욕지수"):
        st.write(feargreed.get_fg_score(7)[0],feargreed.get_fg_score(7)[1])
    with col4.expander("🔎 지난 한달 공포탐욕지수"):
        st.write(feargreed.get_fg_score(30)[0],feargreed.get_fg_score(30)[1])

    period_df = feargreed.get_period_df(period_check)
    col5.line_chart(period_df[0],height=250)
    col5.line_chart(period_df[1],height=250)

    with st.expander("🔎 공포탐욕지수 측정 방법"):
        # flow_img = Image.open('./data/feargreed_flow.png')
        # st.image(flow_img)
        st.write('''
        #### ✅ LSTM 모델 \n
        네이버 종목토론실 댓글은 레이블링이 되어있지 않는 비정형데이터입니다. 모델 학습에는 레이블링이 필요하기 때문에, 
        공포탐욕사전을 만들어서 단어의 빈도수를 분석하여 레이블링을 진행하였습니다. (ex 망했다:공포, 가즈아:탐욕)
        이렇게 생성된 학습데이터를 통해서 LSTM모델을 학습하고, 댓글의 공포탐욕지수를 분석했습니다. \n
        #### ✅ BERT 모델 \n
        사전학습된 BERT(bert-base-multilingual-cased)모델을 네이버 영화 리뷰 댓글(nsmc)로 Fine-Tuning을 통해 미세조정을 거쳐서
        학습하고, 댓글의 공포탐욕지수를 분석했습니다. \n
        ''')
        #st.latex(r'LstmScore = S_{l} \big(0 \leq S_{l} \leq 1 \big)')
        #st.latex(r'BertScore = S_{b} \big(0 \leq S_{b} \leq 1 \big)')
        #st.latex(r'DayCount = N')
        #st.latex(r'Score = \big(S_{l}+S_{b}-\frac{\sum \big(S_{l}+S_{b}\big)}{N} \big) \times 100')

# 관련 뉴스 페이지
elif option == '기사 News':
    op_emoji = ':newspaper:'
    # article = execute.Article()
    st.sidebar.subheader(f'{op_emoji} {option} 페이지입니다')
    SideTab.sidebar_price_now(comp,codenum)
    SideTab.sidebar_price_widget('KOSPI','1001')
    SideTab.sidebar_price_widget('KOSDAQ','2001')
    st.sidebar.subheader("krx 데이터에서 갱신됩니다.")
    
    st.title(f':newspaper: {comp} 관련 뉴스')
    st.subheader(f"내가 선택한 기업 \"{comp}\"의 🔥최신 이슈🔥들을 모아 볼 수 있어요!")

    sub_opt = st.selectbox(
        '옵션을 선택해주세요',
        ('최근 기사', '최근 언론사별 기사'))

    # if sub_opt == '오늘의 기사':
    #    article = execute.Article(comp,1)
    #    article.range_article(1)
    article = execute.Article(comp)
    if sub_opt == '최근 기사':
        article.range_article()
    else:
        article.company_article()

    st.write('You selected:', sub_opt)


    

# 기업정보 페이지
# 기업정보 페이지
elif option == '기업정보 Company Information':
    op_emoji = ':information_source:'
    st.sidebar.subheader(f'{op_emoji} {option} 페이지입니다')
    SideTab.sidebar_price_now(comp,codenum)
    SideTab.sidebar_price_widget('KOSPI','1001')
    SideTab.sidebar_price_widget('KOSDAQ','2001')
    st.sidebar.subheader("krx 데이터에서 갱신됩니다.")   
    st.write(f'''
             # :information_source: {comp} 기업정보
             ''')
    
    # 주가 그래프 
    col1, col2 = st.columns(2)
    
    with col1:
        visualization = execute.visualization()
        price_tab = visualization.mean_price(codenum)
    
    with col2:
        # 기업정보 보여주는 데이터프레임 4개
        company = execute.Company()
        total, rank, stock, foreign, foreign_num, foreign_rate, opinion, goal, high52, low, per, eps = company.get_company_info(codenum)
        comp_df, comp_df2, comp_df3, comp_df4 = company.get_company_info_df(comp, total, rank, stock, foreign, foreign_num, foreign_rate, goal, high52, low, per, eps)
        
        st.write(comp_df)
        st.write(comp_df2)
        st.write(comp_df3)
        st.write(comp_df4)    
        st.text_area('',f'> 왼쪽의 이미지는 {comp}의 주식 가격 흐름을 나타낸 표입니다. 범례에서 확인하실 수 있듯이 분홍색, 초록색, 노랑색의 세 가지 선은 각각 20일, 60일, 120일동안의 이동평균선입니다!',
                     height = 30)
        

    st.write('### 🔎 투자의견 평균')
    st.image(f'data/{opinion[4:]}.png', width = 500, caption = f'위 이미지는 기관별 투자의견 평균을 나타낸 것입니다.')
    
    # 기업 개요와 현황
    st.write(f'### 🚦 {comp} 개요 및 현황')
    summ_title, pres_title, summ_content, pres_content = company.get_company_summary(codenum)
    st.write(f'##### ✅ {summ_title}')
    for s in summ_content:
        st.write(s)
    st.write(f'##### ✅ {pres_title}')
    for p in pres_content:
        st.write(p)        
    
    
    # 기업 등급 정보 보여주는 데이터프레임
    st.write('  ')
    st.write('### 🔎 등급정보')
    st.write(company.get_company_class(codenum))
    
    # 증권사별 투자의견 보여주는 데이터프레임
    st.write('  ')
    st.write('### 🔎 기관별 투자의견')
    st.table(company.get_consensus(codenum))

# 딥러닝 페이지
elif option == "예측-딥러닝모델 DeepLearning Model":
    dl = execute.deeplearning()

    op_emoji = ':dart:'
    st.sidebar.subheader(f'{op_emoji} {option} 페이지입니다')
    SideTab.sidebar_price_now(comp,codenum)
    SideTab.sidebar_price_widget('KOSPI','1001')
    SideTab.sidebar_price_widget('KOSDAQ','2001')
    st.sidebar.subheader("krx 데이터에서 갱신됩니다.")    
    st.write(f"""
             # :dart: {comp} 주가 정보 예측 
             """)
    if comp == '카카오':
        naming = 'kakao'
    else:
        naming = 'naver'


    data,data_idx = dl.get_data(naming)
    col1, col2 = st.columns(2)
    with col1:
        clf = st.selectbox("모델 선택",("Menu","Best Model","LSTM","GRU"))

    if clf == "LSTM":
        st.write("## LSTM Model")
        st.write("직접 하이퍼 파라미터를 설정해 모델을 학습시킬 수 있습니다.")
        
        feature = st.multiselect("Select Features",
                                  ["나스닥","코스피","코스닥","기관합계매수량","기타법인매수량","개인매수량","외국인합계매수량",
                                   "등락률","거래량","전일비","score1","score2","score3","변동금리","vix"],
                                  ["score1","score2","score3"])
        label = ["종가"]

        col1, col2, col3 = st.columns(3)
        with col1:
            train_size = st.number_input("Settin Train Size", step=5, min_value=100)
        with col2:
            epoch = st.number_input("Settin Epoch",step = 10, min_value=30)
        with col3:
            batch_size = st.number_input("Setting Batch Size", step=4, min_value=16)
        
        col4, col5, col6 = st.columns(3)
        with col4:
            sequence_length = st.number_input('Setting Sequence Length', step=1,min_value=5)
        with col5:
            activation = st.selectbox("Setting Activation Function",["relu","tanh"])
        with col6:
            optimizer = st.selectbox("Setting Optimizer",["rmsprop","adam"])


        result1 = st.button(label = "실행", help = "모델을 실행시킵니다.")
        with st.spinner("딥러닝 모델 학습중...."):
            if result1:
                act, pred, c_price, c_rate= dl.lstm_model(data,data_idx,feature,label,train_size,epoch,batch_size,sequence_length,activation,optimizer)
                rmse, r2 = dl.do_predict(act,pred)
                st.write(f'현재 날짜는 {datetime.strftime((datetime.now()).date(), "%Y-%m-%d")} 입니다.')
                today = datetime.strftime((datetime.now()).date(), "%Y-%m-%d")
                if today == act.index[-1]:
                    day = datetime.strftime(date.today() + timedelta(1), "%Y-%m-%d")
                else:
                    day = today

                rate = str(c_rate)
                
                st.write("#### R-Squared")
                st.write(f"R-Squared : {r2}")
                r2_expand = st.expander("R-Squared란 무엇인가요?")
                r2_expand.write("""
                R-Squared 값은 독립변수가 종속변수를 얼마나 잘 설명하는지를 나타내는 지표입니다.  
                R-Squared 값은 보통 0 ~ 1 사이의 값을 가지게 됩니다.
                여기서 독립변수는 여러분들이 선택한 feature를 의미하고, 종속변수는 내일의 주가가 됩니다.  
                R-Squared 값이 1에 가깝다는 것은 예측결과가 신뢰할만 하다는 것을 의미하며, 0에 가깝다면 그다지 신뢰할만하지 않다고 볼 수 있습니다.  
                만약 음수가 나오게 된다면 여러분이 선택한 모델은 전혀 신뢰할 수 없는 모델임을 의미합니다.  
                
                좋은 R-Squared 값이 나올 수 있도록 노력해보세요!
                """)
                st.write("#### 주가 예측")
                if c_rate < 0:
                    st.write(f"{day} 예측가격 : {c_price}")
                    st.write(f"{day} 주가는 {rate}% 내려갈 것으로 예측됩니다.")
                elif c_rate > 0:
                    st.write(f"{day} 예측가격 : {c_price}")
                    st.write(f"{day} 주가는 {rate}% 올라갈 것으로 예측됩니다.")
                else:
                    st.write(f"{day} 예측가격 : {c_price}")
                    st.write(f"{day} 주가는 변하지 않을 것으로 예측됩니다.")
                price_expand = st.expander("예측가격은 어떻게 나오나요?")
                price_expand.write("""
                예측가는 딥러닝 시계열 분석 결과로 나온 값을 토대로 나오게 됩니다.  
                오늘의 예측가격과 내일의 예측가격 사이의 등락율을 계산하고, 그 등락율을 오늘의 종가에 적용합니다.  
                따라서, 내일의 예측가격은 (오늘의 주가 x 예측된 등락율)이 됩니다.  
                """)
                price_expand.write(f"{day} 의 예측가는 {act.index[-1]} 예측가와 {day} 의 예측가 사이의 등락율을 {day} 실제가에 적용한 값입니다. ")
                
                st.write("#### 주가 예측 그래프")
                g1, g2 = st.columns(2)
                with g1:
                    dl.make_graph(act,pred)
                graph_expand = st.expander("주가 예측 그래프는 무엇인가요?")
                graph_expand.write("""
                여러분이 직접 설정한 모델의 예측을 보여주는 그래프입니다.  
                주황색 선은 여러분의 모델이 예측한 주가를 보여주는 것이고 파란색 선은 실제 주가를 보여주는 것입니다.
                """)

    elif clf == "GRU":
        st.write("## GRU")
        st.write("직접 하이퍼 파라미터를 설정해 모델을 학습시킬 수 있습니다.")
        
        feature = st.multiselect("Select Features",
                                  ["나스닥","코스피","코스닥","기관합계매수량","기타법인매수량","개인매수량","외국인합계매수량",
                                   "등락률","거래량","전일비","score1","score2","score3","변동금리","vix"],
                                  ["score1","score2","score3"])
        label = ["종가"]

        col1, col2, col3 = st.columns(3)
        with col1:
            train_size = st.number_input("Settin Train Size", step=5, min_value=100)
        with col2:
            epoch = st.number_input("Settin Epoch",step = 10, min_value=30)
        with col3:
            batch_size = st.number_input("Setting Batch Size", step=4, min_value=16)
        
        col4, col5, col6 = st.columns(3)
        with col4:
            sequence_length = st.number_input('Setting Sequence Length', step=1,min_value=5)
        with col5:
            activation = st.selectbox("Setting Activation Function",["relu","tanh"])
        with col6:
            optimizer = st.selectbox("Setting Optimizer",["rmsprop","adam"])

        result1 = st.button("실행")
        with st.spinner("딥러닝 모델 학습중...."):
            if result1:
                act, pred, c_price, c_rate= dl.gru_model(data,data_idx,feature,label,train_size,epoch,batch_size,sequence_length,activation,optimizer)
                rmse, r2 = dl.do_predict(act,pred)
                st.write(f'현재 날짜는 {datetime.strftime((datetime.now()).date(), "%Y-%m-%d")} 입니다.')
                today = datetime.strftime((datetime.now()).date(), "%Y-%m-%d")
                if today == act.index[-1]:
                    day = datetime.strftime(date.today() + timedelta(1), "%Y-%m-%d")
                else:
                    day = today

                rate = str(c_rate)
                
                st.write("#### R-Squared")
                st.write(f"R-Squared : {r2}")
                r2_expand = st.expander("R-Squared란 무엇인가요?")
                r2_expand.write("""
                R-Squared 값은 독립변수가 종속변수를 얼마나 잘 설명하는지를 나타내는 지표입니다.  
                R-Squared 값은 보통 0 ~ 1 사이의 값을 가지게 됩니다.
                여기서 독립변수는 여러분들이 선택한 feature를 의미하고, 종속변수는 내일의 주가가 됩니다.  
                R-Squared 값이 1에 가깝다는 것은 예측결과가 신뢰할만 하다는 것을 의미하며, 0에 가깝다면 그다지 신뢰할만하지 않다고 볼 수 있습니다.  
                만약 음수가 나오게 된다면 여러분이 선택한 모델은 전혀 신뢰할 수 없는 모델임을 의미합니다.  
                
                좋은 R-Squared 값이 나올 수 있도록 노력해보세요!
                """)
                st.write("#### 주가 예측")
                if c_rate < 0:
                    st.write(f"{day} 예측가격 : {c_price}")
                    st.write(f"{day} 주가는 {rate}% 내려갈 것으로 예측됩니다.")
                elif c_rate > 0:
                    st.write(f"{day} 예측가격 : {c_price}")
                    st.write(f"{day} 주가는 {rate}% 올라갈 것으로 예측됩니다.")
                else:
                    st.write(f"{day} 예측가격 : {c_price}")
                    st.write(f"{day} 주가는 변하지 않을 것으로 예측됩니다.")
                price_expand = st.expander("예측가격은 어떻게 나오나요?")
                price_expand.write("""
                예측가는 딥러닝 시계열 분석 결과로 나온 값을 토대로 나오게 됩니다.  
                오늘의 예측가격과 내일의 예측가격 사이의 등락율을 계산하고, 그 등락율을 오늘의 종가에 적용합니다.  
                따라서, 내일의 예측가격은 (오늘의 주가 x 예측된 등락율)이 됩니다.  
                """)
                price_expand.write(f"{day} 의 예측가는 {act.index[-1]} 예측가와 {day} 의 예측가 사이의 등락율을 {day} 실제가에 적용한 값입니다. ")
                
                st.write("#### 주가 예측 그래프")
                g1, g2 = st.columns(2)
                with g1:
                    dl.make_graph(act,pred)
                graph_expand = st.expander("주가 예측 그래프는 무엇인가요?")
                graph_expand.write("""
                여러분이 직접 설정한 모델의 예측을 보여주는 그래프입니다.  
                주황색 선은 여러분의 모델이 예측한 주가를 보여주는 것이고 파란색 선은 실제 주가를 보여주는 것입니다.
                """)


    elif clf == "Best Model":
        st.write("## Best Model")
        st.write("최적의 하이퍼 파라미터로 학습된 모델입니다.")

        if naming == "kakao":
            st.write(f"{comp}의 가장 예측력이 좋은 모델은 *LSTM* 모델이며 하이퍼 파라미터는 아래와 같습니다.")
            feature = st.multiselect("Select Features",
                                    options=["나스닥","코스피","코스닥","기관합계매수량","기타법인매수량","개인매수량","외국인합계매수량",
                                    "등락률","score1","score2","score3","변동금리","vix"],
                                    default=["나스닥","코스피","코스닥","기관합계매수량","기타법인매수량","개인매수량","외국인합계매수량",
                                    "등락률","score1","score2","score3","변동금리","vix"],
                                    disabled=True)
            label = ["종가"]
            col1, col2, col3 = st.columns(3)
            with col1:
                train_size = st.number_input("Settin Train Size", min_value=130, max_value=130)
            with col2:
                epoch = st.number_input("Settin Epoch", min_value=50, max_value=50)
            with col3:
                batch_size = st.number_input("Setting Batch Size", min_value=16,max_value=16)
            
            col4, col5, col6 = st.columns(3)
            with col4:
                sequence_length = st.number_input('Setting Sequence Length',min_value=14,max_value=14)
            with col5:
                activation = st.selectbox("Setting Activation Function",["tanh"])
            with col6:
                optimizer = st.selectbox("Setting Optimizer",["rmsprop"])
            
            with st.spinner("딥러닝 모델 학습중...."):
                act, pred, c_price, c_rate= dl.lstm_model(data,data_idx,feature,label,train_size,epoch,batch_size,sequence_length,activation,optimizer)
                rmse, r2 = dl.do_predict(act,pred)
                st.write(f'현재 날짜는 {datetime.strftime((datetime.now()).date(), "%Y-%m-%d")} 입니다.')
                today = datetime.strftime((datetime.now()).date(), "%Y-%m-%d")
                if today == act.index[-1]:
                    day = datetime.strftime(date.today() + timedelta(1), "%Y-%m-%d")
                else:
                    day = today

                rate = str(c_rate)
                
                st.write("#### R-Squared")
                st.write(f"R-Squared : {r2}")
                r2_expand = st.expander("R-Squared란 무엇인가요?")
                r2_expand.write("""
                R-Squared 값은 독립변수가 종속변수를 얼마나 잘 설명하는지를 나타내는 지표입니다.  
                R-Squared 값은 보통 0 ~ 1 사이의 값을 가지게 됩니다.
                여기서 독립변수는 여러분들이 선택한 feature를 의미하고, 종속변수는 내일의 주가가 됩니다.  
                R-Square 값이 1에 가깝다는 것은 예측결과가 신뢰할만 하다는 것을 의미하며, 0에 가깝다면 그다지 신뢰할만하지 않다고 볼 수 있습니다.  
                만약 음수가 나오게 된다면 여러분이 선택한 모델은 전혀 신뢰할 수 없는 모델임을 의미합니다.  
                
                좋은 R-Squared 값이 나올 수 있도록 노력해보세요!
                """)
                st.write("#### 주가 예측")
                if c_rate < 0:
                    st.write(f"{day} 예측가격 : {c_price}")
                    st.write(f"{day} 주가는 {rate}% 내려갈 것으로 예측됩니다.")
                elif c_rate > 0:
                    st.write(f"{day} 예측가격 : {c_price}")
                    st.write(f"{day} 주가는 {rate}% 올라갈 것으로 예측됩니다.")
                else:
                    st.write(f"{day} 예측가격 : {c_price}")
                    st.write(f"{day} 주가는 변하지 않을 것으로 예측됩니다.")
                price_expand = st.expander("예측가격은 어떻게 나오나요?")
                price_expand.write("""
                예측가는 딥러닝 시계열 분석 결과로 나온 값을 토대로 나오게 됩니다.  
                오늘의 예측가격과 내일의 예측가격 사이의 등락율을 계산하고, 그 등락율을 오늘의 종가에 적용합니다.  
                따라서, 내일의 예측가격은 (오늘의 주가 x 예측된 등락율)이 됩니다.  
                """)
                price_expand.write(f"{day} 의 예측가는 {act.index[-1]} 예측가와 {day} 의 예측가 사이의 등락율을 {day} 실제가에 적용한 값입니다. ")
                
                st.write("#### 주가 예측 그래프")
                g1, g2 = st.columns(2)
                with g1:
                    dl.make_graph(act,pred)
                graph_expand = st.expander("주가 예측 그래프는 무엇인가요?")
                graph_expand.write("""
                여러분이 직접 설정한 모델의 예측을 보여주는 그래프입니다.  
                주황색 선은 여러분의 모델이 예측한 주가를 보여주는 것이고 파란색 선은 실제 주가를 보여주는 것입니다.
                """)
        
        elif naming == "naver":
            st.write(f"{comp}의 가장 예측력이 좋은 모델은 *GRU* 모델이며 하이퍼 파라미터는 아래와 같습니다.")
            feature = st.multiselect("Select Features",
                                    options=["나스닥","코스피","코스닥","기관합계매수량","기타법인매수량","개인매수량","외국인합계매수량",
                                    "등락률","거래량","전일비","score1","score2","score3","변동금리","vix"],
                                    default=["나스닥","코스피","코스닥","기관합계매수량","기타법인매수량","개인매수량","외국인합계매수량",
                                    "등락률","거래량","전일비","score1","score2","score3","변동금리","vix"],
                                    disabled=True)
            label = ["종가"]
            col1, col2, col3 = st.columns(3)
            with col1:
                train_size = st.number_input("Settin Train Size", min_value=150, max_value=150)
            with col2:
                epoch = st.number_input("Settin Epoch", min_value=50, max_value=50)
            with col3:
                batch_size = st.number_input("Setting Batch Size", min_value=16,max_value=16)
            
            col4, col5, col6 = st.columns(3)
            with col4:
                sequence_length = st.number_input('Setting Sequence Length',min_value=23,max_value=23)
            with col5:
                activation = st.selectbox("Setting Activation Function",["relu"])
            with col6:
                optimizer = st.selectbox("Setting Optimizer",["rmsprop"])
            with st.spinner("딥러닝 모델 학습중...."):
                act, pred, c_price, c_rate= dl.gru_model(data,data_idx,feature,label,train_size,epoch,batch_size,sequence_length,activation,optimizer)
                rmse, r2 = dl.do_predict(act,pred)
                st.write(f'현재 날짜는 {datetime.strftime((datetime.now()).date(), "%Y-%m-%d")} 입니다.')
                today = datetime.strftime((datetime.now()).date(), "%Y-%m-%d")
                if today == act.index[-1]:
                    day = datetime.strftime(date.today() + timedelta(1), "%Y-%m-%d")
                else:
                    day = today

                rate = str(c_rate)
                
                st.write("#### R-Squared")
                st.write(f"R-Square : {r2}")
                r2_expand = st.expander("R-Squared란 무엇인가요?")
                r2_expand.write("""
                R-Squared 값은 독립변수가 종속변수를 얼마나 잘 설명하는지를 나타내는 지표입니다.  
                R-Squared 값은 보통 0 ~ 1 사이의 값을 가지게 됩니다.
                여기서 독립변수는 여러분들이 선택한 feature를 의미하고, 종속변수는 내일의 주가가 됩니다.  
                R-Square 값이 1에 가깝다는 것은 예측결과가 신뢰할만 하다는 것을 의미하며, 0에 가깝다면 그다지 신뢰할만하지 않다고 볼 수 있습니다.  
                만약 음수가 나오게 된다면 여러분이 선택한 모델은 전혀 신뢰할 수 없는 모델임을 의미합니다.  
                
                좋은 R-Squared 값이 나올 수 있도록 노력해보세요!
                """)
                st.write("#### 주가 예측")
                if c_rate < 0:
                    st.write(f"{day} 예측가격 : {c_price}")
                    st.write(f"{day} 주가는 {rate}% 내려갈 것으로 예측됩니다.")
                elif c_rate > 0:
                    st.write(f"{day} 예측가격 : {c_price}")
                    st.write(f"{day} 주가는 {rate}% 올라갈 것으로 예측됩니다.")
                else:
                    st.write(f"{day} 예측가격 : {c_price}")
                    st.write(f"{day} 주가는 변하지 않을 것으로 예측됩니다.")
                price_expand = st.expander("예측가격은 어떻게 나오나요?")
                price_expand.write("""
                예측가는 딥러닝 시계열 분석 결과로 나온 값을 토대로 나오게 됩니다.  
                오늘의 예측가격과 내일의 예측가격 사이의 등락율을 계산하고, 그 등락율을 오늘의 종가에 적용합니다.  
                따라서, 내일의 예측가격은 (오늘의 주가 x 예측된 등락율)이 됩니다.  
                """)
                price_expand.write(f"{day} 의 예측가는 {act.index[-1]} 예측가와 {day} 의 예측가 사이의 등락율을 {day} 실제가에 적용한 값입니다. ")
                
                st.write("#### 주가 예측 그래프")
                g1, g2 = st.columns(2)
                with g1:
                    dl.make_graph(act,pred)
                graph_expand = st.expander("주가 예측 그래프는 무엇인가요?")
                graph_expand.write("""
                여러분이 직접 설정한 모델의 예측을 보여주는 그래프입니다.  
                주황색 선은 여러분의 모델이 예측한 주가를 보여주는 것이고 파란색 선은 실제 주가를 보여주는 것입니다.
                """)


    else:
        st.write("# Welcome to Deep Learning!")
        time_expand = st.expander("✅ 시계열 분석")
        time_expand.write("시계열 데이터란 시간의 흐름에 따라 순차적으로 기록된 데이터를 말합니다.")
        time_expand.write("시계열 분석은 시계열 데이터를 가지고 미래를 예측하는 분석 방법입니다.")
        time_expand.write("이 페이지에서는 딥러닝 모델을 이용한 시계열 분석으로 하여 주가를 예측합니다.")

        best_expand = st.expander("✅ Best Model")
        best_expand.write("Best Model 페이지에서는 Grid Search*를 통해 찾아낸 최적의 하이퍼 파라미터로 학습된 모델로 예측 결과를 확인할 수 있습니다.")
        best_expand.write("LSTM, GRU 페이지에서는 직접 파라미터를 설정하여 모델을 학습시킬 수 있습니다.")

        lstm_expand = st.expander("✅ LSTM Model")
        lstm_expand.write("*LSTM(Long Short-Term Memory)*은 순환신경망의 한 종류입니다.")
        lstm_expand.write("오래된 정보에 대한 학습능력이 떨어지는 것을 방지하기위해 고안된 방법입니다.")
        lstm_expand.write("현재 시점에서 예측을 수행할 때, 최근의 데이터만을 가지고 학습을 진행합니다.")

        gru_expand = st.expander("✅ GRU Model")
        gru_expand.write("*GRU(Gated Recurrent Unit)*은 *LSTM*과 비슷한 성능을 내지만 그 구조는 단순화시킨 모델입니다.")
        gru_expand.write("*GRU*는 단순화된 구조 덕분에 *LSTM*보다 더욱 빠른 학습 속도를 가지게 됩니다.")
# 예측 Prediction 페이지    
elif option == '예측-분류모델 Classification Model':
    prediction_method = execute.Prediction(naming)    

    op_emoji = ':dart:'
    st.sidebar.subheader(f'{op_emoji} {option} 페이지입니다')
    SideTab.sidebar_price_now(comp,codenum)
    SideTab.sidebar_price_widget('KOSPI','1001')
    SideTab.sidebar_price_widget('KOSDAQ','2001')
    st.sidebar.subheader("krx 데이터에서 갱신됩니다.")    
    st.write(f"""
             # :dart: {comp} 주가 정보 예측 
             """)

    col1, col2 = st.columns(2)
    with col1:
        clf = st.selectbox(
            '모델 선택',
            ('Menu','Best Model', 'DecisionTree', 'Logistic', 'KNeighbors', 'Voting',
             'RandomForest', 'GradientBoosting', 'XGB'))

    if clf != 'Menu':
        with st.spinner('Wait for it...'):


            #st.write('Selected Features:', options)
            col1, col2,x, col3 = st.columns([10,10,1,19])
            with col1:
                train_test_rate = st.number_input('train_test_rate', step=0.05,
                                                  min_value=0.20,
                                                  max_value=0.40)                    


            if clf == 'Best Model':

                st.text('''
                    ℹ️ train_test_rate 는 0.2로 고정된 상황에서 RandomForest 와 Gradient Boosting 은 모든 특성으로 
제한하여 조사 하였습니다.
                    
확률이 가장높은 모델이 여러가지라면 순서상 가장 빠른순서의 분류기만 보여집니다.
                    
                    ''')
                if comp == 'NAVER':
                    with st.spinner('Wait for it...'):
                        st.text_area('','''Method : XGB    
    특성조합 : ['vix', '코스피', '코스닥', '기관합계매수량', '외국인합계매수량']''',
                         height = 50)
                        np.random.seed(10)
                        prediction_method.bundle(prediction_method.xgB()
                                                 , ['vix', '코스피', '코스닥', '기관합계매수량', '외국인합계매수량'], train_test_rate)

                    
            
                else:
                    
                    with st.spinner('Wait for it...'):
                        st.text_area('','''Method : DecisionTree 
    max_depth = 5
    min_sample_leaf = 2
    min_sample_split = 2
    특성조합 : ['코스피', '코스닥', '개인매수량', '외국인합계매수량']''',
                         height = 50)
                        np.random.seed(10)
                        prediction_method.bundle(prediction_method.dtc(5,2,2)
                                                 , ['코스피', '코스닥', '개인매수량', '외국인합계매수량'], train_test_rate)
            

            elif clf == 'DecisionTree':
                options = st.multiselect(
                            '특성 선택',
                            ['vix','코스피','코스닥','개인매수량','기관합계매수량','외국인합계매수량','score1','score2','score3'],           
                            ['score1', 'score2','score3'])
                
                with col1:
                    max_depth = st.number_input('max_depth', step=1,
                                                min_value=1,
                                                max_value=10)

                with col2:
                    min_samples_leaf = st.number_input('min_samples_leaf', step=1,
                                                      min_value=1,
                                                      max_value=10)
                    min_samples_split = st.number_input('min_samples_split', step=1,
                                                        min_value=2,
                                                        max_value=10)
                with col3:
                    st.text(
                    '''ℹ️ default옵션으로 gini 계수를 이용합니다.

- max_depth : 트리구조의 최대 깊이입니다.
- min_samples_split : 내부 노드를 분할하는 데 필요한 최소 샘플 수입니다.
- min_samples_leaf : 리프 노드에 있어야 하는 최소 샘플 수입니다.
                    ''')


                with st.spinner('Wait for it...'):
                    features = options
                    np.random.seed(10)
                    prediction_method.bundle(prediction_method.dtc(max_depth,min_samples_leaf,min_samples_split)
                                             , features, train_test_rate)

                
            elif clf == 'Logistic':
                options = st.multiselect(
            '특성 선택',
            ['vix','코스피','코스닥','개인매수량','기관합계매수량','외국인합계매수량','score1','score2','score3'],           
            ['score1', 'score2','score3'])
                with col2:
                    l1_ratio = st.number_input('l1_ratio', step=0.05,
                                                min_value=0.0,
                                                max_value=1.01)
                    
                with col3:
                    st.text(
                    '''ℹ️ Logistic 분류기에서 l1과 l2에 대한 비율을 조정해야하는 ElasticNet 
방식을 이용하고 있습니다.

- l1_ratio : l1 비율 입니다.
                    ''')
                    
                    

                with st.spinner('Wait for it...'):
                    features = options
                    prediction_method.bundle(prediction_method.logi(l1_ratio)
                                             , features, train_test_rate)

            elif clf == 'KNeighbors':
                options = st.multiselect(
            '특성 선택',
            ['vix','코스피','코스닥','개인매수량','기관합계매수량','외국인합계매수량','score1','score2','score3'],           
            ['score1', 'score2','score3'])
                with col2:
                    n_neighbors = st.number_input('n_neighbors', step=1,
                                                min_value=2,
                                                max_value=10)

                with st.spinner('Wait for it...'):
                    features = options
                    prediction_method.bundle(prediction_method.kNN(n_neighbors)
                                             , features, train_test_rate)

            elif clf == 'Voting':
                options = st.multiselect(
            '특성 선택',
            ['vix','코스피','코스닥','개인매수량','기관합계매수량','외국인합계매수량','score1','score2','score3'],           
            ['score1', 'score2','score3'])
                with st.spinner('Wait for it...'):
                    features = options
                    prediction_method.bundle(prediction_method.Vote()
                                             , features, train_test_rate)

            elif clf == 'RandomForest':
                options = st.multiselect(
            '특성 선택',
            ['vix','코스피','코스닥','개인매수량','기관합계매수량','외국인합계매수량','score1','score2','score3'],           
            ['score1', 'score2','score3'])
                with col1:
                    max_depth = st.number_input('max_depth', step=1,
                                                min_value=1,
                                                max_value=10)
                    min_samples_split = st.number_input('min_samples_split', step=1,
                                                        min_value=2,
                                                        max_value=10)
                with col2:
                    min_samples_leaf = st.number_input('min_samples_leaf', step=1,
                                                      min_value=1,
                                                      max_value=10)
                    max_samples = st.number_input('max_samples', step=10,
                                                       min_value=10,
                                                       max_value=100)
                with col3:
                    st.text(
                    '''ℹ️ default옵션으로 gini 계수를 이용하고, 부트스트랩 방식을 적용 했습니다.

- max_depth : 트리구조의 최대 깊이입니다.
- min_samples_split : 내부 노드를 분할하는 데 필요한 최소 샘플 수입니다.
- min_samples_leaf : 리프 노드에 있어야 하는 최소 샘플 수입니다.
- max_samples : 부트스트랩이 True이면 각 기본 추정기를 훈련하기 위해 X에서 추출할 샘플 수입니다.
                    ''')

                with st.spinner('Wait for it...'):
                    features = options
                    prediction_method.bundle(prediction_method.RanF(max_depth,min_samples_leaf,
                                                                    min_samples_split,max_samples)
                                             , features, train_test_rate)

            elif clf == 'GradientBoosting':
                options = st.multiselect(
            '특성 선택',
            ['vix','코스피','코스닥','개인매수량','기관합계매수량','외국인합계매수량','score1','score2','score3'],           
            ['score1', 'score2','score3'])
                with col1:
                    max_depth = st.number_input('max_depth', step=1,
                                                min_value=1,
                                                max_value=10)
                    min_samples_split = st.number_input('min_samples_split', step=1,
                                                        min_value=2,
                                                        max_value=10)
                with col2:
                    min_samples_leaf = st.number_input('min_samples_leaf', step=1,
                                                      min_value=1,
                                                      max_value=10)
                    learning_rate = st.number_input('learning_rate', step=0.1,
                                                       min_value=0.1,
                                                       max_value=0.5)
                with col3:
                    st.text(
                    '''ℹ️ default옵션으로 loss funtion 은 log_loss을 이용합니다.

- max_depth : 개별 회귀 추정기의 최대 깊이입니다.
- min_samples_split : 내부 노드를 분할하는 데 필요한 최소 샘플 수입니다.
- min_samples_leaf : 리프 노드에 있어야 하는 최소 샘플 수입니다.
- learning_rate : 학습률은 learning_rate만큼 각 트리의 기여도를 줄입니다.''')

                with st.spinner('Wait for it...'):
                    features = options
                    prediction_method.bundle(prediction_method.GradB(max_depth,min_samples_leaf,
                                                                    min_samples_split,learning_rate)
                                             , features, train_test_rate)

            else:
                options = st.multiselect(
            'Select Features',
            ['vix','코스피','코스닥','개인매수량','기관합계매수량','외국인합계매수량','score1','score2','score3'],           
            ['score1', 'score2','score3'])
                with st.spinner('Wait for it...'):
                    features = options
                    prediction_method.bundle(prediction_method.xgB()
                                             , features, train_test_rate)


            col1, col2 = st.columns(2)
            #with col1:
            #    vis.price(codenum)



    else:

        """
        # Welcome to Machine Learning!
        """

        basic_expand = st.expander('✅ 기본 분류기')
        basic_expand.write("""
                            - *DecisionTree* 
                        """)
        basic_expand.write("""
                            - *Logistic* 
                        """)
        basic_expand.write("""
                            - *KNeighbors*
                        """)


        ensemble_expand = st.expander('✅ 앙상블 분류기')
        ensemble_expand.write("""
                            통계및 기계 학습 에서 앙상블 방법은 지도 학습 알고리즘 단독으로 얻을 수 있는 예측보다 더 나은 예측 
                            성능을 얻기 위해 여러 학습 알고리즘을 묶어 사용합니다.         
                         """)
        ensemble_expand.write('- *Voting (Voting method)*')
        ensemble_expand.write('- *RandomForest (Bagging method)*')
        ensemble_expand.write('')

        boost_expand = st.expander('✅ 부스팅 분류기')
        boost_expand.write("""         
                       기계 학습 에서 부스팅은 지도학습의 편향과 분산을 줄이기 위한 *앙상블 알고리즘* 이며 약한 학습자를 
                       강한 학습자로 변환하는 기계 학습 알고리즘 제품군입니다.     
                     """)
        boost_expand.write('- *GradientBoosting*')
        boost_expand.write('- *XGB*')
        boost_expand.write('')

        feature_expand = st.expander('✅ 특성 정보')
        feature_expand.write('- *vix* : 변동성 지수')
        feature_expand.write('- *코스피*')
        feature_expand.write('- *코스닥*')

        feature_expand.write('- *개인매수량*')
        feature_expand.write('- *기관합계매수량*')
        feature_expand.write('- *외국인합계매수량*')
        feature_expand.write('- *score#* : 기사에 대한 점수')
        
        st.write('''
         각 분류기에 대해 궁금하신점은 [sklearn](https://scikit-learn.org/stable/search.html)을 참고하시면 됩니다.
         
         XGB 분류기는 [XGBoost](https://xgboost.readthedocs.io/en/stable/index.html)를 참고하시면 됩니다.
        ''')

# 상승 상승 맞춤 /상승
