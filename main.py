# Streamlit으로 웹서비스 구현하기 
import streamlit as st
from PIL import Image
import execute
import time
from datetime import datetime

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

# codenum = execute.get_company_code(comp) # codenum = 기업코드


# 사이드바2 - 카테고리 선택
option = st.sidebar.selectbox(
    '열람할 페이지를 선택해주세요.',
    ('메인 홈 Main Home', '기업정보 Company Information', '개미 동향 Ants MIND','기사 News','예측 Prediction')
)


# 사이드바에서 선택한 카테고리에 따른 페이지뷰

# 메인 홈페이지
SideTab = execute.SideTab()
SideTab.sidebar_price_now(comp,codenum)
SideTab.sidebar_price_widget()
st.sidebar.subheader("krx 데이터에서 갱신됩니다.")

if option == '메인 홈 Main Home':
    op_emoji = ':house:'
    st.sidebar.subheader(f'{op_emoji} {option} 페이지입니다')
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
                
                __단! 모든 예측이 항상 적중하는 것은 아니란 사실을 유념하세요! 투자의 책임은 언제나 스스로 지는 것이니까요!__          
             """)
    
        

# 개미 동향 페이지
elif option == '개미 동향 Ants MIND': ## fear&greed와 댓글 분석 페이지
    op_emoji = ':ant:'
    st.sidebar.subheader(f'{op_emoji} {option} 페이지입니다')
    st.write(f'''
             # :cupid: {comp} 개미 투자자 심리
             ''')
    ant_col1, ant_col2 = st.columns(2)
    
    ant_col1.write('# 시험용으로 적어놓은 텍스트임. 추후 수정 예정!!')
    ant_col1.write("> 사람의 마음은 매우 복잡하고, 얼기설기 얽혀있어서 연구하고 판단 내리기가 쉽지 않아요. 팀 어나더센스는 개미 투자자들의 심리를 분석하기 위해 여러 방법을 고민하던 중, 😨공포탐욕지수(Fear&Greed Index)🤑를 벤치마킹하기로 결정했어요.")
    ant_col1.image('https://mblogthumb-phinf.pstatic.net/MjAyMDAzMTBfMjY5/MDAxNTgzNzk5MDc0MzIw.L52CSqVI9FwSHOzgM_plclsU8SPlm12IiE9HN4vALMIg.b043Hy3Epx1V-OSo3ZnNqjsdvrSZ9jBz7wtTZx84N4Eg.JPEG.sjay34/1583799073661.jpg?type=w800', width = 600)


# 관련 뉴스 페이지
elif option == '기사 News':
    op_emoji = ':newspaper:'
    # article = execute.Article()
    # st.sidebar.subheader(f'{op_emoji} {option} 페이지입니다')
    st.title(f':newspaper: {comp} 관련 뉴스')
    st.subheader(f"내가 선택한 기업 \"{comp}\"의 🔥최신 이슈🔥들을 모아 볼 수 있어요!")

    sub_opt = st.selectbox(
        '옵션을 선택해주세요',
        ('최근 기사', '최근 언론사별 기사'))

    # if sub_opt == '오늘의 기사':
    #    article = execute.Article(comp,1)
    #    article.range_article(1)
    article = execute.Article(comp, 7)
    if sub_opt == '최근 기사':
        article.range_article(7)
    else:
        article.company_article()

    st.write('You selected:', sub_opt)


    
    
# 기업정보 페이지
elif option == '기업정보 Company Information':
    op_emoji = ':information_source:'
    st.sidebar.subheader(f'{op_emoji} {option} 페이지입니다')
    
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
        st.write(f'> 왼쪽의 이미지는 {comp}의 주식가격 흐름을 나타낸 표입니다. 범례에서 확인하실 수 있듯이 분홍색, 초록색, 노랑색의 세 가지 선은 각각 20일, 60일, 120일동안의 이동평균선입니다!')
        

    st.write('### 투자의견')
    st.image(f'data/{opinion}.png', width = 500)
    

    
# 예측 Prediction 페이지    
else:
    if comp == '카카오':
        naming = 'kakao'
    else:
        naming = 'naver'
    vis = execute.visualization()
    prediction_method = execute.Prediction(naming)

    op_emoji = ':dart:'
    st.sidebar.subheader(f'{op_emoji} {option} 페이지입니다')
    st.write(f'''
             # :dart: {comp} 주가 정보 예측 
             ''')
    clf = st.selectbox(
        'Select Classifier',
        ('Menu', 'DecisionTree', 'Logistic', 'KNeighbors', 'Voting',
         'RandomForest', 'GradientBoosting', 'XGB'))

    if clf != 'Menu':

        options = st.multiselect(
            'Select Features',
            ['금리','vix','개인','기관','외국인','score1', 'score2','score3'],
            ['score1', 'score2','score3'])


        if options:
            st.write('Selected Features:', options)

            random_state = st.number_input('Setting Random_state', step=1,min_value=0)
            train_test_rate = st.number_input('Setting train_test_rate', step=0.05,
                                              min_value=0.05,
                                              max_value=0.95)

            if clf:

                with st.spinner('Wait for it...'):
                    features = options
                    prediction_method.bundle(clf, features, train_test_rate, random_state)

            st.write('')
            st.write(f'현재 날짜는 {datetime.strftime((datetime.now()).date(), "%Y-%m-%d")} 입니다.')
            st.write('')
            vis.price(codenum)

        else:
            st.write('You must select Features')

    else:
        basic_expand = st.expander('Basic Classification')
        basic_expand.write("""
                            - 의사결정 트리 학습은 데이터 마이닝에서 일반적으로 사용되는 방법입니다. 
                            목표는 여러 입력 변수를 기반으로 대상 변수의 값을 예측하는 모델을 만드는 것입니다.
                        """)
        basic_expand.write("""
                            - 로지스틱 회귀의 목적은 일반적인 회귀 분석의 목표와 동일하게 종속 변수와 
                            독립 변수간의 관계를 구체적인 함수로 나타내어 향후 예측 모델에 사용하는것 입니다.
                        """)
        basic_expand.write("""
                            - 패턴 인식에서, k-최근접 이웃 알고리즘(또는 줄여서 k-NN)은 분류나 회귀에 
                            사용되는 비모수 방식이다.
                        """)


        ensemble_expand = st.expander('Ensemble Classification')
        ensemble_expand.write("""
                            통계및 기계 학습 에서 앙상블 방법은 지도 학습 알고리즘 단독으로 얻을 수 있는 예측보다 더 나은 예측 
                            성능을 얻기 위해 여러 학습 알고리즘을 묶어 사용합니다.         
                         """)
        ensemble_expand.write('- Voting (Voting method)')
        ensemble_expand.write('- RandomForest (Bagging method)')
        ensemble_expand.write('')

        boost_expand = st.expander('Boosting Classification')
        boost_expand.write("""         
                       기계 학습 에서 부스팅은 지도학습의 편향과 분산을 줄이기 위한 앙상블 알고리즘 이며 약한 학습자를 
                       강한 학습자로 변환하는 기계 학습 알고리즘 제품군입니다.     
                     """)
        boost_expand.write('- GradientBoosting')
        boost_expand.write('- XGB')
        boost_expand.write('')

        feature_expand = st.expander('Feature Infomation')
        feature_expand.write('- 금리 : cma 금리')
        feature_expand.write('- vix : 변동성 지수')
        feature_expand.write('- 개인 : 개인 거래량')
        feature_expand.write('- 기관 : 기관 거래량')
        feature_expand.write('- 외국인 : 외국인 거래량')
        feature_expand.write('- score# : 기사에 대한 점수')
        feature_expand.write('Random_state 를 수정하면 ')