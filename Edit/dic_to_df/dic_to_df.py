import pandas as pd
import numpy as np
import re

def dic2df(file_path):
    # dic 파일 전처리
    f1 = open(file_path, "r", encoding='utf-8-sig')
    dic = f1.readlines()
    data = []
    for info in dic:
        info = info.replace(' \n', '')
        syl = info.replace('.', '+')
        syl = syl.split(',')[1:][0]
        info = syl.split('+')

        # 카테고리 만들기
        cat = info[-1]
        cat = cat[-3:]
        cat = cat[0] + 'S' + cat[1:]
        del info[-1]
        del info[1]
        info.insert(1, cat)

        data.append(info)

    # 필요한 정규표현식
    sem_rgx = re.compile(r'[Q][A-Z]{3}')   # semantic tagset
    syn_rgx = re.compile(r'[Y][A-Z]{3}')   # syntactic tagset
    dom_rgx = re.compile(r'[X]{1}[ABCDEFGHIJKLMNOPQRSTUVWYZ]{3}')   # domain tagset
    ent_rgx = re.compile(r'[X]{2}[A-Z]{2}')  # entity tagset
    mor_rgx = re.compile(r'[A-Z]{3}')  # morph tagset
    word_rgx = re.compile(r"[가-힣]+")  # Lemma 찾기
    cat_rgx = re.compile(r"[A-Z]S[0-9]{2}")  # Category 찾기

    ## 리스트에 ''을 추가하여 각 tag의 종류별로 길이 맞추기
    data_lst = []
    for info in data:
        temp_lst = []

        # 처음 Lemma와 Category 찾기 (index 0, 1)
        if len(temp_lst) == 0:
            for tag in info:
                if word_rgx.fullmatch(tag):
                    temp_lst.append(tag)
                elif cat_rgx.fullmatch(tag):
                    temp_lst.append(tag)
        
        # MorInfo 찾기 (index 2 ~ 16, length 17)
        if len(temp_lst) == 2:
            for tag in info:
                if mor_rgx.fullmatch(tag):
                    temp_lst.append(tag)

            # MorInfo tag의 종류는 최대 15개, 15개를 채울때까지 '' 추가
            while len(temp_lst) < 17:
                temp_lst.append('')
        
        # SynInfo 찾기 (index 17 ~ 31, length 32)
        if len(temp_lst) == 17:
            for tag in info:
                if syn_rgx.fullmatch(tag):
                    temp_lst.append(tag)

            # SynInfo tag의 종류는 최대 15개, 15개를 채울때까지 '' 추가
            while len(temp_lst) < 32:
                temp_lst.append('')

        # SemInfo 찾기 (index 32 ~ 46, length 47)
        if len(temp_lst) == 32:
            for tag in info:
                if sem_rgx.fullmatch(tag):
                    temp_lst.append(tag)

            # SemInfo tag의 종류는 최대 15개, 15개를 채울때까지 '' 추가
            while len(temp_lst) < 47:
                temp_lst.append('')

        # EntInfo 찾기 (index 47 ~ 49, length 50)
        if len(temp_lst) == 47:
            for tag in info:
                if ent_rgx.fullmatch(tag):
                    temp_lst.append(tag)

            # EntInfo tag의 종류는 최대 3개, 3개를 채울때까지 '' 추가
            while len(temp_lst) < 50:
                temp_lst.append('')
        # DomInfo 찾기 (index 50 ~ 64, length 65)
        if len(temp_lst) == 50:
            for tag in info:
                if dom_rgx.fullmatch(tag):
                    temp_lst.append(tag)

            # DomInfo tag의 종류는 최대 15개, 15개를 채울때까지 '' 추가
            while len(temp_lst) < 66:
                temp_lst.append('')
        data_lst.append(temp_lst)

    ## 데이터 프레임화
    df = pd.DataFrame(data_lst)
    
    
    return df

    print(dic2df())