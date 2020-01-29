import pandas as pd
import numpy as np
import os, re

df = pd.read_csv(r'G:\Programming\python\NLP\DecoLexO\DecoLexO\Edit\example\DecoLex_Test.csv')

print(df)

####행 이름 decolex처럼 변경하기####

#첫 행 살리기
col_rgx = re.compile(r'(.*)') ##모든 문자열을 찾기(.이나 Unnamed나)
first = list(df.columns)
df.loc[0] = first
for val in first:
    m = col_rgx.match(val)
    if m:
        x = first.index(val)
        first[x] = np.nan
df.loc[0] = first

#행 이름 설정해주기
col_nme = ['Lemma','Category','Morph1']

l = len(df.columns)
print(2)
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

where = input('where? ')
ori = input('original: ')
new = input('new: ')
col = input('column name(Lemma or Category): ')

if where == 'anywhere':
    anywhere_rpl(df, col, ori, new)
if where == 'whole string':
    whole_rpl(df, col, ori, new)
if where == 'begin':
    begin_rpl(df, col, ori, new)
if where == 'end':
    end_rpl(df, col, ori, new)