import pandas as pd
import re
import csv
import sys

f = open('DECO-Ver5.2-NS-2019-Kernel-DevTest.csv','r', encoding = 'utf-8-sig')
df = csv.reader(f)

#입력한 형태소를 포함하고 있는 단어들을 찾는 함수(clear!)
def Contains(word, text):

    result = []
    info = []

    
    for line in text:
        if word in line[0]:
            print(word)
            info.append(line)

    for i in range(len(info)):
        regist = ""
        for j in range(0,64):
            if info[i][j] == '':
               pass
            else:
                regist += info[i][j]
                regist += ' '
        result.append(regist)
        
    return result

cont = Contains('지가', df)
print(cont)
