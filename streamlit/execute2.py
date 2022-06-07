import pandas as pd
from PIL import Image
from datetime import date, timedelta

class feargreed():
    def __init__(self, comp):
        if comp == '카카오':
            df = pd.read_csv('./data/feargreed_kakao.csv')
        else:
            df = pd.read_csv('./data/feargreed_naver.csv')        
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
        return Image.open(f'./data/feargreed_{chk}.png')

    def get_comments(self,day):
        df = self.df
        greed_comments = df[df['날짜'] == day.isoformat()].sort_values(by='공포탐욕')['댓글'].head().to_list()
        fear_comments = df[df['날짜'] == day.isoformat()].sort_values(by='공포탐욕')['댓글'].tail().to_list()
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

