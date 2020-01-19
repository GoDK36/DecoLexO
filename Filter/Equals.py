import pandas as pd
import numpy as np
import os
import re
import csv
import sys

f = open('DECO-Ver5.2-NS-2019-Kernel-DevTest.csv','r', encoding = 'utf-8-sig')
df = csv.reader(f)

#형태소가 같은 단어들을 찾는 함수
def Equals(word, text):

    result = []
    for line in text:
        if word in line:
            info = line

    for i in info:
        if i == '':
            pass
        else:
            result.append(i)

    return result



equal = Equals('동네',df)
print(equal)
