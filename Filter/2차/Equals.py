import csv


result = []
with open(r'G:\Programming\python\NLP\DecoLexO\DecoLexO\Edit\example\DECO-Ver5.2-NS-2019-Kernel-DevTest.csv', newline='',encoding='utf-8') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
     for row in spamreader:
         result.append(row)

#형태소가 같은 단어들을 찾는 함수
def Equals(word, text):

    
    result = []
    for i in range(len(text)):
        equal = ""
        for line in text[i]:
            if word in line:
                for j in line:
                    if j == ',':
                        equal += ' '
                        result.append(equal)
                        equal = ""
                        pass
                    else:
                        equal += str(j)
                
                
    
    with open(r'G:\Programming\python\NLP\DecoLexO\DecoLexO\Filter\2차\Equals_result.csv', 'w', newline='',encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, quotechar = "'")
        spamwriter.writerow(result)
            
    return result



equal = Equals('가든',result)
print(equal)
