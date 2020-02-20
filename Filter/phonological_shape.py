import pandas as pd
import numpy as np
import os, re

df = pd.read_csv(r'C:\Users\LEE Sunghyun\Desktop\NLP\DECO-Ver5.2-NS-2019-Kernel-DevTest.csv',encoding = 'utf-8-sig')

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



    #indexlis에 저장된 인덱스 값들을 하나씩 뽑아내면서
    #i의 index값이 0일때만 column값들을 뽑아내기위해 
    # index값이 0일때와 아닐 때로 나눈다. 
    for i in indexlis:
        if indexlis.index(i) == 0:
            result = df.loc[i] 
            #result는 series로 저장되어 있기 때문에 to_frame()으로 df화 해주고
            #현재 row와 column이 바뀌어 저장되어 있기 때문에
            #.T로 transepose() 기능을 주어 row와 column을 바꾸어 준다.
            result = result.to_frame().T
            header = result.columns
            result.to_csv('phonological_shape.csv', columns = header, index = False, encoding ='utf-8-sig') 
            cnt += 1
        else:
            result = df.loc[i]
            result = result.to_frame().T
            result.to_csv('phonological_shape.csv', mode = 'a', header = False, index = False, encoding ='utf-8-sig') 
        
    print(cnt)

#단어의 두 번째 음절이 입력 받은 a,b,c에 해당 될 때 출력하는 함수
def Second_Syllable(df, a, b, c):
    #'*' => any consonants
    #'.' => any vowels
    #'w' => 초성, 중성, 종성에 한글이 들어 있을 때
    #''  => a,b,c에 입력이 안들어 왔을 때

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
            
    #indexlis에 저장된 인덱스 값들을 하나씩 뽑아내면서
    #i의 index값이 0일때만 column값들을 뽑아내기위해 
    # index값이 0일때와 아닐 때로 나눈다. 
    for i in indexlis:
        if indexlis.index(i) == 0:
            result = df.loc[i]
            #result는 series로 저장되어 있기 때문에 to_frame()으로 df화 해주고
            #현재 row와 column이 바뀌어 저장되어 있기 때문에
            #.T로 transepose() 기능을 주어 row와 column을 바꾸어 준다.
            result = result.to_frame().T
            header = result.columns
            result.to_csv('phonological_shape.csv', columns = header, index = False, encoding ='utf-8-sig') 
            cnt += 1
        else:
            result = df.loc[i]
            result = result.to_frame().T
            result.to_csv('phonological_shape.csv', mode = 'a', header = False, index = False, encoding ='utf-8-sig') 

    for i in indexlis:
        print(df.loc[i,'Lemma'])

    print(cnt)

#뒤에서 두 번째 음절이 입력받은 a,b,c에 해당 될 때 출력 하는 함수
def Second_to_Last_Syllable(df, a, b, c):
    #'*' => any consonants
    #'.' => any vowels
    #'w' => 초성, 중성, 종성에 한글이 들어 있을 때
    #''  => a,b,c에 입력이 안들어 왔을 때

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

    #indexlis에 저장된 인덱스 값들을 하나씩 뽑아내면서
    #i의 index값이 0일때만 column값들을 뽑아내기위해 
    # index값이 0일때와 아닐 때로 나눈다. 
    for i in indexlis:
        if indexlis.index(i) == 0:
            result = df.loc[i]
            #result는 series로 저장되어 있기 때문에 to_frame()으로 df화 해주고
            #현재 row와 column이 바뀌어 저장되어 있기 때문에
            #.T로 transepose() 기능을 주어 row와 column을 바꾸어 준다.
            result = result.to_frame().T
            header = result.columns
            result.to_csv('phonological_shape.csv', columns = header, index = False, encoding ='utf-8-sig') 
            cnt += 1
        else:
            result = df.loc[i]
            result = result.to_frame().T
            result.to_csv('phonological_shape.csv', mode = 'a', header = False, index = False, encoding ='utf-8-sig') 
    
    print(cnt)

#단어의 마지막 음절이 입력 받은 a,b,c에 해당 될 때 출력하는 함수
def Last_Syllable(df, a, b, c):
    #'*' => any consonants
    #'.' => any vowels
    #'w' => 초성, 중성, 종성에 한글이 들어 있을 때
    #''  => a,b,c에 입력이 안들어 왔을 때

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

    #indexlis에 저장된 인덱스 값들을 하나씩 뽑아내면서
    #i의 index값이 0일때만 column값들을 뽑아내기위해 
    # index값이 0일때와 아닐 때로 나눈다. 
    for i in indexlis:
        if indexlis.index(i) == 0:
            result = df.loc[i]
            #result는 series로 저장되어 있기 때문에 to_frame()으로 df화 해주고
            #현재 row와 column이 바뀌어 저장되어 있기 때문에
            #.T로 transepose() 기능을 주어 row와 column을 바꾸어 준다.
            result = result.to_frame().T
            header = result.columns
            result.to_csv('phonological_shape.csv', columns = header, index = False, encoding ='utf-8-sig') 
            cnt += 1
        else:
            result = df.loc[i]
            result = result.to_frame().T
            result.to_csv('phonological_shape.csv', mode = 'a', header = False, index = False, encoding ='utf-8-sig') 
    
    print(cnt)

#정보가 입력됐음을 알려주는 리스트
#0이 아닌 다른 숫자가 들어가면 정보가 입력됐음을 알려준다.
result = [0,0,0,0]

first = input('First Syllable(If you don\'t want enter pass): ')
if first != 'pass':
    #정보를 입력하게 되면 First syllable은
    #result[0]에 1을 입력한다.
    result.insert(0, 1)
    cho1 = input('초성(ex) ㄱ+ㄴ+ㄷ): ')
    if len(cho1) > 1:
        cho1.split('+')
    jun1 = input('중성(ex) ㅏ+ㅗ+ㅜ): ')
    if len(jun1) > 1:
        jun1.split('+')
    jon1 = input('종성(ex) ㄹ+ㅁ+ㄵ): ')
    if len(jon1) > 1:
        jon1.split('+')

second = input('Second Syllable(If you don\'t want enter pass): ')
if second != 'pass':
    #정보를 입력하게 되면 Second syllable은
    #result[1]에 1을 입력한다.
    result.insert(1, 1)
    cho2 = input('초성(ex) ㄱ+ㄴ+ㄷ): ')
    if len(cho2) > 1:
        cho2.split('+')
    jun2 = input('중성(ex) ㅏ+ㅗ+ㅜ): ')
    if len(jun2) > 1:
        jun2.split('+')
    jon2 = input('종성(ex) ㄹ+ㅁ+ㄵ): ')
    if len(jon2) > 1:
        jon2.split('+')

sec_t_last = input('Second-to-Last Syllable(If you don\'t want enter pass): ')
if sec_t_last != 'pass':
    #정보를 입력하게 되면 Second_to_last_syllable은
    #result[2]에 1을 입력한다.
    result.insert(2, 1)
    cho2L = input('초성(ex) ㄱ+ㄴ+ㄷ): ')
    if len(cho2L) > 1:
        cho2L.split('+')
    jun2L = input('중성(ex) ㅏ+ㅗ+ㅜ): ')
    if len(jun2L) > 1:
        jun2L.split('+')
    jon2L = input('종성(ex) ㄹ+ㅁ+ㄵ): ')
    if len(jon2L) > 1:
        jon2L.split('+')

last = input('Last Syllable(If you don\'t want enter pass): ')
if last != 'pass':
    #정보를 입력하게 되면 Last syllable은
    #result[3]에 1을 입력한다.
    result.insert(3, 1)
    choL = input('초성(ex) ㄱ+ㄴ+ㄷ): ')
    if len(choL) > 1:
        choL.split('+')
    junL = input('중성(ex) ㅏ+ㅗ+ㅜ): ')
    if len(junL) > 1:
        junL.split('+')
    jonL = input('종성(ex) ㄹ+ㅁ+ㄵ): ')
    if len(jonL) > 1:
        jonL.split('+')
    
cnt = 0
df = column_name(df)

for i in range(len(result)):
    #함수가 한번도 실행이 안됐으면 copy는 그냥 df를 사용하고
    #어떤 함수든 한번이라도 실행 됐을 시에 다음 함수는
    #전 함수에서 만들어진 phonological_syllable.csv를 사 용한다.
    if cnt == 0:
        copy = df
    else:
        copy = pd.read_csv(r'C:\Users\LEE Sunghyun\Documents\Python Scripts\phonological_shape.csv',encoding = 'utf-8-sig')
    
    if i == 0:
        if result[i] != 0:
            First_Syllable(copy, cho1, jun1, jon1)
            cnt += 1
    if i == 1:
        if result[i] != 0:
            Second_Syllable(copy, cho2, jun2, jon2)
            cnt += 1
    if i == 2:
        if result[i] != 0:
            Second_to_Last_Syllable(copy, cho2L, jun2L, jon2L)
            cnt += 1
    if i == 3:
        if result[i] != 0:
            Last_Syllable(copy, choL, junL, jonL)
            cnt += 1
