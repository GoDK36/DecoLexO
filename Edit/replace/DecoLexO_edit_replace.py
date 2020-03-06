import pandas as pd
import numpy as np
import os, re

df = pd.read_csv(r'E:\Programming\python\NLP\DecoLexO\DecoLexO\Edit\example\DECO-Ver5.2-NS-2019-Kernel-DevTest.csv',encoding = 'utf-8-sig')

#첫 행 살리기
col_rgx = re.compile(r'[A-Za-z]{6,}[:\.]?')
first = list(df.columns)
df.loc[0] = first
for val in first:
    m = col_rgx.match(val)
    if m:
        x = first.index(val)
        first[x] = np.nan
    else:
        continue
df.loc[0] = first

##행 이름 변경하기
df = df.fillna('')
sem_rgx = re.compile(r'[Q][A-Z]{3}')  #semantic tagset
syn_rgx = re.compile(r'[Y][A-Z]{3}')  #syntactic tagset
dom_rgx = re.compile(r'[X]{1}[ABCDEFGHIJKLMNOPQRSTUVWYZ]{3}')  #domain tagset
ent_rgx = re.compile(r'[X]{2}[A-Z]{2}') #entity tagset
mor_rgx = re.compile(r'[A-Z]{3}') #morph tagset
seminfo = []
syninfo = []
dominfo = []
entinfo = []
morinfo = []

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
            col_nme[x] = 'Sem Info' + str(sem)
            sem += 1
            cnt += 1
            break

        elif syn_rgx.match(k):
            col_nme[x] = 'Syn Info' + str(syn)
            syn += 1
            cnt += 1
            break

        elif dom_rgx.match(k):
            col_nme[x] = 'Dom Info' + str(dom)
            dom += 1
            cnt += 1
            break

        elif ent_rgx.match(k):
            col_nme[x] = 'Ent Info' + str(ent)
            ent += 1
            cnt += 1
            break

        elif mor_rgx.match(k):
            col_nme[x] = 'Mor Info' + str(mor)
            mor += 1 
            cnt += 1
            break

    #만약 위에서 일치하는 값을 못찾았을 때(ex 모두 빈칸인 열이었을 때)
    #cnt는 0이므로 앞에 col_nme의 정보를 보고 
    #해당 정보와 일치하는 정보의 Info숫자를 증가시켜준 값을 해당 리스트 위치에 저장해준다.
    if cnt == 0:
        if 'Sem' in col_nme[x-1]:
            col_nme[x] = 'Sem Info' + str(sem)
            sem+=1
            
        elif 'Syn' in col_nme[x-1]:
            col_nme[x] =  'Syn Info' + str(syn)
            syn+=1
        
        elif 'Dom' in col_nme[x-1]:
            col_nme[x] =  'Dom Info' + str(dom)
            dom+=1
            
        elif 'Ent' in col_nme[x-1]:
            col_nme[x] =  'Ent Info' + str(ent)
            ent+=1
            
        elif 'Mor' in col_nme[x-1]:
            col_nme[x] =  'Mor Info' + str(mor)
            mor+=1

df.columns = col_nme

#편집을 원하는 행을 리스트화 하는 함수
#df에는 불러온 데이터프레임을 넣고 col에는 수정 원하는 행 이름을 삽입
def df2first(df,col):
    col_first = list(df.columns)
    x = col_first.index(col)
    res = df.iloc[:,x:x+1].values.tolist()
    res = sum(res,[])
    return res

#whole string replace 함수

def whole_rpl(df, col, original_text, new_text):
    res = []
    first = df2first(df,col)
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
    
    print(df)


##anywhere replace 함수

def anywhere_rpl(df, col, original_text, new_text):
    res = []
    first = df2first(df,col)
    #anywhere에서 replace
    for x in first:
        y = re.sub(original_text, new_text, x)
        res.append(y)
        
    #열 추가
    df[col] = res
    
    #열 위치 재정렬
    df = df[col_nme]
    
    print(df)

##begin replace 함수

def begin_rpl(df, col, original_text, new_text):
    res = []
    first = df2first(df,col)
    #begin에서 replace
    for x in first:
        y = re.sub(r'^' + original_text, new_text, x)
        res.append(y)
        
    #열 추가
    df[col] = res
    
    #열 위치 재정렬
    df = df[col_nme]
    
    print(df)

##end replace 함수

def end_rpl(df, col, original_text, new_text):
    res = []
    first = df2first(df,col)
    #end에서 replace
    for x in first:
        y = re.sub(original_text + '$', new_text, x)
        res.append(y)
        
    #열 추가
    df[col] = res
    
    #열 위치 재정렬
    df = df[col_nme]
    
    print(df)

where = input('검색범위(anywhere, whole string, brgin, end) ')
ori = input('original text: ')
new = input('new text: ')
col = input('column name: ')

if where == 'anywhere':
    anywhere_rpl(df, col, ori, new)
if where == 'whole string':
    whole_rpl(df, col, ori, new)
if where == 'beginning':
    begin_rpl(df, col, ori, new)
if where == 'ending':
    end_rpl(df, col, ori, new)