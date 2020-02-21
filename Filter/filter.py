import pandas as pd
import numpy as np
import os, re

df = pd.read_csv(r'E:\Programming\python\NLP\DecoLexO\DecoLexO\Edit\example\DECO-Ver5.2-NS-2019-Kernel-DevTest.csv',encoding = 'utf-8-sig')

def column_name(df):
    #첫 행 살리기
    first = list(df.columns)
    df.loc[0] = first
    for val in first:
        if 'Unnamed' in val:
            x = first.index(val)
            first[x] = np.nan
    df.loc[0] = first

    df = df.fillna('')
    sem_rgx = re.compile(r'[Q][A-Z]{3}')  #semantic tagset
    syn_rgx = re.compile(r'[Y][A-Z]{3}')  #syntactic tagset
    dom_rgx = re.compile(r'[X]{1}[ABCDEFGHIJKLMNOPQRSTUVWYZ]{3}')  #domain tagset
    ent_rgx = re.compile(r'[X]{2}[A-Z]{2}') #entity tagset
    mor_rgx = re.compile(r'[A-Z]{3}') #morph tagset

    #컬럼의 총 개수를 l에 저장한다.
    #컬럼의 개수 만큼 lemma와 category뒤에 lemma와 category개수인 2를 뺀만큼
    #''를 추가해 주어 해당 컬럼 개수 만큼의 리스트 col_nme을 만들어 준다.
    l = len(df.columns)
    col_nme = ['Lemma','Category']
    for i in range(l-2):
        col_nme.append('')
    #sem =>SemInfo 뒤에 붙을 숫자 
    #syn =>SynInfo 뒤에 붙을 숫자 
    #dom =>DomInfo 뒤에 붙을 숫자 
    #ent =>EntInfo 뒤에 붙을 숫자 
    #mor =>MorInfo 뒤에 붙을 숫자 
    sem = 1
    syn = 1
    dom = 1
    ent = 1
    mor = 1

    #x를 컬럼의 개수 만큼의 숫자로 지정해 준다.
    #col_val은 해당 df의 열을 리스트화 시켜준 것이다.
    for x in range(0, l):
        col_val = df.iloc[:, x].tolist()
        #cnt가 0이면 일치하는 값을 못 찾았다는 의미로 해석(ex 모두 빈칸인 열을 만났을 때)
        #밑에서 cnt == 0 일때 앞에 정보를 보고 빈칸의 정보를 수정할 때 사용한다.
        cnt = 0
        #k로 col_val의 리스트 요소들을 하나씩 지정해주면서
        #k가 sem_rgx, syn_rgx, dom_rgx, ent_rgx, mor_rgx에 해당되면
        #컬럼에 일치하는 값이 있었다는 의미로 cnt를 1 증가시켜 주고
        #Info뒤에 붙을 숫자를 1씩 증가시켜 주고
        #비효율적인 탐색을 막기 위해 바로 break시켜준다.
        for k in col_val:
            if sem_rgx.match(k):
                col_nme[x] = 'SemInfo' + str(sem)
                sem += 1
                cnt += 1
                break

            elif syn_rgx.match(k):
                col_nme[x] = 'SynInfo' + str(syn)
                syn += 1
                cnt += 1
                break

            elif dom_rgx.match(k):
                col_nme[x] = 'DomInfo' + str(dom)
                dom += 1
                cnt += 1
                break

            elif ent_rgx.match(k):
                col_nme[x] = 'EntInfo' + str(ent)
                ent += 1
                cnt += 1
                break

            elif mor_rgx.match(k):
                col_nme[x] = 'MorInfo' + str(mor)
                mor += 1 
                cnt += 1
                break

        #만약 위에서 일치하는 값을 못찾았을 때(ex 모두 빈칸인 열이었을 때)
        #cnt는 0이므로 앞에 col_nme의 정보를 보고 
        #해당 정보와 일치하는 정보의 Info숫자를 증가시켜준 값을 해당 리스트 위치에 저장해준다.
        if cnt == 0:
            if 'Sem' in col_nme[x-1]:
                col_nme[x] = 'SemInfo' + str(sem)
                sem+=1
                
            elif 'Syn' in col_nme[x-1]:
                col_nme[x] =  'SynInfo' + str(syn)
                syn+=1
            
            elif 'Dom' in col_nme[x-1]:
                col_nme[x] =  'DomInfo' + str(dom)
                dom+=1
                
            elif 'Ent' in col_nme[x-1]:
                col_nme[x] =  'EntInfo' + str(ent)
                ent+=1
                
            elif 'Mor' in col_nme[x-1]:
                col_nme[x] =  'MorInfo' + str(mor)
                mor+=1

    df.columns = col_nme

    return df

#입력받은 word와 같은 단어 정보들을 출력하는 함수
def Equals(df, col, word):
    for i in range(len(word)):
        for j in range(len(df)):
            if df.loc[j,col] == word[i]:
                answer  = df.iloc[j]
            
    #result는 series로 저장되어 있기 때문에 to_frame()으로 df화 해주고
    #현재 row와 column이 바뀌어 저장되어 있기 때문에
    #.T로 transepose() 기능을 주어 row와 column을 바꾸어 준다.
    result = answer.to_frame().T
    header = result.columns
    result.to_csv('filter_result.csv', columns = header, index = False, encoding ='utf-8-sig') 


#입력받은 단어들이 포함되어 있는 단어 정보들을 출력하는 함수
def Contains(df, col, word):
    
    cnt = 0
    
    for i in range(len(word)):
        for j in range(len(df)):
            if word[i] in df.loc[j,col]:
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
            
            
#입력받은 단어들로 시작하는 단어 정보들을 출력하는 함수
def Starts_With(df, col, word):
    cnt = 0
    for i in range(len(word)):
        for j in range(len(df)):
            if df.loc[j,col].startswith(word[i]):
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
            

#입력받은 단어들로 끝나는 단어 정보들을 출력하는 하수
def Ends_With(df, col, word):

    cnt = 0
    
    for i in range(len(word)):
        for j in range(len(df)):
            if df.loc[j,col].endswith(word[i]):
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

#Entry, lemma, category, information을 입력하면 각각 statelis에 저장한다.
statelis = [0,0,0,0]

#entry에 pass를 입력하지 않으면
#state1에 출력하고 싶은 정보를 숫자로 입력하고
#그 정보를 statelis에 숫자로 저장해준다.
#entry_ele에는 단어 요소들을 저장해 주는데
#여러 단어를 입력받을 시 + 로 붙여서 입력해주고
#split('+')을 통해 나누어준 상태로 저장해준다.
entry = input('Entry(If you don\'t want enter pass): ')
if entry != 'pass':
    state1 = int(input('Equals(1), Start_with(2), Ends_with(3), Contains(4), Is_empty(5): '))
    statelis.insert(0, state1)
    entry_ele = input('ex) 가+나+다: ')
    if len(entry_ele) > 1:
        entry_ele.split('+')
    else:
        pass


#lemma에 pass를 입력하지 않으면
#state2에 출력하고 싶은 정보를 숫자로 입력하고
#그 정보를 statelis에 숫자로 저장해준다.
#lemma_ele에는 단어 요소들을 저장해 주는데
#여러 단어를 입력받을 시 + 로 붙여서 입력해주고
#split('+')을 통해 나누어준 상태로 저장해준다.
lemma = input('Lemma(If you don\'t want enter pass): ')
if lemma != 'pass':
    state2 = int(input('Equals(1), Start_with(2), Ends_with(3), Contains(4), Is_empty(5): '))
    statelis.insert(1, state2)
    lemma_ele = input('ex) 가+나+다: ')
    if len(lemma_ele) > 1:
        lemma_ele.split('+')
    else:
        pass


#category에 pass를 입력하지 않으면
#state3에 출력하고 싶은 정보를 숫자로 입력하고
#그 정보를 statelis에 숫자로 저장해준다.
#cate_ele에는 단어 요소들을 저장해 주는데
#여러 단어를 입력받을 시 + 로 붙여서 입력해주고
#split('+')을 통해 나누어준 상태로 저장해준다.
category = input('Category(If you don\'t want enter pass): ')
if category != 'pass':
    state3 = int(input('Equals(1), Start_with(2), Ends_with(3), Contains(4), Is_empty(5): '))
    statelis.insert(2, state3)
    cate_ele = input('ex) 가+나+다: ')
    if len(cate_ele) > 1:
        cate_ele.split('+')
    else:
        pass

 
#info에 pass를 입력하지 않으면
#state4에 출력하고 싶은 정보를 숫자로 입력하고
#그 정보를 statelis에 숫자로 저장해준다.
#info_ele에는 단어 요소들을 저장해 주는데
#여러 단어를 입력받을 시 + 로 붙여서 입력해주고
#split('+')을 통해 나누어준 상태로 저장해준다.
info = input('Information(If you don\'t want enter pass): ')
if info != 'pass':
    state4 = int(input('Equals(1), Start_with(2), Ends_with(3), Contains(4), Is_empty(5): '))
    statelis.insert(3, state4)
    info_ele = input('ex) 가+나+다:')
    if len(info_ele) > 1:
        info_ele.split('+')
    else:
        pass

#정보를 한번 result.csv에 쓰면 cnt를 1 증가시켜서 처음 읽어들인 df가 아닌
#result 파일을 함수에 넣어 줄 수 있게 카운트를 도와주는 변수
cnt = 0
df = column_name(df)

for i in range(len(statelis)):
    #cnt가 0이 아니면 copy에 result파일을 넣어주고
    #cnt가 0이면 copy에 df파일을 넣어준다.
    if cnt != 0:
        copy = pd.read_csv(r'C:\Users\LEE Sunghyun\Documents\Python Scripts\filter_result.csv',encoding = 'utf-8-sig')
    else:
        copy = df

    #statelis[i]에 저장된 숫자로 eqals, start, end 와 같은 정보를 알아내고
    # 그 숫자에 맞는 함수에 copy와 column과 단어 요소들을 넣어준다. 
    if statelis[i] == 0:
        pass
    else:
        if i == 0:
            if statelis[i] == 1:
                Equals(copy, 'Entry', entry_ele)
            elif statelis[i] == 2:
                Starts_With(copy, 'Entry', entry_ele)
            elif statelis[i] == 3:
                Ends_With(copy, 'Entry', entry_ele)
            elif statelis[i] == 4:
                Contains(copy, 'Entry', entry_ele)
            elif statelis[i] == 5:
                Is_Empty(copy, 'Entry', entry_ele)
            cnt += 1

        elif i == 1:
            if statelis[i] == 1:
                Equals(copy, 'Lemma', lemma_ele)
            elif statelis[i] == 2:
                Starts_With(copy, 'Lemma', lemma_ele)
            elif statelis[i] == 3:
                Ends_With(copy, 'Lemma', lemma_ele)
            elif statelis[i] == 4:
                Contains(copy, 'Lemma', lemma_ele)
            elif statelis[i] == 5:
                Is_Empty(copy, 'Lemma', lemma_ele)
            cnt += 1

        elif i == 2:
            if statelis[i] == 1:
                Equals(copy, 'Category', cate_ele)
            elif statelis[i] == 2:
                Starts_With(copy, 'Category', cate_ele)
            elif statelis[i] == 3:
                Ends_With(copy, 'Category', cate_ele)
            elif statelis[i] == 4:
                Contains(copy, 'Category', cate_ele)
            elif statelis[i] == 5:
                Is_Empty(copy, 'Category', cate_ele)
            cnt += 1

        elif i == 3:
            if statelis[i] == 1:
                Equals(copy, info, info_ele)
            elif statelis[i] == 2:
                Starts_With(copy, info, info_ele)
            elif statelis[i] == 3:
                Ends_With(copy, info, info_ele)
            elif statelis[i] == 4:
                Contains(copy, info, info_ele)
            elif statelis[i] == 5:
                Is_Empty(copy, info, info_ele)
            cnt += 1
            