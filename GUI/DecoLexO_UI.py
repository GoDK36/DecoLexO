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
from collections import OrderedDict

#tab_nme list
#열린 탭의 이름을 저장하는 리스트
tab_name_list = []

#original df list
#열린 df의 원본 파일을 저장하는 리스트
original_df_list = []


#tab_name dictionary
tab_name_dic = {}

#handle_df list
#처리한 df의 데이터를 저장하는 리스트
handle_df_list = []

#new_table list
new_table_list = []


##Function Code##
#df을 입력받아 column name들을 지정해주고 df화 해주는 작업을 하는 함수
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

#####################################################################
# filter part에서 Euals, Starts with, Contains, Ends With, Is Empty #
# 부분을 만들어 내는 함수                                            #
#####################################################################

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

    # result는 series로 저장되어 있기 때문에 to_frame()으로 df화 해주고
    # 현재 row와 column이 바뀌어 저장되어 있기 때문에
    # .T로 transepose() 기능을 주어 row와 column을 바꾸어 준다.
    filtered_header = handle_df.columns.tolist()
    filtered_df = pd.DataFrame(filtered_list, columns=filtered_header)
    filtered_df.head()

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

    # result는 series로 저장되어 있기 때문에 to_frame()으로 df화 해주고
    # 현재 row와 column이 바뀌어 저장되어 있기 때문에
    # .T로 transepose() 기능을 주어 row와 column을 바꾸어 준다.
    filtered_header = handle_df.columns.tolist()
    filtered_df = pd.DataFrame(filtered_list, columns=filtered_header)
    filtered_df.head()

    return filtered_df

#입력받은 단어로 시작하는 단어를 찾아내는 함수
def Starts_With(df, col, word):
    if '+' in word:
            word_list = word.split ('+')
    else:
        word_list = []
        word_list.append (word)
    
    #filtered_list에는 찾고자하는 요소에 매칭되는 단어들을 저장할 것이고
    #filtered_index에는 원본 데이터에 있는 찾은 단어의 인덱스를 저장할 것이다.
    filtered_list = []


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
            if df.loc[j, col].startswith (word_list[i]):
                result = df.iloc[j]
                filtered_list.append(list(result))
            

    # result는 series로 저장되어 있기 때문에 to_frame()으로 df화 해주고
    # 현재 row와 column이 바뀌어 저장되어 있기 때문에
    # .T로 transepose() 기능을 주어 row와 column을 바꾸어 준다.
    filtered_header = handle_df.columns.tolist()
    filtered_df = pd.DataFrame(filtered_list, columns=filtered_header)
    filtered_df.head()

    return filtered_df

#입력 받은 단어로 끝나는 단어를 찾아내는 함수
def Ends_With(df, col, word):
    if '+' in word:
            word_list = word.split ('+')
    else:
        word_list = []
        word_list.append (word)
    
    #filtered_list에는 찾고자하는 요소에 매칭되는 단어들을 저장할 것이고
    #filtered_index에는 원본 데이터에 있는 찾은 단어의 인덱스를 저장할 것이다.
    filtered_list = []

    #i는 word_list에 저장된 단어의 개수를 길이로 설정하고
    #j는 원본데이터의 행의 개수를 길이로 설정한다.
    #df는 원본데이터, col은 찾고자 하는 정보(Lemma, Entry, Catgory..), word는 찾고자 하는 단어.
    #df.loc[j, col] => 열마다 돌아가면서 해당 정보와 찾고자 하는 단어로 끝나면
    #answer에 일치 정보의 열을 통째로 저장해준다.
    #이때는 시리즈 형태로 저장되어 있기 때문에 filtered_list에 answer을 list화 한 정보를 넣어주면
    #컬럼 정보는 제외된 순수 데이터 정보만 filteres_list에 저장이된다.
    #filtered_index에는 gui상에서 원본 인덱스보다 +1 된 값으로 나오기 때문에 
    #찾은 데이터의 인덱스 값을 +1해서 넣어준다.
    for i in range (len (word_list)):
        for j in range (len (df)):
            if df.loc[j, col].endswith (word_list[i]):
                result = df.iloc[j]
                filtered_list.append(list(result))

    # result는 series로 저장되어 있기 때문에 to_frame()으로 df화 해주고
    # 현재 row와 column이 바뀌어 저장되어 있기 때문에
    # .T로 transepose() 기능을 주어 row와 column을 바꾸어 준다.
    filtered_header = handle_df.columns.tolist()
    filtered_df = pd.DataFrame(filtered_list, columns=filtered_header)
    filtered_df.head()

    return filtered_df

#입력 받은 단어를 포함하지 않는 단어를 찾아내는 함수
def Is_Empty(df, col, word):
    if '+' in word:
            word_list = word.split ('+')
    else:
        word_list = []
        word_list.append (word)
    
    #filtered_list에는 찾고자하는 요소에 매칭되는 단어들을 저장할 것이고
    #filtered_index에는 원본 데이터에 있는 찾은 단어의 인덱스를 저장할 것이다.
    filtered_list = []

    #i는 word_list에 저장된 단어의 개수를 길이로 설정하고
    #j는 원본데이터의 행의 개수를 길이로 설정한다.
    #df는 원본데이터, col은 찾고자 하는 정보(Lemma, Entry, Catgory..), word는 찾고자 하는 단어.
    #df.loc[j, col] => 열마다 돌아가면서 해당 정보와 찾고자 하는 단어가 없으면
    #answer에 일치 정보의 열을 통째로 저장해준다.
    #이때는 시리즈 형태로 저장되어 있기 때문에 filtered_list에 answer을 list화 한 정보를 넣어주면
    #컬럼 정보는 제외된 순수 데이터 정보만 filteres_list에 저장이된다.
    #filtered_index에는 gui상에서 원본 인덱스보다 +1 된 값으로 나오기 때문에 
    #찾은 데이터의 인덱스 값을 +1해서 넣어준다.
    for i in range (len (word_list)):
        for j in range (len (df)):
            if word_list[i] not in df.loc[j, col]:
                result = df.iloc[j]
                filtered_list.append(list(result))

    # result는 series로 저장되어 있기 때문에 to_frame()으로 df화 해주고
    # 현재 row와 column이 바뀌어 저장되어 있기 때문에
    # .T로 transepose() 기능을 주어 row와 column을 바꾸어 준다.
    filtered_header = handle_df.columns.tolist()
    filtered_df = pd.DataFrame(filtered_list, columns=filtered_header)
    filtered_df.head()

    return filtered_df


######################################################################
# filter part에서 phonological 부분 중 초성 중성 종성이 입력 되었을 때 #
# 해당 음소들을 가진 단어를 찾아낼 때와                                #
# Edit part에서 원하는 음소를 편집하고 싶을 때 해당 음소를 가진 단어를  #
# 찾아낼 때 사용 되는 함수이다.                                       #
#####################################################################


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

    #i를 indexlis에 저장한 인덱스 값들로 지정되게 for문을 돌린다.
    #result는 원본 데이터에서 해당 인덱스가 가리키는 정보를 저장한다.
    #filtered_list에는 result의 리스트 형태로 저장해 
    #column_name을 제외한 순수 데이터를 리스트 형태로 저장한다.
    for i in indexlis:
        result = df.loc[i]
        filtered_list.append(list(result))
    
    filtered_header = handle_df.columns.tolist()
    filtered_df = pd.DataFrame(filtered_list, columns=filtered_header)
    filtered_df.head()

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

    #i를 indexlis에 저장한 인덱스 값들로 지정되게 for문을 돌린다.
    #result는 원본 데이터에서 해당 인덱스가 가리키는 정보를 저장한다.
    #filtered_list에는 result의 리스트 형태로 저장해 
    #column_name을 제외한 순수 데이터를 리스트 형태로 저장한다.
    for i in indexlis:
        result = df.loc[i]
        filtered_list.append(list(result))
       
    filtered_header = handle_df.columns.tolist()
    filtered_df = pd.DataFrame(filtered_list, columns=filtered_header)
    filtered_df.head()

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

    #i를 indexlis에 저장한 인덱스 값들로 지정되게 for문을 돌린다.
    #result는 원본 데이터에서 해당 인덱스가 가리키는 정보를 저장한다.
    #filtered_list에는 result의 리스트 형태로 저장해 
    #column_name을 제외한 순수 데이터를 리스트 형태로 저장한다.
    for i in indexlis:
        result = df.loc[i]
        filtered_list.append(list(result))

    
    filtered_header = handle_df.columns.tolist()
    filtered_df = pd.DataFrame(filtered_list, columns=filtered_header)
    filtered_df.head()

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

    #i를 indexlis에 저장한 인덱스 값들로 지정되게 for문을 돌린다.
    #result는 원본 데이터에서 해당 인덱스가 가리키는 정보를 저장한다.
    #filtered_list에는 result의 리스트 형태로 저장해 
    #column_name을 제외한 순수 데이터를 리스트 형태로 저장한다.
    for i in indexlis:
        result = df.loc[i]
        filtered_list.append(list(result))
    
    filtered_header = handle_df.columns.tolist()
    filtered_df = pd.DataFrame(filtered_list, columns=filtered_header)
    filtered_df.head()


    return filtered_df



#편집을 원하는 행을 리스트화 하는 함수
#df에는 불러온 데이터프레임을 넣고 col에는 수정 원하는 행 이름을 삽입
def df2first(df,col):
    col_first = list(df.columns)
    x = col_first.index(col)
    res = df.iloc[:,x:x+1].values.tolist()
    res = sum(res,[])
    return res


################
# Edit section #
################

#add 기능 함수   
def add(df, col, add_place, add_text):
    res = []
    first = df2first(df,col)
    #column 이름 리스트화(나중에 재정렬용)
    col_nme = df.columns.tolist()
    if add_place == 'beginning':
        for x in first:
            res.append(add_text + x)
    if add_place == 'ending':
        for x in first:
            res.append(x + add_text)   
    #열 추가
    del df[col]
    df[col] = res
    
    #열 위치 재정렬
    df = df[col_nme]
    
    return(df)

##Remove 함수

##필요한 함수
#시작 혹은 끝 부분을 검색하기
def reg(loc,old_text):
    if loc == 'beginning':
        regex = '^' + old_text
    if loc == 'ending':
        regex = old_text + '$'
    return(regex)

#remove 메인 함수   
def rmv(df,col, regex, old_text):
    res = []
    k = re.compile(reg(regex, old_text))
    first = df2first(df,col)
    #column 이름 리스트화(나중에 재정렬용)
    col_nme = df.columns.tolist()
    for x in first:
        first = k.sub('',x)
        res.append(first)
        
    #열 추가
    del df[col]
    df[col] = res
    
    #열 위치 재정렬
    df = df[col_nme]
    
    return(df)

#Replace 함수

#whole string replace 함수

def whole_rpl(df, col, original_text, new_text):
    res = []
    first = df2first(df,col)
    #column 이름 리스트화(나중에 재정렬용)
    col_nme = df.columns.tolist()
    #whole_string에서 replace
    for x in first:
        if x == original_text:
            x = x.replace(original_text, new_text)
            res.append(x)
        else:
            res.append(x)
    #열 추가
    df[col] = res
    
    #열 위치 재정렬
    df = df[col_nme]
    
    return(df)


##anywhere replace 함수

def anywhere_rpl(df, col, original_text, new_text):
    res = []
    first = df2first(df,col)
    #column 이름 리스트화(나중에 재정렬용)
    col_nme = df.columns.tolist()
    #anywhere에서 replace
    for x in first:
        y = re.sub(original_text, new_text, x)
        res.append(y)
        
    #열 추가
    df[col] = res
    
    #열 위치 재정렬
    df = df[col_nme]
    
    return(df)

##begin replace 함수

def begin_rpl(df, col, original_text, new_text):
    res = []
    first = df2first(df,col)
    #column 이름 리스트화(나중에 재정렬용)
    col_nme = df.columns.tolist()
    #begin에서 replace
    for x in first:
        y = re.sub(r'^' + original_text, new_text, x)
        res.append(y)
        
    #열 추가
    df[col] = res
    
    #열 위치 재정렬
    df = df[col_nme]
    
    return(df)

##end replace 함수

def end_rpl(df, col, original_text, new_text):
    res = []
    first = df2first(df,col)
    #column 이름 리스트화(나중에 재정렬용)
    col_nme = df.columns.tolist()
    #end에서 replace
    for x in first:
        y = re.sub(original_text + '$', new_text, x)
        res.append(y)
        
    #열 추가
    df[col] = res
    
    #열 위치 재정렬
    df = df[col_nme]
    
    return(df)

##Irregular 함수

#필요한 함수

#자모음 분리하는 함수

# 초성 리스트. 00 ~ 18
initial = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
# 중성 리스트. 00 ~ 20
mid = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
# 종성 리스트. 00 ~ 27 + 1(1개 없음)
final = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

#자모음 다시 합치는 함수
def jaso_combi(a, b, c):
    global initial
    global mid
    global final


    ini_ord = initial.index(a)*(21*28)
    mid_ord = mid.index(b)*28
    final_ord = final.index(c)
    wansung = ini_ord + mid_ord + final_ord + 44032
    wansung = chr(wansung)
    
    return wansung

#irreg 메인 함수
def irreg(df, jongsung, old_eomi, new_eomi):
    
    #자모음 분리하고 리스트화
    lem = df2first(df, 'Lemma')

    #column 이름 리스트화(나중에 재정렬용)
    col_nme = df.columns.tolist()

    divided_lst = []
    for x in lem:
        d_lst = list(Divide(str(x)))
        divided_lst.append(d_lst)

    #원하는 종성 삭제하기
    for x in divided_lst:
        if len(x) >= 2:
            if x[-2][2] == str(jongsung):
                x[-2][2] = ' '
            else:
                continue
        else:
            continue
    
    #자모음 다시 합치기
    w_lst = []
    for x in divided_lst:
        p_lst = []
        for y in x:
            k = jaso_combi(y[0], y[1], y[2])
            p_lst.append(k)
            word = "".join(p_lst)
        w_lst.append(word)

    #열 추가
    df['Lemma'] = w_lst

    #열 위치 재정렬
    df = df[col_nme]

    #어미 바꾸기
    end_rpl(df, 'Lemma', old_eomi, new_eomi)

    return(df)

##Row action 함수

##행 추가

def addrow(df):
    df.loc[len(df)] = np.nan
    return df

##행 삭제

def delrow(df):
    res_df = df.drop(len(df)-1,0)
    return res_df


##행 복제

def duprow(df, sel):
    # sel = input('복제를 원하는 행 번호: ')
    res_df = df.append(df.iloc[int(sel)], ignore_index = True)
    ##특정 행을 클릭하는것을 어떻게 나타내는지??
    return(res_df)

##dic파일로 저장하는 함수
####dic작성 시작####
def df2dic(df, filepath):
    
    #딕셔너리 자료형의 특징을 이용하여 리스트 요소 순서를 유지하며 중복 제거하기

    def rmvspc(alist):
        d = OrderedDict()
        for i in alist:
            d[i] = True
            res = list(d.keys())
        return res
        
    #필요한 구분자들
    spc = "ㆍ"
    com = ","
    plus = "+"
    dot = "."

    #나중에 txt파일에 쓰기 쉽게 하기 위해 리스트 형식으로 저장
    dic_lst = [] 

    ind_l = len(df.index) #데이터의 총 개수(index 길이)

    for i in range(0, ind_l):
        dic = "ㆍ" #dic 파일의 시작이 ㆍ이므로 미리 설정해서 초기화 시켜줌
        ind_lst = list(df.iloc[i]) 
        inf_lst = rmvspc(ind_lst) #중복되는 요소인 ''을 하나로 줄이기
        inf_lst.remove('') #''는 필요 없으므로 삭제
        lem = inf_lst[0] #lemma 추출
        sep_lem = spc.join(lem) #lemma의 각 음절마다 ㆍ삽입
        dic = dic + sep_lem + com + lem + dot #문자열 형식으로 합치기('ㆍ가ㆍ결,가결.' 이 부분까지 완성)
        #category의 ns01과 같은 정보를 ns만 따로 떼어내기
        cat = inf_lst[1] 
        dic = dic + cat[0:2]
        #그 외의 info들을 모두 'ZNZ+LEO+SLB' 이런 형식으로 더해주기
        for x in range(2, len(inf_lst)):
            inf = inf_lst[x]
            dic = dic + plus + inf
        #ns 뒤에 붙은 숫자 정보를 'JN#JN숫자'형식으로 바꾸어주기
        last = plus + "JN#JN" + cat[-2:]
        dic1 = dic + last
        dic_lst.append(str(dic1))

    # writedata.py
    f = open(filepath, 'w', encoding='utf-8-sig')



    for i in range(len(dic_lst)):
        f.write('%s \n' % dic_lst[i])


    f.close()


#############
# GUI PART  #
#############

class Ui_Deco_LexO(object):
    def setupUi(self, Deco_LexO):
        global Tab_index
        global count
        global alpha
        self.a = QtWidgets.QTableWidget
        self.b = QtWidgets.QTableWidget
        self.c = QtWidgets.QTableWidget
        self.d = QtWidgets.QTableWidget
        self.e = QtWidgets.QTableWidget
        self.f = QtWidgets.QTableWidget
        self.g = QtWidgets.QTableWidget
        self.h = QtWidgets.QTableWidget
        self.i = QtWidgets.QTableWidget
        self.j = QtWidgets.QTableWidget
        self.k = QtWidgets.QTableWidget
        self.l = QtWidgets.QTableWidget
        self.m = QtWidgets.QTableWidget
        self.n = QtWidgets.QTableWidget
        self.o = QtWidgets.QTableWidget
        self.p = QtWidgets.QTableWidget
        self.q = QtWidgets.QTableWidget
        self.r = QtWidgets.QTableWidget
        self.s = QtWidgets.QTableWidget
        self.t = QtWidgets.QTableWidget

        alpha = [self.a, self.b, self.c, self.d, self.e, self.f ,self.g, self.h, self.i, self.j, 
                self.k, self.l, self.m, self.n, self.o, self.p, self.q, self.r, self.s, self.t]
        Tab_index = 0
        count = 0
        Deco_LexO.setObjectName("Deco_LexO")
        Deco_LexO.resize(709, 732)
        self.centralwidget = QtWidgets.QWidget(Deco_LexO)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.dataFrame_Tab = QtWidgets.QTabWidget(self.centralwidget)
        self.dataFrame_Tab.setObjectName("dataFrame_Tab")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.dataFrame_Tab.addTab(self.tab, "")
        self.gridLayout.addWidget(self.dataFrame_Tab, 0, 1, 1, 1)
        self.tabWidget_1 = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_1.setMaximumSize(QtCore.QSize(328, 16777215))
        self.tabWidget_1.setObjectName("tabWidget_1")
        self.Modifying_Tab = QtWidgets.QWidget()
        self.Modifying_Tab.setObjectName("Modifying_Tab")

        #Filter Entry part
        self.FEntryCombo = QtWidgets.QComboBox(self.Modifying_Tab)
        self.FEntryCombo.setGeometry(QtCore.QRect(30, 40, 91, 21))
        self.FEntryCombo.setObjectName("FEntryCombo")
        self.FEntryCombo.addItem("")
        self.FEntryCombo.setItemText(0, "")
        self.FEntryCombo.addItem("")
        self.FEntryCombo.addItem("")
        self.FEntryCombo.addItem("")
        self.FEntryCombo.addItem("")
        self.FEntryCombo.addItem("")
        self.FEntry_Input = QtWidgets.QLineEdit(self.Modifying_Tab)
        self.FEntry_Input.setGeometry(QtCore.QRect(130, 40, 161, 21))
        self.FEntry_Input.setObjectName("FEntry_Input")

        #Filter Lemma part
        self.FLemma_Input = QtWidgets.QLineEdit(self.Modifying_Tab)
        self.FLemma_Input.setGeometry(QtCore.QRect(130, 100, 161, 21))
        self.FLemma_Input.setObjectName("FLemma_Input")
        self.FLemmaCombo = QtWidgets.QComboBox(self.Modifying_Tab)
        self.FLemmaCombo.setGeometry(QtCore.QRect(30, 100, 91, 21))
        self.FLemmaCombo.setObjectName("FLemmaCombo")
        self.FLemmaCombo.addItem("")
        self.FLemmaCombo.setItemText(0, "")
        self.FLemmaCombo.addItem("")
        self.FLemmaCombo.addItem("")
        self.FLemmaCombo.addItem("")
        self.FLemmaCombo.addItem("")
        self.FLemmaCombo.addItem("")

        #Filter Category part
        self.FCateCombo = QtWidgets.QComboBox(self.Modifying_Tab)
        self.FCateCombo.setGeometry(QtCore.QRect(30, 160, 91, 21))
        self.FCateCombo.setObjectName("FCateCombo")
        self.FCateCombo.addItem("")
        self.FCateCombo.setItemText(0, "")
        self.FCateCombo.addItem("")
        self.FCateCombo.addItem("")
        self.FCateCombo.addItem("")
        self.FCateCombo.addItem("")
        self.FCateCombo.addItem("")
        self.FCate_Input = QtWidgets.QLineEdit(self.Modifying_Tab)
        self.FCate_Input.setGeometry(QtCore.QRect(130, 160, 161, 21))
        self.FCate_Input.setObjectName("FCate_Input")

        #Filter Infornation part
        self.FInfoCombo = QtWidgets.QComboBox(self.Modifying_Tab)
        self.FInfoCombo.setGeometry(QtCore.QRect(30, 220, 91, 21))
        self.FInfoCombo.setObjectName("FInfoCombo")
        self.FInfoCombo.addItem("")
        self.FInfoCombo.setItemText(0, "")
        self.FInfoCombo.addItem("")
        self.FInfoCombo.addItem("")
        self.FInfoCombo.addItem("")
        self.FInfoCombo.addItem("")
        self.FInfoCombo.addItem("")
        self.FInfo_Input = QtWidgets.QLineEdit(self.Modifying_Tab)
        self.FInfo_Input.setGeometry(QtCore.QRect(210, 220, 81, 21))
        self.FInfo_Input.setObjectName("FInfo_Input")
        self.FInfo_Colname = QtWidgets.QLineEdit(self.Modifying_Tab)
        self.FInfo_Colname.setGeometry(QtCore.QRect(130, 220, 71, 21))
        self.FInfo_Colname.setObjectName("FInfo_Colname")

        #Filter Phonological First_Syllable part
        self.FFirst_1 = QtWidgets.QLineEdit(self.Modifying_Tab)
        self.FFirst_1.setGeometry(QtCore.QRect(30, 320, 51, 21))
        self.FFirst_1.setObjectName("FFirst_1")
        self.FFirst_2 = QtWidgets.QLineEdit(self.Modifying_Tab)
        self.FFirst_2.setGeometry(QtCore.QRect(100, 320, 51, 21))
        self.FFirst_2.setObjectName("FFirst_2")
        self.FFirst_3 = QtWidgets.QLineEdit(self.Modifying_Tab)
        self.FFirst_3.setGeometry(QtCore.QRect(170, 320, 51, 21))
        self.FFirst_3.setObjectName("FFirst_3")

        #Filter Phonological Second_Syllable part
        self.FSec_3 = QtWidgets.QLineEdit(self.Modifying_Tab)
        self.FSec_3.setGeometry(QtCore.QRect(170, 370, 51, 21))
        self.FSec_3.setObjectName("FSec_3")
        self.FSec_2 = QtWidgets.QLineEdit(self.Modifying_Tab)
        self.FSec_2.setGeometry(QtCore.QRect(100, 370, 51, 21))
        self.FSec_2.setObjectName("FSec_2")
        self.FSec_1 = QtWidgets.QLineEdit(self.Modifying_Tab)
        self.FSec_1.setGeometry(QtCore.QRect(30, 370, 51, 21))
        self.FSec_1.setObjectName("FSec_1")

        #Filter Phonological Second_to_Last part
        self.FSecL_3 = QtWidgets.QLineEdit(self.Modifying_Tab)
        self.FSecL_3.setGeometry(QtCore.QRect(170, 420, 51, 21))
        self.FSecL_3.setObjectName("FSecL_3")
        self.FSecL_2 = QtWidgets.QLineEdit(self.Modifying_Tab)
        self.FSecL_2.setGeometry(QtCore.QRect(100, 420, 51, 21))
        self.FSecL_2.setObjectName("FSecL_2")
        self.FSecL_1 = QtWidgets.QLineEdit(self.Modifying_Tab)
        self.FSecL_1.setGeometry(QtCore.QRect(30, 420, 51, 21))
        self.FSecL_1.setObjectName("FSecL_1")

        #Filter Phonological Last_Syllable part
        self.FLast_3 = QtWidgets.QLineEdit(self.Modifying_Tab)
        self.FLast_3.setGeometry(QtCore.QRect(170, 470, 51, 21))
        self.FLast_3.setObjectName("FLast_3")
        self.FLast_2 = QtWidgets.QLineEdit(self.Modifying_Tab)
        self.FLast_2.setGeometry(QtCore.QRect(100, 470, 51, 21))
        self.FLast_2.setObjectName("FLast_2")
        self.FLast_1 = QtWidgets.QLineEdit(self.Modifying_Tab)
        self.FLast_1.setGeometry(QtCore.QRect(30, 470, 51, 21))
        self.FLast_1.setObjectName("FLast_1")

        self.FPhonoFrame = QtWidgets.QFrame(self.Modifying_Tab)
        self.FPhonoFrame.setGeometry(QtCore.QRect(10, 290, 281, 251))
        self.FPhonoFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.FPhonoFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.FPhonoFrame.setObjectName("FPhonoFrame")

        #Filter Phonological ColumnBox part
        self.FColCombo = QtWidgets.QComboBox(self.FPhonoFrame)
        self.FColCombo.setGeometry(QtCore.QRect(90, 220, 81, 21))
        self.FColCombo.setObjectName("FColCombo")
        self.FColCombo.addItem("")
        self.FColCombo.addItem("")
        self.FColCombo.addItem("")

        self.label_7 = QtWidgets.QLabel(self.FPhonoFrame)
        self.label_7.setGeometry(QtCore.QRect(20, 50, 211, 31))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.FPhonoFrame)
        self.label_8.setGeometry(QtCore.QRect(20, 100, 211, 31))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.FPhonoFrame)
        self.label_9.setGeometry(QtCore.QRect(20, 0, 191, 31))
        self.label_9.setObjectName("label_9")
        self.label_6 = QtWidgets.QLabel(self.FPhonoFrame)
        self.label_6.setGeometry(QtCore.QRect(20, 150, 211, 31))
        self.label_6.setObjectName("label_6")
        self.label_10 = QtWidgets.QLabel(self.FPhonoFrame)
        self.label_10.setGeometry(QtCore.QRect(10, 220, 61, 21))
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")

        #Filter button
        self.FFiltering_Button = QtWidgets.QPushButton(self.Modifying_Tab)
        self.FFiltering_Button.setGeometry(QtCore.QRect(20, 550, 75, 23))
        self.FFiltering_Button.setObjectName("FFiltering_Button")

        #Show all button
        self.FShow_Button = QtWidgets.QPushButton(self.Modifying_Tab)
        self.FShow_Button.setGeometry(QtCore.QRect(110, 550, 75, 23))
        self.FShow_Button.setObjectName("FShow_Button")

        #clear button
        self.FClear_Button = QtWidgets.QPushButton(self.Modifying_Tab)
        self.FClear_Button.setGeometry(QtCore.QRect(210, 550, 75, 23))
        self.FClear_Button.setObjectName("FClear_Button")

        self.label = QtWidgets.QLabel(self.Modifying_Tab)
        self.label.setGeometry(QtCore.QRect(30, 10, 56, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.Modifying_Tab)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 56, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.Modifying_Tab)
        self.label_3.setGeometry(QtCore.QRect(30, 130, 56, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.Modifying_Tab)
        self.label_4.setGeometry(QtCore.QRect(30, 190, 81, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.Modifying_Tab)
        self.label_5.setGeometry(QtCore.QRect(10, 270, 141, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")

        #Filter Phonological button part
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
        self.FInfo_Colname.raise_()

        #Edit GUI
        self.tabWidget_1.addTab(self.Modifying_Tab, "")
        self.Edit_tab = QtWidgets.QWidget()
        self.Edit_tab.setObjectName("Edit_tab")
        self.Edit_function_tab = QtWidgets.QTabWidget(self.Edit_tab)
        self.Edit_function_tab.setGeometry(QtCore.QRect(0, 50, 321, 371))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Edit_function_tab.setFont(font)
        self.Edit_function_tab.setObjectName("Edit_function_tab")
        self.Add_tab = QtWidgets.QWidget()
        self.Add_tab.setObjectName("Add_tab")
        self.Add_column = QtWidgets.QComboBox(self.Add_tab)
        self.Add_column.setGeometry(QtCore.QRect(150, 80, 128, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Add_column.setFont(font)
        self.Add_column.setEditable(True)
        self.Add_column.setObjectName("Add_column")
        self.Add_column.addItem("")
        self.Add_column.setItemText(0, "")
        self.Add_column.addItem("")
        self.Add_column.addItem("")
        self.Add_position = QtWidgets.QComboBox(self.Add_tab)
        self.Add_position.setGeometry(QtCore.QRect(150, 150, 128, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Add_position.setFont(font)
        self.Add_position.setObjectName("Add_position")
        self.Add_position.addItem("")
        self.Add_position.addItem("")
        self.Add_oldText = QtWidgets.QLineEdit(self.Add_tab)
        self.Add_oldText.setGeometry(QtCore.QRect(150, 220, 128, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Add_oldText.setFont(font)
        self.Add_oldText.setAutoFillBackground(False)
        self.Add_oldText.setObjectName("Add_oldText")
        self.Add_start = QtWidgets.QPushButton(self.Add_tab)
        self.Add_start.setGeometry(QtCore.QRect(180, 290, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Add_start.setFont(font)
        self.Add_start.setObjectName("Add_start")
        self.label_12 = QtWidgets.QLabel(self.Add_tab)
        self.label_12.setGeometry(QtCore.QRect(10, 150, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.label_14 = QtWidgets.QLabel(self.Add_tab)
        self.label_14.setGeometry(QtCore.QRect(0, 10, 321, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.label_13 = QtWidgets.QLabel(self.Add_tab)
        self.label_13.setGeometry(QtCore.QRect(10, 220, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.label_11 = QtWidgets.QLabel(self.Add_tab)
        self.label_11.setGeometry(QtCore.QRect(10, 80, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.Edit_function_tab.addTab(self.Add_tab, "")
        self.Remove_tab = QtWidgets.QWidget()
        self.Remove_tab.setObjectName("Remove_tab")
        self.label_15 = QtWidgets.QLabel(self.Remove_tab)
        self.label_15.setGeometry(QtCore.QRect(10, 150, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.Remove_tab)
        self.label_16.setGeometry(QtCore.QRect(0, 10, 321, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.Remove_tab)
        self.label_17.setGeometry(QtCore.QRect(10, 220, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_17.setFont(font)
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.Remove_tab)
        self.label_18.setGeometry(QtCore.QRect(10, 80, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_18.setFont(font)
        self.label_18.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_18.setObjectName("label_18")
        self.Remove_column = QtWidgets.QComboBox(self.Remove_tab)
        self.Remove_column.setGeometry(QtCore.QRect(150, 80, 128, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Remove_column.setFont(font)
        self.Remove_column.setEditable(True)
        self.Remove_column.setObjectName("Remove_column")
        self.Remove_column.addItem("")
        self.Remove_column.setItemText(0, "")
        self.Remove_column.addItem("")
        self.Remove_column.addItem("")
        self.Remove_position = QtWidgets.QComboBox(self.Remove_tab)
        self.Remove_position.setGeometry(QtCore.QRect(150, 150, 128, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Remove_position.setFont(font)
        self.Remove_position.setObjectName("Remove_position")
        self.Remove_position.addItem("")
        self.Remove_position.addItem("")
        self.Remove_oldText = QtWidgets.QLineEdit(self.Remove_tab)
        self.Remove_oldText.setGeometry(QtCore.QRect(150, 220, 130, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Remove_oldText.setFont(font)
        self.Remove_oldText.setAutoFillBackground(False)
        self.Remove_oldText.setObjectName("Remove_oldText")
        self.Remove_start = QtWidgets.QPushButton(self.Remove_tab)
        self.Remove_start.setGeometry(QtCore.QRect(180, 290, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Remove_start.setFont(font)
        self.Remove_start.setObjectName("Remove_start")
        self.Edit_function_tab.addTab(self.Remove_tab, "")
        self.Replace_tab = QtWidgets.QWidget()
        self.Replace_tab.setObjectName("Replace_tab")
        self.Replace_column = QtWidgets.QComboBox(self.Replace_tab)
        self.Replace_column.setGeometry(QtCore.QRect(150, 70, 130, 30))
        self.Replace_column.setEditable(True)
        self.Replace_column.setObjectName("Replace_column")
        self.Replace_column.addItem("")
        self.Replace_column.setItemText(0, "")
        self.Replace_column.addItem("")
        self.Replace_column.addItem("")
        self.Replace_position = QtWidgets.QComboBox(self.Replace_tab)
        self.Replace_position.setGeometry(QtCore.QRect(150, 127, 130, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Replace_position.setFont(font)
        self.Replace_position.setObjectName("Replace_position")
        self.Replace_position.addItem("")
        self.Replace_position.addItem("")
        self.Replace_position.addItem("")
        self.Replace_position.addItem("")
        self.Replace_oldtext = QtWidgets.QLineEdit(self.Replace_tab)
        self.Replace_oldtext.setGeometry(QtCore.QRect(150, 183, 133, 30))
        self.Replace_oldtext.setObjectName("Replace_oldtext")
        self.Replace_newtext = QtWidgets.QLineEdit(self.Replace_tab)
        self.Replace_newtext.setGeometry(QtCore.QRect(150, 240, 133, 30))
        self.Replace_newtext.setObjectName("Replace_newtext")
        self.Replace_start = QtWidgets.QPushButton(self.Replace_tab)
        self.Replace_start.setGeometry(QtCore.QRect(210, 300, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Replace_start.setFont(font)
        self.Replace_start.setObjectName("Replace_start")
        self.label_19 = QtWidgets.QLabel(self.Replace_tab)
        self.label_19.setGeometry(QtCore.QRect(0, 10, 321, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_19.setFont(font)
        self.label_19.setAlignment(QtCore.Qt.AlignCenter)
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.Replace_tab)
        self.label_20.setGeometry(QtCore.QRect(20, 70, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_20.setFont(font)
        self.label_20.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.Replace_tab)
        self.label_21.setGeometry(QtCore.QRect(20, 127, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_21.setFont(font)
        self.label_21.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_21.setObjectName("label_21")
        self.label_22 = QtWidgets.QLabel(self.Replace_tab)
        self.label_22.setGeometry(QtCore.QRect(20, 183, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_22.setFont(font)
        self.label_22.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.Replace_tab)
        self.label_23.setGeometry(QtCore.QRect(20, 240, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_23.setFont(font)
        self.label_23.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_23.setObjectName("label_23")
        self.Edit_function_tab.addTab(self.Replace_tab, "")
        self.Irreg_tab = QtWidgets.QWidget()
        self.Irreg_tab.setObjectName("Irreg_tab")
        self.Irreg_cons = QtWidgets.QLineEdit(self.Irreg_tab)
        self.Irreg_cons.setGeometry(QtCore.QRect(150, 80, 128, 30))
        self.Irreg_cons.setObjectName("Irreg_cons")
        self.Irreg_oldinflec = QtWidgets.QLineEdit(self.Irreg_tab)
        self.Irreg_oldinflec.setGeometry(QtCore.QRect(150, 150, 128, 30))
        self.Irreg_oldinflec.setObjectName("Irreg_oldinflec")
        self.irreg_newinflec = QtWidgets.QLineEdit(self.Irreg_tab)
        self.irreg_newinflec.setGeometry(QtCore.QRect(150, 220, 128, 30))
        self.irreg_newinflec.setObjectName("irreg_newinflec")
        self.Irreg_start = QtWidgets.QPushButton(self.Irreg_tab)
        self.Irreg_start.setGeometry(QtCore.QRect(180, 290, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Irreg_start.setFont(font)
        self.Irreg_start.setObjectName("Irreg_start")
        self.label_24 = QtWidgets.QLabel(self.Irreg_tab)
        self.label_24.setGeometry(QtCore.QRect(0, 10, 321, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_24.setFont(font)
        self.label_24.setAlignment(QtCore.Qt.AlignCenter)
        self.label_24.setObjectName("label_24")
        self.label_25 = QtWidgets.QLabel(self.Irreg_tab)
        self.label_25.setGeometry(QtCore.QRect(10, 80, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_25.setFont(font)
        self.label_25.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_25.setObjectName("label_25")
        self.label_26 = QtWidgets.QLabel(self.Irreg_tab)
        self.label_26.setGeometry(QtCore.QRect(10, 150, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_26.setFont(font)
        self.label_26.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_26.setObjectName("label_26")
        self.label_27 = QtWidgets.QLabel(self.Irreg_tab)
        self.label_27.setGeometry(QtCore.QRect(10, 220, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_27.setFont(font)
        self.label_27.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_27.setObjectName("label_27")
        self.Edit_function_tab.addTab(self.Irreg_tab, "")
        self.Push_Duplicaterow = QtWidgets.QPushButton(self.Edit_tab)
        self.Push_Duplicaterow.setGeometry(QtCore.QRect(9, 500, 301, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Push_Duplicaterow.setFont(font)
        self.Push_Duplicaterow.setObjectName("Push_Duplicaterow")
        self.Push_addrow = QtWidgets.QPushButton(self.Edit_tab)
        self.Push_addrow.setGeometry(QtCore.QRect(9, 450, 141, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Push_addrow.setFont(font)
        self.Push_addrow.setObjectName("Push_addrow")
        self.Push_Deleterow = QtWidgets.QPushButton(self.Edit_tab)
        self.Push_Deleterow.setGeometry(QtCore.QRect(170, 450, 140, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Push_Deleterow.setFont(font)
        self.Push_Deleterow.setObjectName("Push_Deleterow")
        self.tabWidget_1.addTab(self.Edit_tab, "")
        self.gridLayout.addWidget(self.tabWidget_1, 0, 0, 1, 1)
        Deco_LexO.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Deco_LexO)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 709, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuRecent_files = QtWidgets.QMenu(self.menuFile)
        self.menuRecent_files.setObjectName("menuRecent_files")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        Deco_LexO.setMenuBar(self.menubar)
        self.actionOpen_file_s = QtWidgets.QAction(Deco_LexO)
        self.actionOpen_file_s.setShortcutContext(QtCore.Qt.WindowShortcut)
        self.actionOpen_file_s.setObjectName("actionOpen_file_s")
        self.actionNone = QtWidgets.QAction(Deco_LexO)
        self.actionNone.setObjectName("actionNone")
        self.actionSave = QtWidgets.QAction(Deco_LexO)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_file_as = QtWidgets.QAction(Deco_LexO)
        self.actionSave_file_as.setObjectName("actionSave_file_as")
        self.actionQuit = QtWidgets.QAction(Deco_LexO)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAcknowledgement = QtWidgets.QAction(Deco_LexO)
        self.actionAcknowledgement.setObjectName("actionAcknowledgement")
        self.actionAbout_DecoLexO = QtWidgets.QAction(Deco_LexO)
        self.actionAbout_DecoLexO.setObjectName("actionAbout_DecoLexO")
        self.menuRecent_files.addAction(self.actionNone)
        self.menuFile.addAction(self.actionOpen_file_s)
        self.menuFile.addAction(self.menuRecent_files.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_file_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAcknowledgement)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout_DecoLexO)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(Deco_LexO)
        self.dataFrame_Tab.setCurrentIndex(0)
        self.tabWidget_1.setCurrentIndex(0)
        self.Edit_function_tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Deco_LexO)

        ##connenct code##
        self.actionOpen_file_s.triggered.connect(self.openFiles)
        self.actionSave_file_as.triggered.connect(self.save_as)
        #Edit part connect
        self.Add_start.released.connect(self.add_function)
        self.Remove_start.released.connect(self.remove_function)
        self.Replace_start.released.connect(self.replace_function)
        self.Irreg_start.released.connect(self.irregular_function)
        self.Push_addrow.released.connect(self.add_row_function)
        self.Push_Deleterow.released.connect(self.delete_row_function)
        self.Push_Duplicaterow.released.connect(self.duplicate_row_function)

        #Filter part connect
        self.FShow_Button.released.connect (self.show_all)
        self.FFiltering_Button.released.connect (self.filter_function)
        self.FClear_Button.released.connect(self.clear)

    

    def retranslateUi(self, Deco_LexO):
        _translate = QtCore.QCoreApplication.translate
        Deco_LexO.setWindowTitle(_translate("Deco_LexO", "Deco-LexO"))
        self.dataFrame_Tab.setTabText(self.dataFrame_Tab.indexOf(self.tab), _translate("Deco_LexO", "Start"))

        #Filter part GUI
        self.FEntryCombo.setItemText(1, _translate("Deco_LexO", "Equals"))
        self.FEntryCombo.setItemText(2, _translate("Deco_LexO", "Starts with"))
        self.FEntryCombo.setItemText(3, _translate("Deco_LexO", "Ends with"))
        self.FEntryCombo.setItemText(4, _translate("Deco_LexO", "Contains"))
        self.FEntryCombo.setItemText(5, _translate("Deco_LexO", "is empty"))
        self.FLemmaCombo.setItemText(1, _translate("Deco_LexO", "Equals"))
        self.FLemmaCombo.setItemText(2, _translate("Deco_LexO", "Starts with"))
        self.FLemmaCombo.setItemText(3, _translate("Deco_LexO", "Ends with"))
        self.FLemmaCombo.setItemText(4, _translate("Deco_LexO", "Contains"))
        self.FLemmaCombo.setItemText(5, _translate("Deco_LexO", "is empty"))
        self.FCateCombo.setItemText(1, _translate("Deco_LexO", "Equals"))
        self.FCateCombo.setItemText(2, _translate("Deco_LexO", "Starts with"))
        self.FCateCombo.setItemText(3, _translate("Deco_LexO", "Ends with"))
        self.FCateCombo.setItemText(4, _translate("Deco_LexO", "Contains"))
        self.FCateCombo.setItemText(5, _translate("Deco_LexO", "is empty"))
        self.label_7.setText(_translate("Deco_LexO", "Second syllable:"))
        self.label_8.setText(_translate("Deco_LexO", "Second-to-last syllable:"))
        self.label_9.setText(_translate("Deco_LexO", "First syllable:"))
        self.label_6.setText(_translate("Deco_LexO", "Last syllable:"))
        self.label_10.setText(_translate("Deco_LexO", "Column:"))
        self.FFiltering_Button.setText(_translate("Deco_LexO", "Filter"))
        self.FShow_Button.setText(_translate("Deco_LexO", "Show all"))
        self.FClear_Button.setText(_translate("Deco_LexO", "Clear"))
        self.label.setText(_translate("Deco_LexO", "Entry:"))
        self.label_2.setText(_translate("Deco_LexO", "Lemma:"))
        self.label_3.setText(_translate("Deco_LexO", "Category:"))
        self.label_4.setText(_translate("Deco_LexO", "Information:"))
        self.FInfoCombo.setItemText(1, _translate("Deco_LexO", "Equals"))
        self.FInfoCombo.setItemText(2, _translate("Deco_LexO", "Starts with"))
        self.FInfoCombo.setItemText(3, _translate("Deco_LexO", "Ends with"))
        self.FInfoCombo.setItemText(4, _translate("Deco_LexO", "Contains"))
        self.FInfoCombo.setItemText(5, _translate("Deco_LexO", "is empty"))
        self.FColCombo.setItemText(1, _translate("Deco_LexO", "Lemma"))
        self.FColCombo.setItemText(2, _translate("Deco_LexO", "Entry"))
        self.label_5.setText(_translate("Deco_LexO", "Phonological shape"))
        self.tabWidget_1.setTabText(self.tabWidget_1.indexOf(self.Modifying_Tab), _translate("Deco_LexO", "Filter"))

        #Edit part GUI
        self.Add_column.setItemText(1, _translate("Deco_LexO", "Lemma"))
        self.Add_column.setItemText(2, _translate("Deco_LexO", "Category"))
        self.Add_position.setItemText(0, _translate("Deco_LexO", "beginning"))
        self.Add_position.setItemText(1, _translate("Deco_LexO", "ending"))
        self.Add_start.setText(_translate("Deco_LexO", "OK"))
        self.label_12.setText(_translate("Deco_LexO", "Position:"))
        self.label_14.setText(_translate("Deco_LexO", "Add Option"))
        self.label_13.setText(_translate("Deco_LexO", "New Text:"))
        self.label_11.setText(_translate("Deco_LexO", "Column Name:"))
        self.Edit_function_tab.setTabText(self.Edit_function_tab.indexOf(self.Add_tab), _translate("Deco_LexO", "Add"))
        self.label_15.setText(_translate("Deco_LexO", "Position:"))
        self.label_16.setText(_translate("Deco_LexO", "Remove Option"))
        self.label_17.setText(_translate("Deco_LexO", "Old Text:"))
        self.label_18.setText(_translate("Deco_LexO", "Column Name:"))
        self.Remove_column.setItemText(1, _translate("Deco_LexO", "Lemma"))
        self.Remove_column.setItemText(2, _translate("Deco_LexO", "Category"))
        self.Remove_position.setItemText(0, _translate("Deco_LexO", "beginning"))
        self.Remove_position.setItemText(1, _translate("Deco_LexO", "ending"))
        self.Remove_start.setText(_translate("Deco_LexO", "OK"))
        self.Edit_function_tab.setTabText(self.Edit_function_tab.indexOf(self.Remove_tab), _translate("Deco_LexO", "Remove"))
        self.Replace_column.setItemText(1, _translate("Deco_LexO", "Lemma"))
        self.Replace_column.setItemText(2, _translate("Deco_LexO", "Column"))
        self.Replace_position.setItemText(0, _translate("Deco_LexO", "anywhere"))
        self.Replace_position.setItemText(1, _translate("Deco_LexO", "whole string"))
        self.Replace_position.setItemText(2, _translate("Deco_LexO", "beginning"))
        self.Replace_position.setItemText(3, _translate("Deco_LexO", "ending"))
        self.Replace_start.setText(_translate("Deco_LexO", "OK"))
        self.label_19.setText(_translate("Deco_LexO", "Replace Option"))
        self.label_20.setText(_translate("Deco_LexO", "Column Name:"))
        self.label_21.setText(_translate("Deco_LexO", "Position:"))
        self.label_22.setText(_translate("Deco_LexO", "Old Text:"))
        self.label_23.setText(_translate("Deco_LexO", "New Text:"))
        self.Edit_function_tab.setTabText(self.Edit_function_tab.indexOf(self.Replace_tab), _translate("Deco_LexO", "Replace"))
        self.Irreg_start.setText(_translate("Deco_LexO", "OK"))
        self.label_24.setText(_translate("Deco_LexO", "Irregular Option"))
        self.label_25.setText(_translate("Deco_LexO", "Final Consonant:"))
        self.label_26.setText(_translate("Deco_LexO", "Old Inflection:"))
        self.label_27.setText(_translate("Deco_LexO", "New Inflection:"))
        self.Edit_function_tab.setTabText(self.Edit_function_tab.indexOf(self.Irreg_tab), _translate("Deco_LexO", "Irregular"))
        self.Push_Duplicaterow.setText(_translate("Deco_LexO", "Duplicate Row"))
        self.Push_addrow.setText(_translate("Deco_LexO", "Add Row"))
        self.Push_Deleterow.setText(_translate("Deco_LexO", "Delete Row"))
        self.tabWidget_1.setTabText(self.tabWidget_1.indexOf(self.Edit_tab), _translate("Deco_LexO", "Edit"))
        self.menuFile.setTitle(_translate("Deco_LexO", "File"))
        self.menuRecent_files.setTitle(_translate("Deco_LexO", "Recent files"))
        self.menuHelp.setTitle(_translate("Deco_LexO", "Help"))
        self.actionOpen_file_s.setText(_translate("Deco_LexO", "Open files..."))
        self.actionOpen_file_s.setShortcut(_translate("Deco_LexO", "Ctrl+O"))
        self.actionNone.setText(_translate("Deco_LexO", "None"))
        self.actionSave.setText(_translate("Deco_LexO", "Save file"))
        self.actionSave.setShortcut(_translate("Deco_LexO", "Ctrl+S"))
        self.actionSave_file_as.setText(_translate("Deco_LexO", "Save file as..."))
        self.actionSave_file_as.setShortcut(_translate("Deco_LexO", "Ctrl+Shift+S"))
        self.actionQuit.setText(_translate("Deco_LexO", "Quit"))
        self.actionQuit.setShortcut(_translate("Deco_LexO", "Ctrl+Q"))
        self.actionAcknowledgement.setText(_translate("Deco_LexO", "Acknowledgement"))
        self.actionAbout_DecoLexO.setText(_translate("Deco_LexO", "About DecoLexO"))




    # 첫번째 파일을 오픈해 줄 때만 파일을 열어주는 함수
    def readFiles(self, vis_df):
        global count
        control_Tw = alpha[count]
        for i in range (len (vis_df.index)):
            for j in range (len (vis_df.columns)):
                control_Tw.setItem (i, j, QtWidgets.QTableWidgetItem (str (vis_df.iat[i, j])))

        control_Tw.resizeColumnsToContents ()
        control_Tw.resizeRowsToContents ()
        count += 1
    # open file이 아닌 데이터 처리로 visualize를 할 때 사용되는 함수
    def readFiles2(self, vis_df):
        control_Tw = alpha[self.dataFrame_Tab.currentIndex()-1]
        control_Tw.setColumnCount (0)
        control_Tw.setRowCount (0)
        control_Tw.setColumnCount (len (vis_df.columns))
        header = vis_df.columns
        control_Tw.setHorizontalHeaderLabels (header)
        control_Tw.setRowCount (len (vis_df.index))
        for i in range (len (vis_df.index)):
            for j in range (len (vis_df.columns)):
                control_Tw.setItem (i, j, QtWidgets.QTableWidgetItem (str (vis_df.iat[i, j])))

        control_Tw.resizeColumnsToContents ()
        control_Tw.resizeRowsToContents ()

    #open files를 했을 때 실행 되는 함수
    def openFiles(self):
        global handle_df, original_df, Tab_index
        global count
        global tab_name_dic
        global handle_df_list, new_table_list
        try:
            fname = QtWidgets.QFileDialog.getOpenFileName (None, 'Open CSV file', '' , "CSV Files(*.csv)")
            self.new_tab = QtWidgets.QWidget ()
            self.new_tab.setObjectName ("new_tab")
            self.gridLayout_2 = QtWidgets.QGridLayout (self.new_tab)
            self.gridLayout_2.setObjectName ("gridLayout_2")
            alpha[count] = QtWidgets.QTableWidget (self.new_tab)
            alpha[count].setColumnCount (0)
            alpha[count].setRowCount (0)
            self.gridLayout_2.addWidget (alpha[count], 0, 1, 1, 1)
            self.dataFrame_Tab.addTab (self.new_tab, str (fname).split ("', '")[0][2:].split('/')[-1])
            tab_name_list.append(str (fname).split ("', '")[0][2:].split('/')[-1])
            Ofileloc = str (fname).split ("', '")[0][2:]
            original_read = pd.read_csv (Ofileloc, encoding='utf-8-sig')
            original_df = column_name (original_read)
            original_df_list.append(original_df)
            handle_df = original_df.copy ()
            handle_df_list.append(handle_df)
            alpha[count].setColumnCount (len (handle_df.columns))
            header = original_df.columns
            alpha[count].setHorizontalHeaderLabels (header)
            alpha[count].setRowCount (len (handle_df.index))
            self.readFiles (handle_df)
            Tab_index += 1
            self.dataFrame_Tab.setCurrentIndex(Tab_index)
        except Exception:
            pass
  

    def clear(self):
        self.FEntry_Input.setText('')
        self.FEntryCombo.setCurrentIndex(0)
        self.FLemma_Input.setText('')
        self.FLemmaCombo.setCurrentIndex(0)
        self.FCate_Input.setText('')
        self.FCateCombo.setCurrentIndex(0)
        self.FInfo_Input.setText('')
        self.FInfoCombo.setCurrentIndex(0)
        self.FInfo_Colname.setText('')

        self.FFirst_1.setText(''), self.FFirst_2.setText(''), self.FFirst_3.setText('')
        self.FSec_1.setText(''), self.FSec_2.setText(''), self.FSec_3.setText('')
        self.FSecL_1.setText(''), self.FSecL_2.setText(''), self.FSecL_3.setText('')
        self.FLast_1.setText(''), self.FLast_2.setText(''), self.FLast_3.setText('')

        print(self.dataFrame_Tab.currentIndex())


    ##Save As를 눌렀을때 실행될 저장 함수들(df2dic, to_csv)
    def save_as(self):
        global handle_df
        global original_df

        result_df =  handle_df_list[self.dataFrame_Tab.currentIndex()-1]
        sname = QtWidgets.QFileDialog.getSaveFileName(None, 'Save Location', '' , 'CSV File (*.csv);; DIC File (*.dic)')
        
        sfileloc = str (sname).split ("', '")[0][2:]

        sfileform = sfileloc.split('.')[-1]

        if sfileform == 'csv':
            col_nme = original_df.columns.tolist()
            result_df = result_df[col_nme]
            print(result_df)
            return (result_df.to_csv(sfileloc, header=True, index=False, na_rep='', encoding='utf-8-sig'))
        if sfileform == 'dic':
            col_nme = original_df.columns.tolist()
            result_df = result_df[col_nme]
            return (df2dic(result_df, sfileloc))

        


    #filter part에서 filter 버튼을 누르면 실행되는 함수
    #각각 상황에 맞게 위에 선언된 함수들을 연결해 주고
    #상황에 맞게 나오느 결과들은 전역변수로 선언되 handle_df에 저장해준 후
    #마지막에 handel_df_list에 해당 탭의 인덱스 번호 -1한 부분에 
    #마지막으로 처리된 handle_df를 저장해준다.
    def filter_function(self):
        global handle_df
        global filtered_df

        
        handle_df = handle_df_list[self.dataFrame_Tab.currentIndex()-1]
        
        #Lemma에 찾고자 하는 정보가 들어왔을 때 실행 되는 코드
        if self.FLemma_Input.text () != '':
            statelis = [0]
            FComboDict = {'Equals': 1, 'Starts with': 2, 'Ends with': 3, 'Contains': 4, 'is empty': 5}
            #LemmaCombo박스에 선택된 것을 보고 Equal, start, End, contain, empty를 판별하여
            # 해당 단어의 value값을 statelis에 넣어준다.  
            statelis.insert (0, FComboDict[self.FLemmaCombo.currentText ()])

            #statelis에 있는 value값에 따라 해당 코드를 실행시켜준다.
            if statelis[0] == 1:
                handle_df = Equals (handle_df, 'Lemma', self.FLemma_Input.text ())
            if statelis[0] == 2:
                handle_df = Starts_With (handle_df, 'Lemma', self.FLemma_Input.text ())
            if statelis[0] == 3:
                handle_df = Ends_With (handle_df, 'Lemma', self.FLemma_Input.text())
            if statelis[0] == 4:
                handle_df = Contains (handle_df, 'Lemma', self.FLemma_Input.text())
            if statelis[0] == 5:
                handle_df = Is_Empty (handle_df, 'Lemma', self.FLemma_Input.text())

            self.readFiles2 (handle_df)
        
        #Entry에 찾고자 하는 정보가 들어왔을 때 실행 되는 코드
        if self.FEntry_Input.text () != '':
            statelis = [0]
            FComboDict = {'Equals': 1, 'Starts with': 2, 'Ends with': 3, 'Contains': 4, 'is empty': 5}
            statelis.insert (0, FComboDict[self.FEntryCombo.currentText ()])
            
            if statelis[0] == 1:
                handle_df = Equals (handle_df, 'Entry', self.FEntry_Input.text ())
            if statelis[0] == 2:
                handle_df = Starts_With (handle_df, 'Entry', self.FEntry_Input.text ())
            if statelis[0] == 3:
                handle_df = Ends_With (handle_df, 'Entry', self.FEntry_Input.text())
            if statelis[0] == 4:
                handle_df = Contains (handle_df, 'Entry', self.FEntry_Input.text())
            if statelis[0] == 5:
                handle_df = Is_Empty (handle_df, 'Entry', self.FEntry_Input.text())

            self.readFiles2 (handle_df)
        

        #Category에 원하는 정보가 들어왔을 때 실행되는 코드
        if self.FCate_Input.text () != '':
            statelis = [0]
            FComboDict = {'Equals': 1, 'Starts with': 2, 'Ends with': 3, 'Contains': 4, 'is empty': 5}
            statelis.insert (0, FComboDict[self.FCateCombo.currentText ()])
            
            if statelis[0] == 1:
                handle_df = Equals (handle_df, 'Category', self.FCate_Input.text ())
            if statelis[0] == 2:
                handle_df = Starts_With (handle_df, 'Category', self.FCate_Input.text ())
            if statelis[0] == 3:
                handle_df = Ends_With (handle_df, 'Category', self.FCate_Input.text())
            if statelis[0] == 4:
                handle_df = Contains (handle_df, 'Category', self.FCate_Input.text())
            if statelis[0] == 5:
                handle_df = Is_Empty (handle_df, 'Category', self.FCate_Input.text())

            self.readFiles2 (handle_df)
        
        #Information에 원하는 정보가 들어있을 경우
        if self.FInfo_Input.text () != '':
            statelis = [0]
            FComboDict = {'Equals': 1, 'Starts with': 2, 'Ends with': 3, 'Contains': 4, 'is empty': 5}
            statelis.insert (0, FComboDict[self.FInfoCombo.currentText ()])

            #사용자가 colum name을 직접 설정할 경우
            if self.FInfo_Colname.text() != '':
                if statelis[0] == 1:
                    handle_df = Equals (handle_df, self.FInfo_Colname.text(), self.FInfo_Input.text ())
                if statelis[0] == 2:
                    handle_df = Starts_With (handle_df, self.FInfo_Colname.text(), self.FInfo_Input.text ())
                if statelis[0] == 3:
                    handle_df = Ends_With (handle_df, self.FInfo_Colname.text(), self.FInfo_Input.text())
                if statelis[0] == 4:
                    handle_df = Contains (handle_df, self.FInfo_Colname.text(), self.FInfo_Input.text())
                if statelis[0] == 5:
                    handle_df = Is_Empty (handle_df, self.FInfo_Colname.text(), self.FInfo_Input.text())

                self.readFiles2 (handle_df)
            
            #사용자가 column name을 설정하지 않은 경우
            else:
                if statelis[0] == 1:
                    handle_df = Equals (handle_df, 'Lemma', self.FLemma_Input.text ())
                if statelis[0] == 2:
                    handle_df = Starts_With (handle_df, 'Lemma', self.FLemma_Input.text ())
                if statelis[0] == 3:
                    handle_df = Ends_With (handle_df, 'Lemma', self.FLemma_Input.text())
                if statelis[0] == 4:
                    handle_df = Contains (handle_df, 'Lemma', self.FLemma_Input.text())
                if statelis[0] == 5:
                    handle_df = Is_Empty (handle_df, 'Lemma', self.FLemma_Input.text())
            

            self.readFiles2 (handle_df)

        #Fisrt Syllable
        if self.FFirst_1.text() != '' or self.FFirst_2.text() != '' or self.FFirst_3.text() != '':
            handle_df = First_Syllable(handle_df, self.FFirst_1.text(), self.FFirst_2.text(), self.FFirst_3.text())

            self.readFiles2 (handle_df)

        #Second Syllable  
        if self.FSec_1.text() != '' or self.FSec_2.text() != '' or self.FSec_3.text() != '':
            handle_df = Second_Syllable(handle_df, self.FSec_1.text(), self.FSec_2.text(), self.FSec_3.text())

            self.readFiles2 (handle_df)

        #Second to Last syllable
        if self.FSecL_1.text() != '' or self.FSecL_2.text() != '' or self.FSecL_3.text() != '':
            handle_df = Second_to_Last_Syllable(handle_df, self.FSecL_1.text(), self.FSecL_2.text(), self.FSecL_3.text())

            self.readFiles2 (handle_df)
        
        #Last Syllable
        if self.FLast_1.text() != '' or self.FLast_2.text() != '' or self.FLast_3.text() != '':
            handle_df = Last_Syllable(handle_df, self.FLast_1.text(), self.FLast_2.text(), self.FLast_3.text())

            self.readFiles2 (handle_df)

        handle_df_list[self.dataFrame_Tab.currentIndex() -1 ] = handle_df
        print( handle_df_list[self.dataFrame_Tab.currentIndex() -1 ] )

    #show버튼을 누르면 원본 데이터를 보여주는 함수
    def show_all(self):
        global handle_df

        print(self.dataFrame_Tab.currentIndex())
        handle_df = original_df_list[self.dataFrame_Tab.currentIndex()-1].copy()

        self.readFiles2 (handle_df)


    ######################
    ##Edit Function 함수##
    ######################


    #Add function에서 ok를 누르면 실행될 함수

    def add_function(self):
        global handle_df

        handle_df = handle_df_list[self.dataFrame_Tab.currentIndex()-1]
        ##입력값 텍스트화
        add_col_txt = str(self.Add_column.currentText())  ##combobox는 currentText()사용
        add_pos_txt = str(self.Add_position.currentText())
        add_new_txt = str(self.Add_oldText.text())
        handle_df = add(handle_df, add_col_txt, add_pos_txt, add_new_txt) ##새로운 변수에 저장하기
        #     handle_df (작업창에 떠있는 데이터프레임),

        self.readFiles2 (handle_df) ##readfiles함수에 넣으면 나타남.    

    #Remove Function에서 ok를 누르면 실행될 함수

    def remove_function(self):
        global handle_df

        handle_df = handle_df_list[self.dataFrame_Tab.currentIndex()-1]

        ##입력값 텍스트화
        rem_col_txt = str(self.Remove_column.currentText())
        rem_pos_txt = str(self.Remove_position.currentText())
        rem_old_txt = str(self.Remove_oldText.text())
        
        handle_df = rmv(handle_df, rem_col_txt, rem_pos_txt, rem_old_txt)

        self.readFiles2 (handle_df)

    #Replace Function에서 ok를 누르면 실행될 함수
    
    def replace_function(self):
        global handle_df

        handle_df = handle_df_list[self.dataFrame_Tab.currentIndex()-1]

        ##입력값 텍스트화
        rep_col_txt = str(self.Replace_column.currentText())
        rep_pos_txt = str(self.Replace_position.currentText())
        rep_old_txt = str(self.Replace_oldtext.text())
        rep_new_txt = str(self.Replace_newtext.text())
        
        if rep_pos_txt == 'anywhere':
            handle_df = anywhere_rpl(handle_df, rep_col_txt, rep_old_txt, rep_new_txt)
        if rep_pos_txt == 'whole string':
            handle_df = whole_rpl(handle_df, rep_col_txt, rep_old_txt, rep_new_txt)
        if rep_pos_txt == 'beginning':
            handle_df = begin_rpl(handle_df, rep_col_txt, rep_old_txt, rep_new_txt)
        if rep_pos_txt == 'ending':
            handle_df = end_rpl(handle_df, rep_col_txt, rep_old_txt, rep_new_txt)

        self.readFiles2(handle_df)

    #Replace Function에서 ok를 누르면 실행될 함수

    def irregular_function(self):
        global handle_df

        handle_df = handle_df_list[self.dataFrame_Tab.currentIndex()-1]

        fin_con_txt = str(self.Irreg_cons.text())
        old_inf_txt = str(self.Irreg_oldinflec.text())
        new_inf_txt = str(self.irreg_newinflec.text())

        handle_df = irreg(handle_df, fin_con_txt, old_inf_txt, new_inf_txt)

        self.readFiles2(handle_df)

    ##Add row 버튼을 누르면 실행될 함수

    def add_row_function(self):
        global handle_df

        handle_df = handle_df_list[self.dataFrame_Tab.currentIndex()-1]

        handle_df = addrow(handle_df)

        self.readFiles2(handle_df)

    ##Delete row 버튼을 누르면 실행될 함수

    def delete_row_function(self):
        global handle_df

        handle_df = handle_df_list[self.dataFrame_Tab.currentIndex()-1]

        handle_df = delrow(handle_df)
        
        self.readFiles2(handle_df)

        
    ##Duplicate row 버튼을 누르면 실행될 함수
    def duplicate_row_function(self):
        global handle_df
        global alpha

        handle_df = handle_df_list[self.dataFrame_Tab.currentIndex()-1]

        cell_idx = alpha[self.dataFrame_Tab.currentIndex()-1].selectedIndexes() #선택한 행의 인덱스 정보 반환하는 함수

        sel_cells = list(set(( idx.row() for idx in cell_idx))) ##인덱스 정보 중 row의 인덱스 값(정수)로 변환
        # sel_cell = self.new_tableWidget.currentRow()  선택한 단일의 행의 인덱스 값(정수)반환하는 함수 

        for i in sel_cells:
            handle_df = duprow(handle_df, i)

        self.readFiles2(handle_df)
        
       

        #return tab_name_dic[self.dataFrame_Tab.currentWidget()]

    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Deco_LexO = QtWidgets.QMainWindow()
    ui = Ui_Deco_LexO()
    ui.setupUi(Deco_LexO)
    Deco_LexO.show()
    sys.exit(app.exec_())
