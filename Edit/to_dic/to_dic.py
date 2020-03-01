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

####dic작성 시작####
def df2dic(df, filepath, filename):

    #딕셔너리 자료형의 특징을 이용하여 리스트 요소 순서를 유지하며 중복 제거하기
    from collections import OrderedDict

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
    f = open(filepath + '\\' + filename + '.dic', 'w', encoding='utf-8-sig')



    for i in range(len(dic_lst)):
        f.write('%s \n' % dic_lst[i])


    f.close()

df2dic(df, input('저장경로를 적어주세요: '), input('저장할 파일의 이름은? '))