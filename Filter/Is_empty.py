import pandas as pd
import re
import csv
import sys

f = open('DECO-Ver5.2-NS-2019-Kernel-DevTest.csv','r', encoding = 'utf-8-sig')
df = csv.reader(f)

def Is_Empty(word, text):

    print(word)
    result = []
    info = []

    
    for line in text:
        if word not in line[0]:
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

empty = Is_Empty('개개인',df)
print(empty)
