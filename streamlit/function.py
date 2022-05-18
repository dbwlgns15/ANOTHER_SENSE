import pandas as pd
import numpy as np
import re
import requests
import pickle
from konlpy.tag import Okt
from bs4 import BeautifulSoup
from datetime import date
from collections import Counter
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

def get_code(symbol):
    krx = pd.read_csv('./src/krx_code.csv')
    krx = krx.set_index('한글 종목약명')
    try:
        code = krx.at[symbol,'단축코드']
        return code
    except:
        return 0

def get_today():
    today = date.today().isoformat()
    return today

def get_feargreed_wordcloud(symbol):
    code = get_code(symbol)
    if code == 0:
        return 0
    today = get_today()
    comment_list = []
    chk = 1
    i = 1
    while chk:  
        url = f'https://finance.naver.com/item/board.naver?code={code}&page={i}'
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50'}
        res = requests.get(url, headers = headers)
        bs = BeautifulSoup(res.text, 'html.parser')  
        for j in range(20):
            try:
                root = bs.find('div',{'class':'section inner_sub'}).find_all('tr',{'onmouseover':'mouseOver(this)'})[j].text.split('\n') 
                if today != root[1].split()[0].replace('.','-'):
                    chk = 0
                    break
                if len(root) == 14: 
                    pass      
                elif len(root) == 13: 
                    comment = root[3]
                    comment = re.sub('\[삭제된 게시물의 답글\]',' ',comment)
                    comment = re.sub('[^가-힣]',' ',comment)
                    comment = re.sub(' +',' ',comment)
                    comment = comment.strip()
                    if comment == '':
                        pass
                    else:
                        comment_list.append(comment)                 
                else: 
                    pass
            except: 
                pass
        i += 1
        if chk == 0:
            break   
    okt = Okt()
    tag_list = ['Noun','Verb','Adjective','VerbPrefix'] 
    tokenized_data = []
    words = []
    for i in range(len(comment_list)):
        tokenized_sentence = okt.pos(comment_list[i], stem=True) 
        tag_checked_sentence = []
        for j in tokenized_sentence:
            x,y = j
            if y in tag_list:
                tag_checked_sentence.append(x)
            if y == 'Noun':
                words.append(x)
        if tag_checked_sentence == []:
            pass
        else:
            tokenized_data.append(tag_checked_sentence)     
    for i in tokenized_data:
        for j in range(len(i)):
            i[j] = "'"+i[j]+"'"
    with open('./src/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)   
    test = tokenizer.texts_to_sequences(tokenized_data)
    test = pad_sequences(test, maxlen=15)
    model = load_model('./src/model.h5')
    pred = model.predict(test)
    feargreed_index = f'{int(((pred.mean()-0.5)*2+0.5)*100)}%'
    wordcloud = Counter(words)

    return feargreed_index, wordcloud