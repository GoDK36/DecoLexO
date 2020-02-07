import pandas as pd
import numpy as np
import os, re

df = pd.read_csv(r'E:\Programming\python\NLP\DecoLexO\DecoLexO\Edit\example\DECO-Ver5.2-NS-2019-Kernel-DevTest.csv')


####행 이름 decolex처럼 변경하기####

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

#행 이름 설정해주기
col_nme = ['Lemma','Category','Morph1']

l = len(df.columns)
for i in range(1, l - 2):
    info = 'info' + str(i)
    col_nme.append(info)

df.columns = col_nme


#편집을 원하는 행을 리스트화 하는 함수
#df에는 불러온 데이터프레임을 넣고 col에는 수정 원하는 행 이름을 삽입
def df2first(df,col):
    col_first = list(df.columns)
    x = col_first.index(col)
    res = df.iloc[:,x:x+1].values.tolist()
    res = sum(res,[])
    return res

#add하기    
def add(df, col, add_place, add_text):
    res = []
    first = df2first(df,col)
    if add_place == 'begin':
        for x in first:
            res.append(add_text + x)
    if add_place == 'end':
        for x in first:
            res.append(x + add_text)   
    #열 추가
    del df[col]
    df[col] = res
    
    #열 위치 재정렬
    df = df[col_nme]
    
    print(df)

add(df, input('수정을 원하는 행 이름 선택(Lemma, Category) '), input('begin or end? '), input('add text: '))