import pandas as pd
import re
import csv
import sys

f = open('DECO-Ver5.2-NS-2019-Kernel-DevTest.csv','r', encoding = 'utf-8-sig')
df = csv.reader(f)

def Start_With(word, text):
    print(word)

    result = []
    info = []
    for line in text:
        start = ""
        for i in line[0]:
            start += i
            if start == word:
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


start = Start_With('개',df)
print(start)
