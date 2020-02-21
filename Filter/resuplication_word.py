import pandas as pd
import numpy as np
import os, re

df1 = pd.read_csv(r'E:\Programming\python\NLP\DecoLexO\DecoLexO\Edit\example\DECO-Ver5.2-NS-2019-Kernel-DevTest.csv',encoding = 'utf-8-sig')
df2 = pd.read_csv(r'E:\Programming\python\NLP\DecoLexO\DecoLexO\Edit\example\DecoLex_Test.csv',encoding = 'utf-8-sig')

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

df1 = column_name(df1)
df2 = column_name(df2)

#첫 번째 파일에서 추출한 lemma들을 df1_lemma 리스트에 저장한다
df1_lemma = []
for i in range(len(df1)):
    df1_lemma.append(df1.loc[i,'Lemma'])


#두 번째 파일에서 추출한 lemma들을 df1_lemma 리스트에 저장한다.
df2_lemma = []
for i in range(len(df2)):
    df2_lemma.append(df2.loc[i,'Lemma'])


#df1_lemma와 df2_lemma에서 
#공통된 단어의 인덱스를 locate리스트에 저장한다.
locate = []
for i in range(len(df1_lemma)):
    for j in range(len(df2_lemma)):
        if df1_lemma[i] == df2_lemma[j]:
            locate.append(df1_lemma.index(df1_lemma[i]))
            locate.append(j)
            break

#공통된 단어를 csv에 적는 함수
def Write(df1, df2, locate):

    #처음 적을 때만 column name들이 써질 수 있게
    #result에 적힌 lemma 인덱스 값들의 index 값이 0일 때만 column name이 출력되게 해주고
    #그 후에는 홀수번째 인덱스 값은 df2에서 짝수번째는 df1에서 정보를 가져온다.
    #df1에서 값이 나올 때는 result.insert(0, "From","First")로 
    #앞에 From column을 추가해주고 출처를 First로 써주고
    #df2에서 값이 나올 때는 result.insert(0, "From","First")로 
    #앞에 From column을 추가해준다 출처를 Second로 표시해준다.
    for i in locate:
        #header가 중복되어 써지는 것을 방지하기 위해 index 값이 0일때만
        #header = True인 정보를 쓰게 한다.
        if locate.index(i) == 0:
            #result변수에 df1에서 locate에 저장되어 있는 i번째 인덱스 정보를 저장한다.
            #result변수는 series로 되어있기 때문에 to_frame()으로 df화 해주고
            #세로로 컬럼과 정보들이 출력되기 때문에 .T로 transpose() 해주어 다시 result에 저장한다.
            result = df1.loc[i]
            result = result.to_frame().T
            #앞에 출처를 알 수 있게 From이라는 이름의 column을 넣어주고
            #df1이면 First를 df2이면 Second라는 정보들을 넣어준다.
            result.head()
            result.insert(0, "From","First")
            header = result.columns
            result.to_csv('reduplication_result.csv', columns = header, index = False, encoding ='utf-8-sig')
        #index값이 짝수 일때는 df1에서 정보를 csv에 write한다.
        #단 to_csv의 mode='a'(추가)이고 header=False이다. 
        elif locate.index(i) % 2 == 0:
            result = df1.loc[i]
            result = result.to_frame().T
            result.head()
            result.insert(0, "From","First")
            result.to_csv('reduplication_result.csv', mode = 'a',header=False, index = False, encoding ='utf-8-sig')
        #index값이 홀수 일때는 df2에서 정보를 csv에 write한다.
        #마찬가지로 to_csv의 mode='a'(추가)이고 header=False이다. 
        else:
            result = df2.loc[i]
            result = result.to_frame().T
            result.head()
            result.insert(0, "From","Second")
            result.to_csv('reduplication_result.csv', mode = 'a',header=False, index = False, encoding ='utf-8-sig')
            
Write(df1, df2, locate)
