# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DecoLexO.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

import pandas as pd
import numpy as np
import os, re
from PyQt5 import QtCore, QtGui, QtWidgets

    ##Function Code##
    
def column_name(df):
    # 첫 행 살리기
    first = list (df.columns)
    df.loc[0] = first
    for val in first:
        if 'Unnamed' in val:
            x = first.index (val)
            first[x] = np.nan
    df.loc[0] = first

    df = df.fillna ('')
    sem_rgx = re.compile (r'[Q][A-Z]{3}')  # semantic tagset
    syn_rgx = re.compile (r'[Y][A-Z]{3}')  # syntactic tagset
    dom_rgx = re.compile (r'[X]{1}[ABCDEFGHIJKLMNOPQRSTUVWYZ]{3}')  # domain tagset
    ent_rgx = re.compile (r'[X]{2}[A-Z]{2}')  # entity tagset
    mor_rgx = re.compile (r'[A-Z]{3}')  # morph tagset

    # 컬럼의 총 개수를 l에 저장한다.
    # 컬럼의 개수 만큼 lemma와 category뒤에 lemma와 category개수인 2를 뺀만큼
    # ''를 추가해 주어 해당 컬럼 개수 만큼의 리스트 col_nme을 만들어 준다.
    l = len (df.columns)
    col_nme = ['Lemma', 'Category']
    for i in range (l - 2):
        col_nme.append ('')
    # sem =>SemInfo 뒤에 붙을 숫자
    # syn =>SynInfo 뒤에 붙을 숫자
    # dom =>DomInfo 뒤에 붙을 숫자
    # ent =>EntInfo 뒤에 붙을 숫자
    # mor =>MorInfo 뒤에 붙을 숫자
    sem = 1
    syn = 1
    dom = 1
    ent = 1
    mor = 1

    # x를 컬럼의 개수 만큼의 숫자로 지정해 준다.
    # col_val은 해당 df의 열을 리스트화 시켜준 것이다.
    for x in range (0, l):
        col_val = df.iloc[:, x].tolist ()
        # cnt가 0이면 일치하는 값을 못 찾았다는 의미로 해석(ex 모두 빈칸인 열을 만났을 때)
        # 밑에서 cnt == 0 일때 앞에 정보를 보고 빈칸의 정보를 수정할 때 사용한다.
        cnt = 0
        # k로 col_val의 리스트 요소들을 하나씩 지정해주면서
        # k가 sem_rgx, syn_rgx, dom_rgx, ent_rgx, mor_rgx에 해당되면
        # 컬럼에 일치하는 값이 있었다는 의미로 cnt를 1 증가시켜 주고
        # Info뒤에 붙을 숫자를 1씩 증가시켜 주고
        # 비효율적인 탐색을 막기 위해 바로 break시켜준다.
        for k in col_val:
            if sem_rgx.match (k):
                col_nme[x] = 'SemInfo' + str (sem)
                sem += 1
                cnt += 1
                break

            elif syn_rgx.match (k):
                col_nme[x] = 'SynInfo' + str (syn)
                syn += 1
                cnt += 1
                break

            elif dom_rgx.match (k):
                col_nme[x] = 'DomInfo' + str (dom)
                dom += 1
                cnt += 1
                break

            elif ent_rgx.match (k):
                col_nme[x] = 'EntInfo' + str (ent)
                ent += 1
                cnt += 1
                break

            elif mor_rgx.match (k):
                col_nme[x] = 'MorInfo' + str (mor)
                mor += 1
                cnt += 1
                break

        # 만약 위에서 일치하는 값을 못찾았을 때(ex 모두 빈칸인 열이었을 때)
        # cnt는 0이므로 앞에 col_nme의 정보를 보고
        # 해당 정보와 일치하는 정보의 Info숫자를 증가시켜준 값을 해당 리스트 위치에 저장해준다.
        if cnt == 0:
            if 'Sem' in col_nme[x - 1]:
                col_nme[x] = 'SemInfo' + str (sem)
                sem += 1

            elif 'Syn' in col_nme[x - 1]:
                col_nme[x] = 'SynInfo' + str (syn)
                syn += 1

            elif 'Dom' in col_nme[x - 1]:
                col_nme[x] = 'DomInfo' + str (dom)
                dom += 1

            elif 'Ent' in col_nme[x - 1]:
                col_nme[x] = 'EntInfo' + str (ent)
                ent += 1

            elif 'Mor' in col_nme[x - 1]:
                col_nme[x] = 'MorInfo' + str (mor)
                mor += 1

    df.columns = col_nme

    return df


# 입력받은 word와 같은 단어 정보들을 출력하는 함수
def Equals(df, col, word):

    #입력받은 단어가 1개 이상일 때는 +로 묶여서 들어오기 때문에 입력받은 word에
    # +가 있는지 확인후 존재하면 +단위로 나눈 단어들을 list 형태로 word_lsit에 저장해주고
    # 단일 단어일 경우 그 단어 자체를 list형태로 word_list에 저장해준다. 
    if '+' in word:
        word_list = word.split ('+')
    else:
        word_list = []
        word_list.append (word)

    #filtered_list에는 찾고자하는 요소에 매칭되는 단어들을 저장할 것이고
    #filtered_index에는 원본 데이터에 있는 찾은 단어의 인덱스를 저장할 것이다.
    filtered_list = []
    filtered_index = []

    #i는 word_list에 저장된 단어의 개수를 길이로 설정하고
    #j는 원본데이터의 행의 개수를 길이로 설정한다.
    #df는 원본데이터, col은 찾고자 하는 정보(Lemma, Entry, Catgory..), word는 찾고자 하는 단어.
    #df.loc[j, col] => 열마다 돌아가면서 해당 정보와 찾고자 하는 단어가 일치하면
    #answer에 일치 정보의 열을 통째로 저장해준다.
    #이때는 시리즈 형태로 저장되어 있기 때문에 filtered_list에 answer을 list화 한 정보를 넣어주면
    #컬럼 정보는 제외된 순수 데이터 정보만 filteres_list에 저장이된다.
    #filtered_index에는 gui상에서 원본 인덱스보다 +1 된 값으로 나오기 때문에 
    #찾은 데이터의 인덱스 값을 +1해서 넣어준다.
    for i in range (len (word_list)):
        for j in range (len (df)):
            if df.loc[j, col] == word_list[i]:
                answer = df.iloc[j]
                filtered_list.append(list(answer))
                filtered_index.append(str(j+1))

    # result는 series로 저장되어 있기 때문에 to_frame()으로 df화 해주고
    # 현재 row와 column이 바뀌어 저장되어 있기 때문에
    # .T로 transepose() 기능을 주어 row와 column을 바꾸어 준다.
    filtered_header = handle_df.columns.tolist()
    filtered_df = pd.DataFrame(filtered_list, columns=filtered_header)
    filtered_df.head()
    filtered_df.insert(0,'Original Index', filtered_index)

    return filtered_df


# 입력받은 단어들이 포함되어 있는 단어 정보들을 출력하는 함수
def Contains(df, col, word):
    if '+' in word:
            word_list = word.split ('+')
    else:
        word_list = []
        word_list.append (word)
    
    #filtered_list에는 찾고자하는 요소에 매칭되는 단어들을 저장할 것이고
    #filtered_index에는 원본 데이터에 있는 찾은 단어의 인덱스를 저장할 것이다.
    filtered_list = []
    filtered_index = []

    #i는 word_list에 저장된 단어의 개수를 길이로 설정하고
    #j는 원본데이터의 행의 개수를 길이로 설정한다.
    #df는 원본데이터, col은 찾고자 하는 정보(Lemma, Entry, Catgory..), word는 찾고자 하는 단어.
    #df.loc[j, col] => 열마다 돌아가면서 해당 정보와 찾고자 하는 단어를 포함하면
    #answer에 일치 정보의 열을 통째로 저장해준다.
    #이때는 시리즈 형태로 저장되어 있기 때문에 filtered_list에 answer을 list화 한 정보를 넣어주면
    #컬럼 정보는 제외된 순수 데이터 정보만 filteres_list에 저장이된다.
    #filtered_index에는 gui상에서 원본 인덱스보다 +1 된 값으로 나오기 때문에 
    #찾은 데이터의 인덱스 값을 +1해서 넣어준다.
    for i in range (len (word_list)):
        for j in range (len (df)):
            if word[i] in df.loc[j, col]:
                result = df.iloc[j]
                filtered_list.append(list(result))
                filtered_index.append(str(j+1))

    # result는 series로 저장되어 있기 때문에 to_frame()으로 df화 해주고
    # 현재 row와 column이 바뀌어 저장되어 있기 때문에
    # .T로 transepose() 기능을 주어 row와 column을 바꾸어 준다.
    filtered_header = handle_df.columns.tolist()
    filtered_df = pd.DataFrame(filtered_list, columns=filtered_header)
    filtered_df.head()
    filtered_df.insert(0,'Original Index', filtered_index)

    return filtered_df
        
def Starts_With(df, col, word):
    if '+' in word:
            word_list = word.split ('+')
    else:
        word_list = []
        word_list.append (word)
    
    #filtered_list에는 찾고자하는 요소에 매칭되는 단어들을 저장할 것이고
    #filtered_index에는 원본 데이터에 있는 찾은 단어의 인덱스를 저장할 것이다.
    filtered_list = []
    filtered_index = []

    #i는 word_list에 저장된 단어의 개수를 길이로 설정하고
    #j는 원본데이터의 행의 개수를 길이로 설정한다.
    #df는 원본데이터, col은 찾고자 하는 정보(Lemma, Entry, Catgory..), word는 찾고자 하는 단어.
    #df.loc[j, col] => 열마다 돌아가면서 해당 정보와 찾고자 하는 단어로 시작하면
    #answer에 일치 정보의 열을 통째로 저장해준다.
    #이때는 시리즈 형태로 저장되어 있기 때문에 filtered_list에 answer을 list화 한 정보를 넣어주면
    #컬럼 정보는 제외된 순수 데이터 정보만 filteres_list에 저장이된다.
    #filtered_index에는 gui상에서 원본 인덱스보다 +1 된 값으로 나오기 때문에 
    #찾은 데이터의 인덱스 값을 +1해서 넣어준다.
    for i in range (len (word_list)):
        for j in range (len (df)):
            if df.loc[j, col].startswith (word[i]):
                result = df.iloc[j]
                filtered_list.append(list(result))
                filtered_index.append(str(j+1))
            

    # result는 series로 저장되어 있기 때문에 to_frame()으로 df화 해주고
    # 현재 row와 column이 바뀌어 저장되어 있기 때문에
    # .T로 transepose() 기능을 주어 row와 column을 바꾸어 준다.
    filtered_header = handle_df.columns.tolist()
    filtered_df = pd.DataFrame(filtered_list, columns=filtered_header)
    filtered_df.head()
    filtered_df.insert(0,'Original Index', filtered_index)

    return filtered_df

def Ends_With(df, col, word):
    if '+' in word:
            word_list = word.split ('+')
    else:
        word_list = []
        word_list.append (word)
    
    #filtered_list에는 찾고자하는 요소에 매칭되는 단어들을 저장할 것이고
    #filtered_index에는 원본 데이터에 있는 찾은 단어의 인덱스를 저장할 것이다.
    filtered_list = []
    filtered_index = []

    #i는 word_list에 저장된 단어의 개수를 길이로 설정하고
    #j는 원본데이터의 행의 개수를 길이로 설정한다.
    #df는 원본데이터, col은 찾고자 하는 정보(Lemma, Entry, Catgory..), word는 찾고자 하는 단어.
    #df.loc[j, col] => 열마다 돌아가면서 해당 정보와 찾고자 하는 단어로 끝나면
    #answer에 일치 정보의 열을 통째로 저장해준다.
    #이때는 시리즈 형태로 저장되어 있기 때문에 filtered_list에 answer을 list화 한 정보를 넣어주면
    #컬럼 정보는 제외된 순수 데이터 정보만 filteres_list에 저장이된다.
    #filtered_index에는 gui상에서 원본 인덱스보다 +1 된 값으로 나오기 때문에 
    #찾은 데이터의 인덱스 값을 +1해서 넣어준다.
    for i in range (len (word)):
        for j in range (len (df)):
            if df.loc[j, col].endswith (word[i]):
                result = df.iloc[j]
                filtered_list.append(list(result))
                filtered_index.append(str(j+1))

    # result는 series로 저장되어 있기 때문에 to_frame()으로 df화 해주고
    # 현재 row와 column이 바뀌어 저장되어 있기 때문에
    # .T로 transepose() 기능을 주어 row와 column을 바꾸어 준다.
    filtered_header = handle_df.columns.tolist()
    filtered_df = pd.DataFrame(filtered_list, columns=filtered_header)
    filtered_df.head()
    filtered_df.insert(0,'Original Index', filtered_index)

    return filtered_df

def Is_Empty(df, col, word):
    if '+' in word:
            word_list = word.split ('+')
    else:
        word_list = []
        word_list.append (word)
    
    #filtered_list에는 찾고자하는 요소에 매칭되는 단어들을 저장할 것이고
    #filtered_index에는 원본 데이터에 있는 찾은 단어의 인덱스를 저장할 것이다.
    filtered_list = []
    filtered_index = []

    #i는 word_list에 저장된 단어의 개수를 길이로 설정하고
    #j는 원본데이터의 행의 개수를 길이로 설정한다.
    #df는 원본데이터, col은 찾고자 하는 정보(Lemma, Entry, Catgory..), word는 찾고자 하는 단어.
    #df.loc[j, col] => 열마다 돌아가면서 해당 정보와 찾고자 하는 단어가 없으면
    #answer에 일치 정보의 열을 통째로 저장해준다.
    #이때는 시리즈 형태로 저장되어 있기 때문에 filtered_list에 answer을 list화 한 정보를 넣어주면
    #컬럼 정보는 제외된 순수 데이터 정보만 filteres_list에 저장이된다.
    #filtered_index에는 gui상에서 원본 인덱스보다 +1 된 값으로 나오기 때문에 
    #찾은 데이터의 인덱스 값을 +1해서 넣어준다.
    for i in range (len (word)):
        for j in range (len (df)):
            if word[i] not in df.loc[j, col]:
                result = df.iloc[j]
                filtered_list.append(list(result))
                filtered_index.append(str(j+1))

    # result는 series로 저장되어 있기 때문에 to_frame()으로 df화 해주고
    # 현재 row와 column이 바뀌어 저장되어 있기 때문에
    # .T로 transepose() 기능을 주어 row와 column을 바꾸어 준다.
    filtered_header = handle_df.columns.tolist()
    filtered_df = pd.DataFrame(filtered_list, columns=filtered_header)
    filtered_df.head()
    filtered_df.insert(0,'Original Index', filtered_index)

    return filtered_df


# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

def Divide(korean_word):
    r_lst = []
    for w in list(korean_word.strip()):
        ## 영어인 경우 구분해서 작성함. 
        if '가'<=w<='힣':
            ## 588개 마다 초성이 바뀜. 
            ch1 = (ord(w) - ord('가'))//588
            ## 중성은 총 28가지 종류
            ch2 = ((ord(w) - ord('가')) - (588*ch1)) // 28
            ch3 = (ord(w) - ord('가')) - (588*ch1) - 28*ch2
            r_lst.append([CHOSUNG_LIST[ch1], JUNGSUNG_LIST[ch2], JONGSUNG_LIST[ch3]])
        else:
            r_lst.append([w])
    return r_lst

#입력받은 초성, 중성, 종성에 해당하는 정보를 첫번째 음절에 포함하고 있는 단어를 출력하는 함수.
def First_Syllable(df, a, b, c):
    #'*' => any consonants
    #'.' => any vowels
    #'w' => 초성, 중성, 종성에 한글이 들어 있을 때
    #''  => a,b,c에 입력이 안들어 왔을 때

    #a, b, c에 들어온 값이 +로 묶여서 들어오면 +단위로 나누어 주어
    #각각 a, b, c에 리스트 형태로 저장해준다.
    #아닌 경우는 그대로 사용한다.
    if '+' in a:
        a = a.split ('+')
    else:
        pass

    if '+' in b:
        b = b.split ('+')
    else:
        pass

    if '+' in c:
       c = c.split ('+')
    else:
        pass

    #df에서 lemma만을 저장하는 코드이다.
    lemma = []
    for i in range(len(df)):
        lemma.append(df.loc[i,'Lemma'])

    #인덱스 값을 저장할 리스트
    indexlis = []
    cnt = 0

    for i in range(len(df)):
        #Divide함수에 df의 lemma들을 차례대로 넣어서 형태소로 나누어 주고
        #word에는 첫번째 Syllable만을 리스트 형태로 저장해준다.
        #word[0] = 초성, word[1] = 중성, word[2] = 종성
        divide = Divide(lemma[i])
        word = divide[0]

        #a(초성)이 가질 수 있는 값: '*', ' ', 'word'
        #b(중성)이 가질 수 있는 값: '.', ' ', 'word'
        #c(종성)이 가질 수 있는 값: '*', '.', ' ', 'word'로
        #총 3x3x4인 36가지의 조건이 각 함수마다 생긴다. 
        #word[0] = 초성, word[1] = 중성, word[2] = 종성

        #a: '*'일 때
        if a == '*':
            #a: '*', b: '.'
            if b == '.':
                #a: '*', b: '.', c: ['*', '.', '', 'w']
                if c == '*':
                    if word[2] != ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                elif c == '.':
                    if word[2] == ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                elif c == '':
                    #if word[2] == ' ':
                    indexlis.append(lemma.index(lemma[i]))
                    cnt += 1
                else:
                    if word[2] in c:
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
            #a: '*', b: ''
            elif b == '':
                #a: '*', b: '', c: ['*', '.', '', 'w']
                if c == '*':
                    if word[2] != ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                elif c == '.':
                    if word[2] == ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                elif c == '':
                    #if word[2] == ' ':
                    indexlis.append(lemma.index(lemma[i]))
                    cnt += 1
                else:
                    if word[2] in c:
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
            #b에 음소들이 저장되어 있을 때
            #a: '*', b: 'w', c: ['*', '.', '', 'w']
            else:
                if word[1] in b:
                    if c == '*':
                        if word[2] != ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '.':
                        if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '':
                        #if word[2] == ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                    else:
                        if word[2] in c:
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1

        elif a == '.':
            break

        #a: ''
        elif a == '':
            #a: '', b: '.'
            if b == '.':
                 #a: '', b: '.', c: ['*', '.', '', 'w']  
                if c == '*':
                    if word[2] != ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                elif c == '.':
                    if word[2] == ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                elif c == '':
                    #if word[2] == ' ':
                    indexlis.append(lemma.index(lemma[i]))
                    cnt += 1
                else:
                    if word[2] in c:
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
            #a: '', b: ''    
            elif b == '':
                 #a: '', b: '', c: ['*', '.', '', 'w']  
                if c == '*':
                    if word[2] != ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                elif c == '.':
                    if word[2] == ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                else:
                    if word[2] in c:
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
            #a: '', b: 'w'
            else:
                if word[1] in b:
                    #a: '', b: 'w', c: ['*', '.', '', 'w']  
                    if c == '*':
                        if word[2] != ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '.':
                        if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '':
                        #if word[2] == ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                    else:
                        if word[2] in c:
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1

        else:
            #a : 'w'
            if word[0] in a:
                #a: 'w', b: '.'
                if b == '.':
                    #a: 'w', b: '.', c: ['*', '.', '', 'w']  
                    if c == '*':
                        if word[2] != ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '.':
                        if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '':
                        #if word[2] == ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                    else:
                        if word[2] in c:
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                #a: 'w', b: ''
                elif b == '':
                    #a: 'w', b: '.', c:['*', '.', '', 'w']  
                    if c == '*':
                        if word[2] != ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '.':
                        if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '':
                        #if word[2] == ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                    else:
                        if word[2] in c:
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                else:
                    #a: 'w', b: 'w'
                    if word[1] in b:
                        #a: 'w', b: 'w', c:['*', '.', '', 'w']
                        if c == '*':
                            if word[2] != ' ':
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                        elif c == '.':
                            if word[2] == ' ':
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                        elif c == '':
                            #if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                        else:
                            if word[2] in c:
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1

    #입력한 a,b,c의 값에 맞는 정보들을 filtered_list에 저장하고
    #추출한 데이터의 원래 index 값을 filtered_index에 저장한다.
    filtered_list = []
    filtered_index = []

    #i를 indexlis에 저장한 인덱스 값들로 지정되게 for문을 돌린다.
    #result는 원본 데이터에서 해당 인덱스가 가리키는 정보를 저장한다.
    #filtered_list에는 result의 리스트 형태로 저장해 
    #column_name을 제외한 순수 데이터를 리스트 형태로 저장한다.
    for i in indexlis:
        result = df.loc[i]
        filtered_list.append(list(result))
        filtered_index.append(str(i))
    
    filtered_header = handle_df.columns.tolist()
    filtered_df = pd.DataFrame(filtered_list, columns=filtered_header)
    filtered_df.head()
    filtered_df.insert(0,'Original Index', filtered_index)

    return filtered_df

#단어의 두 번째 음절이 입력 받은 a,b,c에 해당 될 때 출력하는 함수
def Second_Syllable(df, a, b, c):
    #'*' => any consonants
    #'.' => any vowels
    #'w' => 초성, 중성, 종성에 한글이 들어 있을 때
    #''  => a,b,c에 입력이 안들어 왔을 때

    #a, b, c에 들어온 값이 +로 묶여서 들어오면 +단위로 나누어 주어
    #각각 a, b, c에 리스트 형태로 저장해준다.
    #아닌 경우는 그대로 사용한다.
    if '+' in a:
        a = a.split ('+')
    else:
        pass

    if '+' in b:
        b = b.split ('+')
    else:
        pass

    if '+' in c:
       c = c.split ('+')
    else:
        pass

    lemma = []
    for i in range(len(df)):
        lemma.append(df.loc[i,'Lemma'])

    indexlis = []
    cnt = 0

    for i in range(len(df)):
        divide = Divide(df.loc[i,'Lemma'])

        #단어의 길이가 1일 때는 Second syllable이 존재하지 않으므로
        #길이가 1 이상일때만 해당하는 단어를 찾게 한다.
        #길이가 1일 넘을 때는 word에 divide[1](두번 째 음절)을 넣어준다.
        if len(divide) > 1:
            word = divide[1]
            #a: '*'
            if a == '*':
                #a: '*', b: '.'
                if b == '.':
                    #a: '*', b: '.', c:['*', '.', '', 'w']
                    if c == '*':
                        if word[2] != ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '.':
                        if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '':
                        #if word[2] == ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                    else:
                        if word[2] in c:
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                #a: '*', b: ''
                elif b == '':
                    #a: '*', b: '', c:['*', '.', '', 'w']
                    if c == '*':
                        if word[2] != ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '.':
                        if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '':
                        #if word[2] == ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                    else:
                        if word[2] in c:
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                else:
                    #a: '*', b: 'w'
                    if word[1] in b:
                        #a: '*', b: 'w', c:['*', '.', '', 'w']
                        if c == '*':
                            if word[2] != ' ':
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                        elif c == '.':
                            if word[2] == ' ':
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                        elif c == '':
                            #if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                        else:
                            if word[2] in c:
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
        
            elif a == '.':
                break
            #a: ''
            elif a == '':
                #a: '', b: '.'
                if b == '.':
                    #a: 'w', b: 'w', c:['*', '.', '', 'w']
                    if c == '*':
                        if word[2] != ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '.':
                        if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '':
                        #if word[2] == ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                    else:
                        if word[2] in c:
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                #a: '', b: ''
                elif b == '':
                    #a: '', b: '', c:['*', '.', '', 'w']
                    if c == '*':
                        if word[2] != ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '.':
                        if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '':
                        #if word[2] == ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                    else:
                        if word[2] in c:
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                else:
                    #a: '', b: 'w'
                    if word[1] in b:
                        #a: '', b: 'w', c:['*', '.', '', 'w']
                        if c == '*':
                            if word[2] != ' ':
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                        elif c == '.':
                            if word[2] == ' ':
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                        elif c == '':
                            #if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                        else:
                            if word[2] in c:
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
            else:
                #a: 'w'
                if word[0] in a:
                    #a: 'w', b: '.'
                    if b == '.':
                        #a: 'w', b: '.', c:['*', '.', '', 'w']
                        if c == '*':
                            if word[2] != ' ':
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                        elif c == '.':
                            if word[2] == ' ':
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                        elif c == '':
                            #if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                        else:
                            if word[2] in c:
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                    #a: 'w', b: ''
                    elif b == '':
                        #a: 'w', b: '', c:['*', '.', '', 'w']
                        if c == '*':
                            if word[2] != ' ':
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                        elif c == '.':
                            if word[2] == ' ':
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                        elif c == '':
                            #if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                        else:
                            if word[2] in c:
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1

                    else:
                        #a: 'w', b: 'w'
                        if word[1] in b:
                            #a: 'w', b: 'w', c:['*', '.', '', 'w']
                            if c == '*':
                                if word[2] != ' ':
                                    indexlis.append(lemma.index(lemma[i]))
                                    cnt += 1
                            elif c == '.':
                                if word[2] == ' ':
                                    indexlis.append(lemma.index(lemma[i]))
                                    cnt += 1
                            elif c == '':
                                #if word[2] == ' ':
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                            else:
                                if word[2] in c:
                                    indexlis.append(lemma.index(lemma[i]))
                                    cnt += 1

        else:
            pass    
    
    #입력한 a,b,c의 값에 맞는 정보들을 filtered_list에 저장하고
    #추출한 데이터의 원래 index 값을 filtered_index에 저장한다.
    filtered_list = []
    filtered_index = []

    #i를 indexlis에 저장한 인덱스 값들로 지정되게 for문을 돌린다.
    #result는 원본 데이터에서 해당 인덱스가 가리키는 정보를 저장한다.
    #filtered_list에는 result의 리스트 형태로 저장해 
    #column_name을 제외한 순수 데이터를 리스트 형태로 저장한다.
    for i in indexlis:
        result = df.loc[i]
        filtered_list.append(list(result))
        filtered_index.append(str(i))
    
    filtered_header = handle_df.columns.tolist()
    filtered_df = pd.DataFrame(filtered_list, columns=filtered_header)
    filtered_df.head()
    filtered_df.insert(0,'Original Index', filtered_index)

    return filtered_df

#뒤에서 두 번째 음절이 입력받은 a,b,c에 해당 될 때 출력 하는 함수
def Second_to_Last_Syllable(df, a, b, c):
    #'*' => any consonants
    #'.' => any vowels
    #'w' => 초성, 중성, 종성에 한글이 들어 있을 때
    #''  => a,b,c에 입력이 안들어 왔을 때

    #a, b, c에 들어온 값이 +로 묶여서 들어오면 +단위로 나누어 주어
    #각각 a, b, c에 리스트 형태로 저장해준다.
    #아닌 경우는 그대로 사용한다.
    if '+' in a:
        a = a.split ('+')
    else:
        pass

    if '+' in b:
        b = b.split ('+')
    else:
        pass

    if '+' in c:
       c = c.split ('+')
    else:
        pass

    lemma = []
    for i in range(len(df)):
        lemma.append(df.loc[i,'Lemma'])

    indexlis = []
    cnt = 0
    
    for i in range(len(df)):
        divide = Divide(lemma[i])

        #단어의 길이가 1일 때는 Second_to-last_syllable이 존재하지 않으므로
        #길이가 1 이상일때만 해당하는 단어를 찾게 한다.
        #길이가 1일 넘을 때는 word에 divide[-2](뒤에서 두번 째 음절)을 넣어준다.
        if len(divide) > 1:
            word = divide[-2]
            #a: '*'
            if a == '*':
                #a : '*', b: '.'
                if b == '.':
                    #a : '*', b: '.', c:['*', '.', '', 'w']
                    if c == '*':
                        if word[2] != ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '.':
                        if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '':
                        #if word[2] == ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                    else:
                        if word[2] in c:
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                #a : '*', b: ''
                elif b == '':
                    #a : '*', b: '', c:['*', '.', '', 'w']
                    if c == '*':
                        if word[2] != ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '.':
                        if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '':
                        #if word[2] == ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                    else:
                        if word[2] in c:
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                else:
                    #a : '*', b: 'w'
                    if word[1] in b:
                        #a : '*', b: 'w', c:['*', '.', '', 'w']
                        if c == '*':
                            if word[2] != ' ':
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                        elif c == '.':
                            if word[2] == ' ':
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                        elif c == '':
                            #if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                        else:
                            if word[2] in c:
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1

            elif a == '.':
                break
            
            #a : ''
            elif a == '':
                #a: '', b: '.'
                if b == '.':
                    #a : '', b: '.', c:['*', '.', '', 'w']
                    if c == '*':
                        if word[2] != ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '.':
                        if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '':
                        #if word[2] == ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                    else:
                        if word[2] in c:
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                #a : '', b: ''
                elif b == '':
                    #a : '', b: '', c:['*', '.', '', 'w']
                    if c == '*':
                        if word[2] != ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                        elif c == '.':
                            if word[2] == ' ':
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                        else:
                            if word[2] in c:
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                #a : '', b: 'w'
                else:
                    if word[1] in b:
                        #a : '', b: 'w', c:['*', '.', '', 'w']
                        if c == '*':
                            if word[2] != ' ':
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                        elif c == '.':
                            if word[2] == ' ':
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                        elif c == '':
                            #if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                        else:
                            if word[2] in c:
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
            #a : 'w'
            else:  
                if word[0] in a:
                    #a: 'w', b: '.'
                    if b == '.':
                        #a : 'w', b: '.', c:['*', '.', '', 'w']
                        if c == '*':
                            if word[2] != ' ':
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                        elif c == '.':
                            if word[2] == ' ':
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                        elif c == '':
                            #if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                        else:
                            if word in c:
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                    #a : 'w', b: ''
                    elif b == '':
                        #a : 'w', b: '', c:['*', '.', '', 'w']
                        if c == '*':
                            if word[2] != ' ':
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                        elif c == '.':
                            if word[2] == ' ':
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                        elif c == '':
                            #if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                        else:   
                            if word[2] in c:
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                    #a: 'w', b: 'w'
                    else:
                        if word[1] in b:
                            #a : 'w', b: 'w', c:['*', '.', '', 'w']
                            if c == '*':
                                if word[2] != ' ':
                                    indexlis.append(lemma.index(lemma[i]))
                                    cnt += 1
                            elif c == '.':
                                if word[2] == ' ':
                                    indexlis.append(lemma.index(lemma[i]))
                                    cnt += 1
                            elif c == '':
                                #if word[2] == ' ':
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                            else:
                                if word[2] in c:
                                    indexlis.append(lemma.index(lemma[i]))
                                    cnt += 1

    #입력한 a,b,c의 값에 맞는 정보들을 filtered_list에 저장하고
    #추출한 데이터의 원래 index 값을 filtered_index에 저장한다.
    filtered_list = []
    filtered_index = []

    #i를 indexlis에 저장한 인덱스 값들로 지정되게 for문을 돌린다.
    #result는 원본 데이터에서 해당 인덱스가 가리키는 정보를 저장한다.
    #filtered_list에는 result의 리스트 형태로 저장해 
    #column_name을 제외한 순수 데이터를 리스트 형태로 저장한다.
    for i in indexlis:
        result = df.loc[i]
        filtered_list.append(list(result))
        filtered_index.append(str(i))
    
    filtered_header = handle_df.columns.tolist()
    filtered_df = pd.DataFrame(filtered_list, columns=filtered_header)
    filtered_df.head()
    filtered_df.insert(0,'Original Index', filtered_index)

    return filtered_df

#단어의 마지막 음절이 입력 받은 a,b,c에 해당 될 때 출력하는 함수
def Last_Syllable(df, a, b, c):
    #'*' => any consonants
    #'.' => any vowels
    #'w' => 초성, 중성, 종성에 한글이 들어 있을 때
    #''  => a,b,c에 입력이 안들어 왔을 때

    #a, b, c에 들어온 값이 +로 묶여서 들어오면 +단위로 나누어 주어
    #각각 a, b, c에 리스트 형태로 저장해준다.
    #아닌 경우는 그대로 사용한다.
    if '+' in a:
        a = a.split ('+')
    else:
        pass

    if '+' in b:
        b = b.split ('+')
    else:
        pass

    if '+' in c:
       c = c.split ('+')
    else:
        pass

    lemma = []
    for i in range(len(df)):
        lemma.append(df.loc[i,'Lemma'])

    indexlis = []
    cnt = 0


    for i in range(len(df)):
        divide = Divide(lemma[i])
        #word는 last syllable이므로 divide에 단어 길이에서 -1 한 값을 넣어준다.
        word = divide[len(divide) - 1]
        #a: '*'
        if a == '*':                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
            #a: '*', b: '.'
            if b == '.':
                #a: '*', b: '.', c:['*', '.', '', 'w']
                if c == '*':
                    if word[2] != ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                elif c == '.':
                    if word[2] == ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                elif c == '':
                    #if word[2] == ' ':
                    indexlis.append(lemma.index(lemma[i]))
                    cnt += 1
                else:
                    if word[2] in c:
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
            #a: '*', b: ''
            elif b == '':
                #a: '*', b: '', c:['*', '.', '', 'w']
                if c == '*':
                    if word[2] != ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                elif c == '.':
                    if word[2] == ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                elif c == '':
                    #if word[2] == ' ':
                    indexlis.append(lemma.index(lemma[i]))
                    cnt += 1
                else:
                    if word[2] in c:
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
            #a: '*', b: 'w'
            else:
                if word[1] in b:
                    #a: '*', b: 'w', c:['*', '.', '', 'w'] 
                    if c == '*':
                        if word[2] != ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '.':
                        if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '':
                        #if word[2] == ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                    else:
                        if word[2] in c:
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
    
        elif a == '.':
            break

        #a: ''
        elif a == '':
            #a: '*', b: '.'
            if b == '.':
                #a: '*', b: '.', c:['*', '.', '', 'w']
                if c == '*':
                    if word[2] != ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                elif c == '.':
                    if word[2] == ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                elif c == '':
                    #if word[2] == ' ':
                    indexlis.append(lemma.index(lemma[i]))
                    cnt += 1
                else:
                    if word[2] in c:
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
            #a: '*', b: ''
            elif b == '':
                #a: '*', b: '', c:['*', '.', '', 'w']
                if c == '*':
                    if word[2] != ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                elif c == '.':
                    if word[2] == ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                elif c == '':
                    #if word[2] == ' ':
                    indexlis.append(lemma.index(lemma[i]))
                    cnt += 1
                else:
                    if word[2] in c:
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
            #a: '*', b: 'w'
            else:
                if word[1] in b:
                    #a: '*', b: '.', c:['*', '.', '', 'w']
                    if c == '*':
                        if word[2] != ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '.':
                        if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '':
                        #if word[2] == ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                    else:
                        if word[2] in c:
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
        #a: 'w'
        else:  
            if word[0] in a:
                #a: 'w', b: '.'
                if b == '.':
                    #a: 'w', b: '.', c:['*', '.', '', 'w']
                    if c == '*':
                        if word[2] != ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '.':
                        if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '':
                        #if word[2] == ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                    else:
                        if word[2] in c:
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                #a: 'w', b: ''
                elif b == '':
                    #a: 'w', b: '', c:['*', '.', '', 'w']
                    if c == '*':
                        if word[2] != ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '.':
                        if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    elif c == '':
                        #if word[2] == ' ':
                        indexlis.append(lemma.index(lemma[i]))
                        cnt += 1
                    else:
                        if word[2] in c:
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                    #a: 'w', b: 'w', c:['*', '.', '', 'w']
                else:
                    if word[1] in b:
                        if c == '*':
                            if word[2] != ' ':
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                        elif c == '.':
                            if word[2] == ' ':
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1
                        elif c == '':
                            #if word[2] == ' ':
                            indexlis.append(lemma.index(lemma[i]))
                            cnt += 1
                        else:
                            if word[2] in c:
                                indexlis.append(lemma.index(lemma[i]))
                                cnt += 1

    #입력한 a,b,c의 값에 맞는 정보들을 filtered_list에 저장하고
    #추출한 데이터의 원래 index 값을 filtered_index에 저장한다.
    filtered_list = []
    filtered_index = []

    #i를 indexlis에 저장한 인덱스 값들로 지정되게 for문을 돌린다.
    #result는 원본 데이터에서 해당 인덱스가 가리키는 정보를 저장한다.
    #filtered_list에는 result의 리스트 형태로 저장해 
    #column_name을 제외한 순수 데이터를 리스트 형태로 저장한다.
    for i in indexlis:
        result = df.loc[i]
        filtered_list.append(list(result))
        filtered_index.append(str(i))
    
    filtered_header = handle_df.columns.tolist()
    filtered_df = pd.DataFrame(filtered_list, columns=filtered_header)
    filtered_df.head()
    filtered_df.insert(0,'Original Index', filtered_index)

    return filtered_df

class Ui_Deco_LexO (object):
    def setupUi(self, Deco_LexO):
        Deco_LexO.setObjectName ("Deco_LexO")
        Deco_LexO.resize (709, 732)
        self.centralwidget = QtWidgets.QWidget (Deco_LexO)
        self.centralwidget.setObjectName ("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout (self.centralwidget)
        self.gridLayout.setObjectName ("gridLayout")
        self.dataFrame_Tab = QtWidgets.QTabWidget (self.centralwidget)
        self.dataFrame_Tab.setObjectName ("dataFrame_Tab")
        self.tab = QtWidgets.QWidget ()
        self.tab.setObjectName ("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout (self.tab)
        self.gridLayout_2.setObjectName ("gridLayout_2")
        self.tableWidget = QtWidgets.QTableWidget (self.tab)
        self.tableWidget.setObjectName ("tableWidget")
        self.tableWidget.setColumnCount (0)
        self.tableWidget.setRowCount (0)
        self.gridLayout_2.addWidget (self.tableWidget, 0, 0, 1, 1)
        self.dataFrame_Tab.addTab (self.tab, "")
        self.gridLayout.addWidget (self.dataFrame_Tab, 0, 1, 1, 1)
        self.tabWidget_1 = QtWidgets.QTabWidget (self.centralwidget)
        self.tabWidget_1.setMaximumSize (QtCore.QSize (328, 16777215))
        self.tabWidget_1.setObjectName ("tabWidget_1")
        self.Modifying_Tab = QtWidgets.QWidget ()
        self.Modifying_Tab.setObjectName ("Modifying_Tab")

        self.FEntryCombo = QtWidgets.QComboBox (self.Modifying_Tab)
        self.FEntryCombo.setGeometry (QtCore.QRect (30, 40, 81, 21))
        self.FEntryCombo.setObjectName ("FEntryCombo")
        self.FEntryCombo.addItem ("")
        self.FEntryCombo.setItemText (0, "")
        self.FEntryCombo.addItem ("")
        self.FEntryCombo.addItem ("")
        self.FEntryCombo.addItem ("")
        self.FEntryCombo.addItem ("")
        self.FEntryCombo.addItem ("")
        self.FEntry_Input = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FEntry_Input.setGeometry (QtCore.QRect (120, 40, 141, 21))
        self.FEntry_Input.setObjectName ("FEntry_Input")

        self.FLemma_Input = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FLemma_Input.setGeometry (QtCore.QRect (120, 100, 141, 21))
        self.FLemma_Input.setObjectName ("FLemma_Input")
        self.FLemmaCombo = QtWidgets.QComboBox (self.Modifying_Tab)
        self.FLemmaCombo.addItem ("")
        self.FLemmaCombo.setItemText (0, "")
        self.FLemmaCombo.addItem ("a")
        self.FLemmaCombo.addItem ("")
        self.FLemmaCombo.addItem ("")
        self.FLemmaCombo.addItem ("")
        self.FLemmaCombo.addItem ("")
        self.FLemmaCombo.setGeometry (QtCore.QRect (30, 100, 81, 21))
        self.FLemmaCombo.setObjectName ("FLemmaCombo")

        self.FCateCombo = QtWidgets.QComboBox (self.Modifying_Tab)
        self.FCateCombo.setGeometry (QtCore.QRect (30, 160, 81, 21))
        self.FCateCombo.addItem ("")
        self.FCateCombo.setItemText (0, "")
        self.FCateCombo.addItem ("")
        self.FCateCombo.addItem ("")
        self.FCateCombo.addItem ("")
        self.FCateCombo.addItem ("")
        self.FCateCombo.addItem ("")
        self.FCateCombo.setObjectName ("FCateCombo")
        self.FCate_Input = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FCate_Input.setGeometry (QtCore.QRect (120, 160, 141, 21))
        self.FCate_Input.setObjectName ("FCate_Input")

        #First Syllable
        self.FFirst_1 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FFirst_1.setGeometry (QtCore.QRect (30, 320, 51, 21))
        self.FFirst_1.setObjectName ("FFirst_1")
        self.FFirst_2 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FFirst_2.setGeometry (QtCore.QRect (100, 320, 51, 21))
        self.FFirst_2.setObjectName ("FFirst_2")
        self.FFirst_3 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FFirst_3.setGeometry (QtCore.QRect (170, 320, 51, 21))
        self.FFirst_3.setObjectName ("FFirst_3")
        
        #Second Syllable
        self.FSec_3 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FSec_3.setGeometry (QtCore.QRect (170, 370, 51, 21))
        self.FSec_3.setObjectName ("FSec_3")
        self.FSec_2 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FSec_2.setGeometry (QtCore.QRect (100, 370, 51, 21))
        self.FSec_2.setObjectName ("FSec_2")
        self.FSec_1 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FSec_1.setGeometry (QtCore.QRect (30, 370, 51, 21))
        self.FSec_1.setObjectName ("FSec_1")

        #Second to last syllable
        self.FSecL_3 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FSecL_3.setGeometry (QtCore.QRect (170, 420, 51, 21))
        self.FSecL_3.setObjectName ("FSecL_3")
        self.FSecL_2 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FSecL_2.setGeometry (QtCore.QRect (100, 420, 51, 21))
        self.FSecL_2.setObjectName ("FSecL_2")
        self.FSecL_1 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FSecL_1.setGeometry (QtCore.QRect (30, 420, 51, 21))
        self.FSecL_1.setObjectName ("FSecL_1")

        #Last syllable
        self.FLast_3 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FLast_3.setGeometry (QtCore.QRect (170, 470, 51, 21))
        self.FLast_3.setObjectName ("FLast_3")
        self.FLast_2 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FLast_2.setGeometry (QtCore.QRect (100, 470, 51, 21))
        self.FLast_2.setObjectName ("FLast_2")
        self.FLast_1 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FLast_1.setGeometry (QtCore.QRect (30, 470, 51, 21))
        self.FLast_1.setObjectName ("FLast_1")

        self.FPhonoFrame = QtWidgets.QFrame (self.Modifying_Tab)
        self.FPhonoFrame.setGeometry (QtCore.QRect (10, 290, 281, 251))
        self.FPhonoFrame.setFrameShape (QtWidgets.QFrame.Box)
        self.FPhonoFrame.setFrameShadow (QtWidgets.QFrame.Raised)
        self.FPhonoFrame.setObjectName ("FPhonoFrame")
        self.FColCombo = QtWidgets.QComboBox (self.FPhonoFrame)
        self.FColCombo.setGeometry (QtCore.QRect (90, 220, 81, 21))
        self.FColCombo.setObjectName ("FColCombo")
        self.label_7 = QtWidgets.QLabel (self.FPhonoFrame)
        self.label_7.setGeometry (QtCore.QRect (20, 50, 211, 31))
        self.label_7.setObjectName ("label_7")
        self.label_8 = QtWidgets.QLabel (self.FPhonoFrame)
        self.label_8.setGeometry (QtCore.QRect (20, 100, 211, 31))
        self.label_8.setObjectName ("label_8")
        self.label_9 = QtWidgets.QLabel (self.FPhonoFrame)
        self.label_9.setGeometry (QtCore.QRect (20, 0, 191, 31))
        self.label_9.setObjectName ("label_9")
        self.label_6 = QtWidgets.QLabel (self.FPhonoFrame)
        self.label_6.setGeometry (QtCore.QRect (20, 150, 211, 31))
        self.label_6.setObjectName ("label_6")
        self.label_10 = QtWidgets.QLabel (self.FPhonoFrame)
        self.label_10.setGeometry (QtCore.QRect (10, 220, 61, 21))
        self.label_10.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName ("label_10")

        #filter button
        self.FFiltering_Button = QtWidgets.QPushButton (self.Modifying_Tab)
        self.FFiltering_Button.setGeometry (QtCore.QRect (20, 550, 75, 23))
        self.FFiltering_Button.setObjectName ("FFiltering_Button")

        #show all button
        self.FShow_Button = QtWidgets.QPushButton (self.Modifying_Tab)
        self.FShow_Button.setGeometry (QtCore.QRect (110, 550, 75, 23))
        self.FShow_Button.setObjectName ("FShow_Button")

        #clear button
        self.FClear_Button = QtWidgets.QPushButton (self.Modifying_Tab)
        self.FClear_Button.setGeometry (QtCore.QRect (210, 550, 75, 23))
        self.FClear_Button.setObjectName ("FClear_Button")

        self.label = QtWidgets.QLabel (self.Modifying_Tab)
        self.label.setGeometry (QtCore.QRect (30, 10, 56, 21))
        self.label.setObjectName ("label")
        self.label_2 = QtWidgets.QLabel (self.Modifying_Tab)
        self.label_2.setGeometry (QtCore.QRect (30, 70, 56, 21))
        self.label_2.setObjectName ("label_2")
        self.label_3 = QtWidgets.QLabel (self.Modifying_Tab)
        self.label_3.setGeometry (QtCore.QRect (30, 130, 56, 21))
        self.label_3.setObjectName ("label_3")
        self.FInfo_Input = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FInfo_Input.setGeometry (QtCore.QRect (120, 220, 141, 21))
        self.FInfo_Input.setObjectName ("FInfo_Input")
        self.label_4 = QtWidgets.QLabel (self.Modifying_Tab)
        self.label_4.setGeometry (QtCore.QRect (30, 190, 81, 21))
        self.label_4.setObjectName ("label_4")

        self.FInfoCombo = QtWidgets.QComboBox (self.Modifying_Tab)
        self.FInfoCombo.setGeometry (QtCore.QRect (30, 220, 81, 21))
        self.FInfoCombo.addItem ("")
        self.FInfoCombo.setItemText (0, "")
        self.FInfoCombo.addItem ("")
        self.FInfoCombo.addItem ("")
        self.FInfoCombo.addItem ("")
        self.FInfoCombo.addItem ("")
        self.FInfoCombo.addItem ("")
        self.FInfoCombo.setObjectName ("FInfoCombo")

        self.label_5 = QtWidgets.QLabel (self.Modifying_Tab)
        self.label_5.setGeometry (QtCore.QRect (10, 270, 141, 31))
        font = QtGui.QFont ()
        font.setBold (True)
        font.setWeight (75)
        self.label_5.setFont (font)
        self.label_5.setObjectName ("label_5")

        self.FPhonoFrame.raise_()
        self.FEntryCombo.raise_()
        self.FEntry_Input.raise_()
        self.FLemma_Input.raise_()
        self.FLemmaCombo.raise_()
        self.FCateCombo.raise_()
        self.FCate_Input.raise_()
        self.FFirst_1.raise_()
        self.FFirst_2.raise_()
        self.FFirst_3.raise_()
        self.FSec_3.raise_()
        self.FSec_2.raise_()
        self.FSec_1.raise_()
        self.FSecL_3.raise_()
        self.FSecL_2.raise_()
        self.FSecL_1.raise_()
        self.FLast_3.raise_()
        self.FLast_2.raise_()
        self.FLast_1.raise_()
        self.FFiltering_Button.raise_()
        self.FShow_Button.raise_()
        self.FClear_Button.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.FInfo_Input.raise_()
        self.label_4.raise_()
        self.FInfoCombo.raise_()
        self.label_5.raise_()

        self.tabWidget_1.addTab (self.Modifying_Tab, "")
        self.tab_2 = QtWidgets.QWidget ()
        self.tab_2.setObjectName ("tab_2")
        self.tabWidget_1.addTab (self.tab_2, "")
        self.gridLayout.addWidget (self.tabWidget_1, 0, 0, 1, 1)
        Deco_LexO.setCentralWidget (self.centralwidget)
        self.menubar = QtWidgets.QMenuBar (Deco_LexO)
        self.menubar.setGeometry (QtCore.QRect (0, 0, 709, 21))
        self.menubar.setObjectName ("menubar")
        self.menuFile = QtWidgets.QMenu (self.menubar)
        self.menuFile.setObjectName ("menuFile")
        self.menuRecent_files = QtWidgets.QMenu (self.menuFile)
        self.menuRecent_files.setObjectName ("menuRecent_files")
        self.menuHelp = QtWidgets.QMenu (self.menubar)
        self.menuHelp.setObjectName ("menuHelp")
        Deco_LexO.setMenuBar (self.menubar)
        self.actionOpen_file_s = QtWidgets.QAction (Deco_LexO)
        self.actionOpen_file_s.setShortcutContext (QtCore.Qt.WindowShortcut)
        self.actionOpen_file_s.setObjectName ("actionOpen_file_s")
        self.actionNone = QtWidgets.QAction (Deco_LexO)
        self.actionNone.setObjectName ("actionNone")
        self.actionSave = QtWidgets.QAction (Deco_LexO)
        self.actionSave.setObjectName ("actionSave")
        self.actionSave_file_as = QtWidgets.QAction (Deco_LexO)
        self.actionSave_file_as.setObjectName ("actionSave_file_as")
        self.actionQuit = QtWidgets.QAction (Deco_LexO)
        self.actionQuit.setObjectName ("actionQuit") 
        self.actionAcknowledgement = QtWidgets.QAction (Deco_LexO)
        self.actionAcknowledgement.setObjectName ("actionAcknowledgement")
        self.actionAbout_DecoLexO = QtWidgets.QAction (Deco_LexO)
        self.actionAbout_DecoLexO.setObjectName ("actionAbout_DecoLexO")
        self.menuRecent_files.addAction (self.actionNone)
        self.menuFile.addAction (self.actionOpen_file_s)
        self.menuFile.addAction (self.menuRecent_files.menuAction ())
        self.menuFile.addSeparator ()
        self.menuFile.addAction (self.actionSave)
        self.menuFile.addAction (self.actionSave_file_as)
        self.menuFile.addSeparator ()
        self.menuFile.addAction (self.actionQuit)
        self.menuHelp.addAction (self.actionAcknowledgement)
        self.menuHelp.addSeparator ()
        self.menuHelp.addAction (self.actionAbout_DecoLexO)
        self.menubar.addAction (self.menuFile.menuAction ())
        self.menubar.addAction (self.menuHelp.menuAction ())
        
        self.retranslateUi (Deco_LexO)
        self.dataFrame_Tab.setCurrentIndex (1)
        self.tabWidget_1.setCurrentIndex (0)
        QtCore.QMetaObject.connectSlotsByName (Deco_LexO)

        self.FShow_Button.released.connect (self.show_all)
        self.FFiltering_Button.released.connect (self.filter_function)
        self.FClear_Button.released.connect(self.phonological_shape)

    def retranslateUi(self, Deco_LexO):
        # Entry, lemma, category, information을 입력하면 각각 statelis에 저장한다.
        _translate = QtCore.QCoreApplication.translate
        Deco_LexO.setWindowTitle (_translate ("Deco_LexO", "Deco-LexO"))
        self.dataFrame_Tab.setTabText (self.dataFrame_Tab.indexOf (self.tab), _translate ("Deco_LexO", "Tab 1"))
        self.FEntryCombo.setItemText (1, _translate ("Deco_LexO", "Equals"))
        self.FEntryCombo.setItemText (2, _translate ("Deco_LexO", "Starts with"))
        self.FEntryCombo.setItemText (3, _translate ("Deco_LexO", "Ends with"))
        self.FEntryCombo.setItemText (4, _translate ("Deco_LexO", "Contains"))
        self.FEntryCombo.setItemText (5, _translate ("Deco_LexO", "is empty"))

        self.FLemmaCombo.setItemText (1, _translate ("Deco_LexO", "Equals"))
        self.FLemmaCombo.setItemText (2, _translate ("Deco_LexO", "Starts with"))
        self.FLemmaCombo.setItemText (3, _translate ("Deco_LexO", "Ends with"))
        self.FLemmaCombo.setItemText (4, _translate ("Deco_LexO", "Contains"))
        self.FLemmaCombo.setItemText (5, _translate ("Deco_LexO", "is empty"))

        self.FCateCombo.setItemText (1, _translate ("Deco_LexO", "Equals"))
        self.FCateCombo.setItemText (2, _translate ("Deco_LexO", "Starts with"))
        self.FCateCombo.setItemText (3, _translate ("Deco_LexO", "Ends with"))
        self.FCateCombo.setItemText (4, _translate ("Deco_LexO", "Contains"))
        self.FCateCombo.setItemText (5, _translate ("Deco_LexO", "is empty"))

        self.FInfoCombo.setItemText (1, _translate ("Deco_LexO", "Equals"))
        self.FInfoCombo.setItemText (2, _translate ("Deco_LexO", "Starts with"))
        self.FInfoCombo.setItemText (3, _translate ("Deco_LexO", "Ends with"))
        self.FInfoCombo.setItemText (4, _translate ("Deco_LexO", "Contains"))
        self.FInfoCombo.setItemText (5, _translate ("Deco_LexO", "is empty"))

        self.label_7.setText (_translate ("Deco_LexO", "Second syllable:"))
        self.label_8.setText (_translate ("Deco_LexO", "Second-to-last syllable:"))
        self.label_9.setText (_translate ("Deco_LexO", "First syllable:"))
        self.label_6.setText (_translate ("Deco_LexO", "Last syllable:"))
        self.label_10.setText (_translate ("Deco_LexO", "Column:"))
        self.FFiltering_Button.setText (_translate ("Deco_LexO", "Filter"))
        self.FShow_Button.setText (_translate ("Deco_LexO", "Show all"))
        self.FClear_Button.setText (_translate ("Deco_LexO", "Clear"))
        self.label.setText (_translate ("Deco_LexO", "Entry:"))
        self.label_2.setText (_translate ("Deco_LexO", "Lemma:"))
        self.label_3.setText (_translate ("Deco_LexO", "Category:"))
        self.label_4.setText (_translate ("Deco_LexO", "Information:"))
        self.label_5.setText (_translate ("Deco_LexO", "Phonological shape"))
        self.tabWidget_1.setTabText (self.tabWidget_1.indexOf (self.Modifying_Tab), _translate ("Deco_LexO", "Filter"))
        self.tabWidget_1.setTabText (self.tabWidget_1.indexOf (self.tab_2), _translate ("Deco_LexO", "Edit"))
        self.menuFile.setTitle (_translate ("Deco_LexO", "File"))
        self.menuRecent_files.setTitle (_translate ("Deco_LexO", "Recent files"))
        self.menuHelp.setTitle (_translate ("Deco_LexO", "Help"))
        self.actionOpen_file_s.setText (_translate ("Deco_LexO", "Open files..."))
        self.actionOpen_file_s.setShortcut (_translate ("Deco_LexO", "Ctrl+O"))
        self.actionNone.setText (_translate ("Deco_LexO", "None"))
        self.actionSave.setText (_translate ("Deco_LexO", "Save file"))
        self.actionSave.setShortcut (_translate ("Deco_LexO", "Ctrl+S"))
        self.actionSave_file_as.setText (_translate ("Deco_LexO", "Save file as..."))
        self.actionSave_file_as.setShortcut (_translate ("Deco_LexO", "Ctrl+Shift+S"))
        self.actionQuit.setText (_translate ("Deco_LexO", "Quit"))
        self.actionQuit.setShortcut (_translate ("Deco_LexO", "Ctrl+Q"))
        self.actionAcknowledgement.setText (_translate ("Deco_LexO", "Acknowledgement"))
        self.actionAbout_DecoLexO.setText (_translate ("Deco_LexO", "About DecoLexO"))
        self.actionOpen_file_s.triggered.connect (self.openFiles)

    # 함수를 읽어 주느 함수
    def readFiles(self, new_tableWidget, vis_df):
        for i in range (len (vis_df.index)):
            for j in range (len (vis_df.columns)):
                self.new_tableWidget.setItem (i, j, QtWidgets.QTableWidgetItem (str (vis_df.iat[i, j])))

        self.new_tableWidget.resizeColumnsToContents ()
        self.new_tableWidget.resizeRowsToContents ()

    def readFiles2(self, vis_df):
        self.new_tableWidget.setColumnCount (0)
        self.new_tableWidget.setRowCount (0)
        self.new_tableWidget.setColumnCount (len (vis_df.columns))
        header = vis_df.columns
        self.new_tableWidget.setHorizontalHeaderLabels (header)
        self.new_tableWidget.setRowCount (len (vis_df.index))
        for i in range (len (vis_df.index)):
            for j in range (len (vis_df.columns)):
                self.new_tableWidget.setItem (i, j, QtWidgets.QTableWidgetItem (str (vis_df.iat[i, j])))

        self.new_tableWidget.resizeColumnsToContents ()
        self.new_tableWidget.resizeRowsToContents ()

    def openFiles(self):
        global handle_df
        fname = QtWidgets.QFileDialog.getOpenFileName ()
        self.new_tab = QtWidgets.QWidget ()
        self.new_tab.setObjectName ("new_tab")
        self.gridLayout_2 = QtWidgets.QGridLayout (self.new_tab)
        self.gridLayout_2.setObjectName ("gridLayout_2")
        self.new_tableWidget = QtWidgets.QTableWidget (self.new_tab)
        self.new_tableWidget.setObjectName ("new_tableWidget")
        self.new_tableWidget.setColumnCount (0)
        self.new_tableWidget.setRowCount (0)
        self.gridLayout_2.addWidget (self.new_tableWidget, 0, 1, 1, 1)
        self.dataFrame_Tab.addTab (self.new_tab, "")
        self.dataFrame_Tab.addTab (self.new_tab, str (fname).split ("', '")[0][2:])
        Ofileloc = str (fname).split ("', '")[0][2:]
        # 함수를 읽어 주느 함수
        original_read = pd.read_csv (Ofileloc, encoding='utf-8-sig')
        self.original_df = column_name (original_read)
        handle_df = self.original_df.copy ()
        self.new_tableWidget.setColumnCount (len (handle_df.columns))
        header = self.original_df.columns
        self.new_tableWidget.setHorizontalHeaderLabels (header)
        self.new_tableWidget.setRowCount (len (handle_df.index))
        self.readFiles (self.new_tableWidget, handle_df)

    def filter_function(self):
        
        #Lemma에 찾고자 하는 정보가 들어왔을 때 실행 되는 코드
        if self.FLemma_Input.text () != '':
            statelis = [0]
            FComboDict = {'Equals': 1, 'Starts with': 2, 'Ends with': 3, 'Contains': 4, 'is empty': 5}
            #LemmaCombo박스에 선택된 것을 보고 Equal, start, End, contain, empty를 판별하여
            # 해당 단어의 value값을 statelis에 넣어준다.  
            statelis.insert (0, FComboDict[self.FLemmaCombo.currentText ()])

            #statelis에 있는 value값에 따라 해당 코드를 실행시켜준다.
            if statelis[0] == 1:
                filtered_df = Equals (handle_df, 'Lemma', self.FLemma_Input.text ())
            if statelis[0] == 2:
                filtered_df = Starts_With (handle_df, 'Lemma', self.FLemma_Input.text ())
            if statelis[0] == 3:
                filtered_df = Ends_With (handle_df, 'Lemma', self.FLemma_Input.text())
            if statelis[0] == 4:
                filtered_df = Contains (handle_df, 'Lemma', self.FLemma_Input.text())
            if statelis[0] == 5:
                filtered_df = Is_Empty (handle_df, 'Lemma', self.FLemma_Input.text())

            self.readFiles2 (filtered_df)
        
        #Entry에 찾고자 하는 정보가 들어왔을 때 실행 되는 코드
        if self.FEntry_Input.text () != '':
            statelis = [0]
            FComboDict = {'Equals': 1, 'Starts with': 2, 'Ends with': 3, 'Contains': 4, 'is empty': 5}
            statelis.insert (0, FComboDict[self.FEntryCombo.currentText ()])
            
            if statelis[0] == 1:
                filtered_df = Equals (handle_df, 'Entry', self.FEntry_Input.text ())
            if statelis[0] == 2:
                filtered_df = Starts_With (handle_df, 'Entry', self.FEntry_Input.text ())
            if statelis[0] == 3:
                filtered_df = Ends_With (handle_df, 'Entry', self.FEntry_Input.text())
            if statelis[0] == 4:
                filtered_df = Contains (handle_df, 'Entry', self.FEntry_Input.text())
            if statelis[0] == 5:
                filtered_df = Is_Empty (handle_df, 'Entry', self.FEntry_Input.text())

            self.readFiles2 (filtered_df)
        

        #Category에 원하는 정보가 들어왔을 때 실행되는 코드
        if self.FCate_Input.text () != '':
            statelis = [0]
            FComboDict = {'Equals': 1, 'Starts with': 2, 'Ends with': 3, 'Contains': 4, 'is empty': 5}
            statelis.insert (0, FComboDict[self.FCateCombo.currentText ()])
            
            if statelis[0] == 1:
                filtered_df = Equals (handle_df, 'Category', self.FCate_Input.text ())
            if statelis[0] == 2:
                filtered_df = Starts_With (handle_df, 'Category', self.FCate_Input.text ())
            if statelis[0] == 3:
                filtered_df = Ends_With (handle_df, 'Category', self.FCate_Input.text())
            if statelis[0] == 4:
                filtered_df = Contains (handle_df, 'Category', self.FCate_Input.text())
            if statelis[0] == 5:
                filtered_df = Is_Empty (handle_df, 'Category', self.FCate_Input.text())

            self.readFiles2 (filtered_df)
        
        if self.FInfo_Input.text () != '':
            statelis = [0]
            FComboDict = {'Equals': 1, 'Starts with': 2, 'Ends with': 3, 'Contains': 4, 'is empty': 5}
            statelis.insert (0, FComboDict[self.FLemmaCombo.currentText ()])
            
            if statelis[0] == 1:
                filtered_df = Equals (handle_df, 'Lemma', self.FLemma_Input.text ())
            if statelis[0] == 2:
                filtered_df = Starts_With (handle_df, 'Lemma', self.FLemma_Input.text ())
            if statelis[0] == 3:
                filtered_df = Ends_With (handle_df, 'Lemma', self.FLemma_Input.text())
            if statelis[0] == 4:
                filtered_df = Contains (handle_df, 'Lemma', self.FLemma_Input.text())
            if statelis[0] == 5:
                filtered_df = Is_Empty (handle_df, 'Lemma', self.FLemma_Input.text())

            self.readFiles2 (filtered_df)

    #show버튼을 누르면 원본 데이터를 보여주는 함수
    def show_all(self):
        self.readFiles2 (self.original_df)


    def phonological_shape(self):

        if self.FFirst_1.text() != '' or self.FFirst_2.text() != '' or self.FFirst_3.text() != '':
            handle_df = First_Syllable(handle_df, self.FFirst_1.text(), self.FFirst_2.text(), self.FFirst_3.text())

            self.readFiles2 (handle_df)
        
        if self.FSec_1.text() != '' or self.FSec_2.text() != '' or self.FSec_3.text() != '':
            handle_df = Second_Syllable(handle_df, self.FSec_1.text(), self.FSec_2.text(), self.FSec_3.text())

            self.readFiles2 (handle_df)
        
        if self.FSecL_1.text() != '' or self.FSecL_2.text() != '' or self.FSecL_3.text() != '':
            handle_df = Second_to_Last_Syllable(handle_df, self.FSecL_1.text(), self.FSecL_2.text(), self.FSecL_3.text())

            self.readFiles2 (handle_df)
        
        if self.FLast_1.text() != '' or self.FLast_2.text() != '' or self.FLast_3.text() != '':
            handle_df = Last_Syllable(handle_df, self.FLast_1.text(), self.FLast_2.text(), self.FLast_3.text())

            self.readFiles2 (handle_df)
    

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication (sys.argv)
    Deco_LexO = QtWidgets.QMainWindow ()
    ui = Ui_Deco_LexO ()
    ui.setupUi (Deco_LexO)
    Deco_LexO.show ()
    sys.exit (app.exec_ ())