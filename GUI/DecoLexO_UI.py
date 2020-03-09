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

#입력받은 단어들로 시작하는 단어 정보들을 출력하는 함수
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

#입력받은 단어들로 끝나는 단어 정보들을 출력하는 함수
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

#입력받은 단어들이 없는 단어 정보들을 출력하는 함수
def Is_Empty(df, col, word):
    
    cnt = 0
    
    for i in range(len(word)):
        for j in range(len(df)):
            if word[i] not in df.loc[j,col]:
                if cnt == 0:
                    result = df.iloc[j]
                    result = result.to_frame().T
                    header = result.columns
                    result.to_csv('filter_result.csv', columns = header, index = False, encoding ='utf-8-sig') 
                    cnt += 1
                elif cnt != 0:
                    result = df.iloc[j]
                    result = result.to_frame().T
                    result.to_csv('filter_result.csv', mode = 'a', header = False, index = False, encoding ='utf-8-sig') 

#함수를 읽어 주는 함수
def readFiles(new_tableWidget, df):
        newdf = column_name (df)
        new_tableWidget.setColumnCount (len (newdf.columns))
        header = newdf.columns
        new_tableWidget.setHorizontalHeaderLabels (header)
        new_tableWidget.setRowCount (len (newdf.index))
        for i in range (len (newdf.index)):
            for j in range (len (newdf.columns)):
                new_tableWidget.setItem (i, j, QtWidgets.QTableWidgetItem (str (newdf.iat[i, j])))

        new_tableWidget.resizeColumnsToContents ()
        new_tableWidget.resizeRowsToContents ()

#편집을 원하는 행을 리스트화 하는 함수
#df에는 불러온 데이터프레임을 넣고 col에는 수정 원하는 행 이름을 삽입
def df2first(df,col):
    col_first = list(df.columns)
    x = col_first.index(col)
    res = df.iloc[:,x:x+1].values.tolist()
    res = sum(res,[])
    return res

#Edit section 

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

def Divide(korean_word):
    global initial
    global mid
    global final

    r_lst = []
    for w in list(korean_word.strip()):
        ## 영어인 경우 구분해서 작성함. 
        if '가'<=w<='힣':
            ## 588개 마다 초성이 바뀜. 
            ch1 = (ord(w) - ord('가'))//588
            ## 중성은 총 28가지 종류
            ch2 = ((ord(w) - ord('가')) - (588*ch1)) // 28
            ch3 = (ord(w) - ord('가')) - (588*ch1) - 28*ch2
            r_lst.append([initial[ch1], mid[ch2], final[ch3]])
        else:
            r_lst.append([w])
    return r_lst

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

#끝음절 replace 함수 (어미 바꾸기 용)
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

        self.FFirst_1 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FFirst_1.setGeometry (QtCore.QRect (30, 320, 51, 21))
        self.FFirst_1.setObjectName ("FFirst_1")
        self.FFirst_2 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FFirst_2.setGeometry (QtCore.QRect (100, 320, 51, 21))
        self.FFirst_2.setObjectName ("FFirst_2")
        self.FFirst_3 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FFirst_3.setGeometry (QtCore.QRect (170, 320, 51, 21))
        self.FFirst_3.setObjectName ("FFirst_3")
        self.FSec_3 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FSec_3.setGeometry (QtCore.QRect (170, 370, 51, 21))
        self.FSec_3.setObjectName ("FSec_3")
        self.FSec_2 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FSec_2.setGeometry (QtCore.QRect (100, 370, 51, 21))
        self.FSec_2.setObjectName ("FSec_2")
        self.FSec_1 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FSec_1.setGeometry (QtCore.QRect (30, 370, 51, 21))
        self.FSec_1.setObjectName ("FSec_1")
        self.FSecL_3 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FSecL_3.setGeometry (QtCore.QRect (170, 420, 51, 21))
        self.FSecL_3.setObjectName ("FSecL_3")
        self.FSecL_2 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FSecL_2.setGeometry (QtCore.QRect (100, 420, 51, 21))
        self.FSecL_2.setObjectName ("FSecL_2")
        self.FSecL_1 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FSecL_1.setGeometry (QtCore.QRect (30, 420, 51, 21))
        self.FSecL_1.setObjectName ("FSecL_1")
        self.FLast3 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FLast3.setGeometry (QtCore.QRect (170, 470, 51, 21))
        self.FLast3.setObjectName ("FLast3")
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
        self.FFiltering_Button = QtWidgets.QPushButton (self.Modifying_Tab)
        self.FFiltering_Button.setGeometry (QtCore.QRect (20, 550, 75, 23))
        self.FFiltering_Button.setObjectName ("FFiltering_Button")
        self.FShow_Button = QtWidgets.QPushButton (self.Modifying_Tab)
        self.FShow_Button.setGeometry (QtCore.QRect (110, 550, 75, 23))
        self.FShow_Button.setObjectName ("FShow_Button")
        self.FShow_Button.clicked.connect(lambda parameter_list: self.openFiles())
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
        self.tabWidget_1.addTab(self.Modifying_Tab, "")
        self.Edit_Tab = QtWidgets.QWidget()
        self.Edit_Tab.setObjectName("Edit_Tab")
        self.Push_addrow = QtWidgets.QPushButton(self.Edit_Tab)
        self.Push_addrow.setGeometry(QtCore.QRect(20, 530, 130, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Push_addrow.setFont(font)
        self.Push_addrow.setObjectName("Push_addrow")
        self.Push_Deleterow = QtWidgets.QPushButton(self.Edit_Tab)
        self.Push_Deleterow.setGeometry(QtCore.QRect(170, 530, 140, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Push_Deleterow.setFont(font)
        self.Push_Deleterow.setObjectName("Push_Deleterow")
        self.Push_Duplicaterow = QtWidgets.QPushButton(self.Edit_Tab)
        self.Push_Duplicaterow.setGeometry(QtCore.QRect(20, 580, 290, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Push_Duplicaterow.setFont(font)
        self.Push_Duplicaterow.setObjectName("Push_Duplicaterow")
        self.Edit_function_tab = QtWidgets.QTabWidget(self.Edit_Tab)
        self.Edit_function_tab.setGeometry(QtCore.QRect(0, 50, 321, 371))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Edit_function_tab.setFont(font)
        self.Edit_function_tab.setObjectName("Edit_function_tab")
        self.Add_tab = QtWidgets.QWidget()


        ###Edit Section###
        
                ###Add tab###

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


                ####Remove tab#####

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


                ####Replace Tab#####

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
        

                ####Irregular tab#####

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


        self.tabWidget_1.addTab(self.Edit_Tab, "")
        self.gridLayout.addWidget(self.tabWidget_1, 0, 0, 1, 1)
        self.dataFrame_Tab = QtWidgets.QTabWidget(self.centralwidget)
        self.dataFrame_Tab.setObjectName("dataFrame_Tab")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout_2.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.dataFrame_Tab.addTab(self.tab, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.dataFrame_Tab.addTab(self.tab_5, "")
        self.gridLayout.addWidget(self.dataFrame_Tab, 0, 1, 1, 1)
        Deco_LexO.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Deco_LexO)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1015, 26))
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


        self.tabWidget_1.addTab (self.Edit_Tab, "")
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

        ##connenct code##
        self.Add_start.released.connect(self.add_function)
        self.Remove_start.released.connect(self.remove_function)
        self.Replace_start.released.connect(self.replace_function)
        self.Irreg_start.released.connect(self.irregular_function)
        self.Push_addrow.released.connect(self.add_row_function)
        self.Push_Deleterow.released.connect(self.delete_row_function)
        

    def retranslateUi(self, Deco_LexO):
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
        self.Push_addrow.setText(_translate("Deco_LexO", "Add Row"))
        self.Push_Deleterow.setText(_translate("Deco_LexO", "Delete Row"))
        self.Push_Duplicaterow.setText(_translate("Deco_LexO", "Duplicate Row"))
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
        self.tabWidget_1.setTabText (self.tabWidget_1.indexOf (self.Edit_Tab), _translate ("Deco_LexO", "Edit"))
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

    ######################
    ##Edit Function 함수##
    ######################


    #Add function에서 ok를 누르면 실행될 함수

    def add_function(self):
        global handle_df

        ##입력값 텍스트화
        add_col_txt = str(self.Add_column.currentText())  ##combobox는 currentText()사용
        add_pos_txt = str(self.Add_position.currentText())
        add_new_txt = str(self.Add_oldText.text())
        handle_df = add(handle_df, add_col_txt, add_pos_txt, add_new_txt) ##새로운 변수에 저장하기
        #     handle_df,#handledf(작엊창에 떠있는 데이터프레임),
        #     self.Add_column.text(),
        #     self.Add_position.text(),
        #     self.Add_oldText.text()
        # )

        self.readFiles2 (handle_df) ##readfiles함수에 넣으면 나타남.    

    #Remove Function에서 ok를 누르면 실행될 함수

    def remove_function(self):
        global handle_df

        ##입력값 텍스트화
        rem_col_txt = str(self.Remove_column.currentText())
        rem_pos_txt = str(self.Remove_position.currentText())
        rem_old_txt = str(self.Remove_oldText.text())
        
        handle_df = rmv(handle_df, rem_col_txt, rem_pos_txt, rem_old_txt)

        self.readFiles2 (handle_df)

    #Replace Function에서 ok를 누르면 실행될 함수
    
    def replace_function(self):
        global handle_df

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

        fin_con_txt = str(self.Irreg_cons.text())
        old_inf_txt = str(self.Irreg_oldinflec.text())
        new_inf_txt = str(self.irreg_newinflec.text())

        handle_df = irreg(handle_df, fin_con_txt, old_inf_txt, new_inf_txt)

        self.readFiles2(handle_df)

    ##Add row 버튼을 누르면 실행될 함수

    def add_row_function(self):
        global handle_df

        handle_df = addrow(handle_df)

        self.readFiles2(handle_df)

    ##Delete row 버튼을 누르면 실행될 함수

    def delete_row_function(self):
        global handle_df

        handle_df = delrow(handle_df)
        
        self.readFiles2(handle_df)



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication (sys.argv)
    Deco_LexO = QtWidgets.QMainWindow ()
    ui = Ui_Deco_LexO ()
    ui.setupUi (Deco_LexO)
    Deco_LexO.show ()
    sys.exit (app.exec_ ())