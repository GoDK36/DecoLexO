import pandas as pd
import numpy as np
import os, re

df = pd.read_csv(r'G:\Programming\python\NLP\DecoLexO\DecoLexO\Edit\example\DECO-Ver5.2-NS-2019-Kernel-DevTest.csv')


####행 이름 decolex처럼 변경하기####

#첫 행 살리기
col_rgx = re.compile(r'(.*)')
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


##행 추가
def addrow(df):
    df.loc[len(df)] = np.nan
    return df


##행 삭제

def delrow(df):
    res_df = df.drop(len(df)-1,0)
    return res_df


##행 복제

def duprow(df):
    sel = input('복제를 원하는 행 번호: ')
    res_df = df.append(df.iloc[int(sel)], ignore_index = True)
    return(res_df)
