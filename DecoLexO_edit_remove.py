import pandas as pd
import numpy as np
import os, re

df = pd.read_csv(r'G:\Programming\python\NLP\DecoLexO\DecoLexO\Edit\example\DecoLex_Test.csv')


####행 이름 decolex처럼 변경하기####

#첫 행 살리기
first = list(df.columns)
df.loc[0] = first
for val in first:
    if 'Unnamed' in val:
        x = first.index(val)
        first[x] = np.nan
df.loc[0] = first

#행 이름 설정해주기
col_nme = ['Lemma','Category','Morph1']

for nme in df.columns:
    if 'Unnamed' in nme:
        n_nme = re.sub('Unnamed: ([0-9]+)', 'info\\1',nme)
        col_nme.append(n_nme)
        if len(df.columns) != len(col_nme):
            del col_nme[len(col_nme) - 1]

df.columns = col_nme


#편집을 원하는 행을 리스트화 하는 함수
#df에는 불러온 데이터프레임을 넣고 col에는 수정 원하는 행 이름을 삽입
def df2first(df,col):
    col_first = list(df.columns)
    x = col_first.index(col)
    res = df.iloc[:,x:x+1].values.tolist()
    res = sum(res,[])
    return res

#시작 혹은 끝 부분을 검색하기
def reg(loc):
    if loc == 'begin':
        regex = '^' + input('지울 것은? ')
    if loc == 'end':
        regex = input('지울 것은? ') + '$'
    return(regex)
   
#remove하기    
def rmv(df,col, regex):
    res = []
    k = re.compile(reg(regex))
    first = df2first(df,col)
    for x in first:
        first = k.sub('',x)
        res.append(first)
        
    #열 추가
    del df[col]
    df[col] = res
    
    #열 위치 재정렬
    df = df[col_nme]
    
    print(df)

rmv(df, input('수정을 원하는 행 이름: '), input('begin or end? '))
