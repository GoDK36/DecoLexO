# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DecoLexO.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

import pandas as pd
import numpy as np
import os, re
from PyQt5 import QtCore, QtGui, QtWidgets


def column_name(df):
    # 첫 행 살리기
    first = list (df.columns)
    df.loc[0] = first
    for val in first:
        if 'Unnamed' in val:
            x = first.index (val)
            first[x] = np.nan
    df.loc[0] = first

    df = df.fillna ('')
    sem_rgx = re.compile (r'[Q][A-Z]{3}')  # semantic tagset
    syn_rgx = re.compile (r'[Y][A-Z]{3}')  # syntactic tagset
    dom_rgx = re.compile (r'[X]{1}[ABCDEFGHIJKLMNOPQRSTUVWYZ]{3}')  # domain tagset
    ent_rgx = re.compile (r'[X]{2}[A-Z]{2}')  # entity tagset
    mor_rgx = re.compile (r'[A-Z]{3}')  # morph tagset

    # 컬럼의 총 개수를 l에 저장한다.
    # 컬럼의 개수 만큼 lemma와 category뒤에 lemma와 category개수인 2를 뺀만큼
    # ''를 추가해 주어 해당 컬럼 개수 만큼의 리스트 col_nme을 만들어 준다.
    l = len (df.columns)
    col_nme = ['Lemma', 'Category']
    for i in range (l - 2):
        col_nme.append ('')
    # sem =>SemInfo 뒤에 붙을 숫자
    # syn =>SynInfo 뒤에 붙을 숫자
    # dom =>DomInfo 뒤에 붙을 숫자
    # ent =>EntInfo 뒤에 붙을 숫자
    # mor =>MorInfo 뒤에 붙을 숫자
    sem = 1
    syn = 1
    dom = 1
    ent = 1
    mor = 1

    # x를 컬럼의 개수 만큼의 숫자로 지정해 준다.
    # col_val은 해당 df의 열을 리스트화 시켜준 것이다.
    for x in range (0, l):
        col_val = df.iloc[:, x].tolist ()
        # cnt가 0이면 일치하는 값을 못 찾았다는 의미로 해석(ex 모두 빈칸인 열을 만났을 때)
        # 밑에서 cnt == 0 일때 앞에 정보를 보고 빈칸의 정보를 수정할 때 사용한다.
        cnt = 0
        # k로 col_val의 리스트 요소들을 하나씩 지정해주면서
        # k가 sem_rgx, syn_rgx, dom_rgx, ent_rgx, mor_rgx에 해당되면
        # 컬럼에 일치하는 값이 있었다는 의미로 cnt를 1 증가시켜 주고
        # Info뒤에 붙을 숫자를 1씩 증가시켜 주고
        # 비효율적인 탐색을 막기 위해 바로 break시켜준다.
        for k in col_val:
            if sem_rgx.match (k):
                col_nme[x] = 'SemInfo' + str (sem)
                sem += 1
                cnt += 1
                break

            elif syn_rgx.match (k):
                col_nme[x] = 'SynInfo' + str (syn)
                syn += 1
                cnt += 1
                break

            elif dom_rgx.match (k):
                col_nme[x] = 'DomInfo' + str (dom)
                dom += 1
                cnt += 1
                break

            elif ent_rgx.match (k):
                col_nme[x] = 'EntInfo' + str (ent)
                ent += 1
                cnt += 1
                break

            elif mor_rgx.match (k):
                col_nme[x] = 'MorInfo' + str (mor)
                mor += 1
                cnt += 1
                break

        # 만약 위에서 일치하는 값을 못찾았을 때(ex 모두 빈칸인 열이었을 때)
        # cnt는 0이므로 앞에 col_nme의 정보를 보고
        # 해당 정보와 일치하는 정보의 Info숫자를 증가시켜준 값을 해당 리스트 위치에 저장해준다.
        if cnt == 0:
            if 'Sem' in col_nme[x - 1]:
                col_nme[x] = 'SemInfo' + str (sem)
                sem += 1

            elif 'Syn' in col_nme[x - 1]:
                col_nme[x] = 'SynInfo' + str (syn)
                syn += 1

            elif 'Dom' in col_nme[x - 1]:
                col_nme[x] = 'DomInfo' + str (dom)
                dom += 1

            elif 'Ent' in col_nme[x - 1]:
                col_nme[x] = 'EntInfo' + str (ent)
                ent += 1

            elif 'Mor' in col_nme[x - 1]:
                col_nme[x] = 'MorInfo' + str (mor)
                mor += 1

    df.columns = col_nme

    return df

#입력받은 word와 같은 단어 정보들을 출력하는 함수
def Equals(df, col, word):
    for i in range(len(word)):
        for j in range(len(df)):
            if df.loc[j,col] == word[i]:
                answer  = df.iloc[j]
            
    #result는 series로 저장되어 있기 때문에 to_frame()으로 df화 해주고
    #현재 row와 column이 바뀌어 저장되어 있기 때문에
    #.T로 transepose() 기능을 주어 row와 column을 바꾸어 준다.
    result = answer.to_frame().T
    header = result.columns
    result.to_csv('filter_result.csv', columns = header, index = False, encoding ='utf-8-sig') 


#입력받은 단어들이 포함되어 있는 단어 정보들을 출력하는 함수
def Contains(df, col, word):
    for i in range(len(word)):
        for j in range(len(df)):
            if word[i] in df.loc[j,col]:
                if cnt == 0:
                    result = df.iloc[j]
                    result = result.to_frame().T
                    header = result.columns
                    result.to_csv('filter_result.csv', columns = header, index = False, encoding ='utf-8-sig') 
                    cnt += 1
                elif cnt != 0:
                    result = df.iloc[j]
                    result = result.to_frame().T
                    result.to_csv('filter_result.csv', mode = 'a', header = False, index = False, encoding ='utf-8-sig') 
            
            
#입력받은 단어들로 시작하는 단어 정보들을 출력하는 함수
def Starts_With(df, col, word):
    cnt = 0
    for i in range(len(word)):
        for j in range(len(df)):
            if df.loc[j,col].startswith(word[i]):
                if cnt == 0:
                    result = df.iloc[j]
                    result = result.to_frame().T
                    header = result.columns
                    result.to_csv('filter_result.csv', columns = header, index = False, encoding ='utf-8-sig') 
                    cnt += 1
                elif cnt != 0:
                    result = df.iloc[j]
                    result = result.to_frame().T
                    result.to_csv('filter_result.csv', mode = 'a', header = False, index = False, encoding ='utf-8-sig') 
            

#입력받은 단어들로 끝나는 단어 정보들을 출력하는 함수
def Ends_With(df, col, word):

    cnt = 0
    
    for i in range(len(word)):
        for j in range(len(df)):
            if df.loc[j,col].endswith(word[i]):
                if cnt == 0:
                    result = df.iloc[j]
                    result = result.to_frame().T
                    header = result.columns
                    result.to_csv('filter_result.csv', columns = header, index = False, encoding ='utf-8-sig') 
                    cnt += 1
                elif cnt != 0:
                    result = df.iloc[j]
                    result = result.to_frame().T
                    result.to_csv('filter_result.csv', mode = 'a', header = False, index = False, encoding ='utf-8-sig') 

#입력받은 단어들이 없는 단어 정보들을 출력하는 함수
def Is_Empty(df, col, word):
    
    cnt = 0
    
    for i in range(len(word)):
        for j in range(len(df)):
            if word[i] not in df.loc[j,col]:
                if cnt == 0:
                    result = df.iloc[j]
                    result = result.to_frame().T
                    header = result.columns
                    result.to_csv('filter_result.csv', columns = header, index = False, encoding ='utf-8-sig') 
                    cnt += 1
                elif cnt != 0:
                    result = df.iloc[j]
                    result = result.to_frame().T
                    result.to_csv('filter_result.csv', mode = 'a', header = False, index = False, encoding ='utf-8-sig') 

#함수를 읽어 주는 함수
def readFiles(new_tableWidget, df):
        newdf = column_name (df)
        new_tableWidget.setColumnCount (len (newdf.columns))
        header = newdf.columns
        new_tableWidget.setHorizontalHeaderLabels (header)
        new_tableWidget.setRowCount (len (newdf.index))
        for i in range (len (newdf.index)):
            for j in range (len (newdf.columns)):
                new_tableWidget.setItem (i, j, QtWidgets.QTableWidgetItem (str (newdf.iat[i, j])))

        new_tableWidget.resizeColumnsToContents ()
        new_tableWidget.resizeRowsToContents ()


class Ui_Deco_LexO (object):
    def setupUi(self, Deco_LexO):
        Deco_LexO.setObjectName ("Deco_LexO")
        Deco_LexO.resize (709, 732)
        self.centralwidget = QtWidgets.QWidget (Deco_LexO)
        self.centralwidget.setObjectName ("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout (self.centralwidget)
        self.gridLayout.setObjectName ("gridLayout")
        self.dataFrame_Tab = QtWidgets.QTabWidget (self.centralwidget)
        self.dataFrame_Tab.setObjectName ("dataFrame_Tab")
        self.tab = QtWidgets.QWidget ()
        self.tab.setObjectName ("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout (self.tab)
        self.gridLayout_2.setObjectName ("gridLayout_2")
        self.tableWidget = QtWidgets.QTableWidget (self.tab)
        self.tableWidget.setObjectName ("tableWidget")
        self.tableWidget.setColumnCount (0)
        self.tableWidget.setRowCount (0)
        self.gridLayout_2.addWidget (self.tableWidget, 0, 0, 1, 1)
        self.dataFrame_Tab.addTab (self.tab, "")
        self.gridLayout.addWidget (self.dataFrame_Tab, 0, 1, 1, 1)
        self.tabWidget_1 = QtWidgets.QTabWidget (self.centralwidget)
        self.tabWidget_1.setMaximumSize (QtCore.QSize (328, 16777215))
        self.tabWidget_1.setObjectName ("tabWidget_1")
        self.Modifying_Tab = QtWidgets.QWidget ()
        self.Modifying_Tab.setObjectName ("Modifying_Tab")

        self.FEntryCombo = QtWidgets.QComboBox (self.Modifying_Tab)
        self.FEntryCombo.setGeometry (QtCore.QRect (30, 40, 81, 21))
        self.FEntryCombo.setObjectName ("FEntryCombo")
        self.FEntryCombo.addItem ("")
        self.FEntryCombo.setItemText (0, "")
        self.FEntryCombo.addItem ("")
        self.FEntryCombo.addItem ("")
        self.FEntryCombo.addItem ("")
        self.FEntryCombo.addItem ("")
        self.FEntryCombo.addItem ("")
        self.FEntry_Input = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FEntry_Input.setGeometry (QtCore.QRect (120, 40, 141, 21))
        self.FEntry_Input.setObjectName ("FEntry_Input")

        self.FLemma_Input = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FLemma_Input.setGeometry (QtCore.QRect (120, 100, 141, 21))
        self.FLemma_Input.setObjectName ("FLemma_Input")
        self.FLemmaCombo = QtWidgets.QComboBox (self.Modifying_Tab)
        self.FLemmaCombo.addItem ("")
        self.FLemmaCombo.setItemText (0, "")
        self.FLemmaCombo.addItem ("a")
        self.FLemmaCombo.addItem ("")
        self.FLemmaCombo.addItem ("")
        self.FLemmaCombo.addItem ("")
        self.FLemmaCombo.addItem ("")
        self.FLemmaCombo.setGeometry (QtCore.QRect (30, 100, 81, 21))
        self.FLemmaCombo.setObjectName ("FLemmaCombo")

        self.FCateCombo = QtWidgets.QComboBox (self.Modifying_Tab)
        self.FCateCombo.setGeometry (QtCore.QRect (30, 160, 81, 21))
        self.FCateCombo.addItem ("")
        self.FCateCombo.setItemText (0, "")
        self.FCateCombo.addItem ("")
        self.FCateCombo.addItem ("")
        self.FCateCombo.addItem ("")
        self.FCateCombo.addItem ("")
        self.FCateCombo.addItem ("")
        self.FCateCombo.setObjectName ("FCateCombo")
        self.FCate_Input = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FCate_Input.setGeometry (QtCore.QRect (120, 160, 141, 21))
        self.FCate_Input.setObjectName ("FCate_Input")

        self.FFirst_1 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FFirst_1.setGeometry (QtCore.QRect (30, 320, 51, 21))
        self.FFirst_1.setObjectName ("FFirst_1")
        self.FFirst_2 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FFirst_2.setGeometry (QtCore.QRect (100, 320, 51, 21))
        self.FFirst_2.setObjectName ("FFirst_2")
        self.FFirst_3 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FFirst_3.setGeometry (QtCore.QRect (170, 320, 51, 21))
        self.FFirst_3.setObjectName ("FFirst_3")
        self.FSec_3 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FSec_3.setGeometry (QtCore.QRect (170, 370, 51, 21))
        self.FSec_3.setObjectName ("FSec_3")
        self.FSec_2 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FSec_2.setGeometry (QtCore.QRect (100, 370, 51, 21))
        self.FSec_2.setObjectName ("FSec_2")
        self.FSec_1 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FSec_1.setGeometry (QtCore.QRect (30, 370, 51, 21))
        self.FSec_1.setObjectName ("FSec_1")
        self.FSecL_3 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FSecL_3.setGeometry (QtCore.QRect (170, 420, 51, 21))
        self.FSecL_3.setObjectName ("FSecL_3")
        self.FSecL_2 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FSecL_2.setGeometry (QtCore.QRect (100, 420, 51, 21))
        self.FSecL_2.setObjectName ("FSecL_2")
        self.FSecL_1 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FSecL_1.setGeometry (QtCore.QRect (30, 420, 51, 21))
        self.FSecL_1.setObjectName ("FSecL_1")
        self.FLast3 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FLast3.setGeometry (QtCore.QRect (170, 470, 51, 21))
        self.FLast3.setObjectName ("FLast3")
        self.FLast_2 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FLast_2.setGeometry (QtCore.QRect (100, 470, 51, 21))
        self.FLast_2.setObjectName ("FLast_2")
        self.FLast_1 = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FLast_1.setGeometry (QtCore.QRect (30, 470, 51, 21))
        self.FLast_1.setObjectName ("FLast_1")
        self.FPhonoFrame = QtWidgets.QFrame (self.Modifying_Tab)
        self.FPhonoFrame.setGeometry (QtCore.QRect (10, 290, 281, 251))
        self.FPhonoFrame.setFrameShape (QtWidgets.QFrame.Box)
        self.FPhonoFrame.setFrameShadow (QtWidgets.QFrame.Raised)
        self.FPhonoFrame.setObjectName ("FPhonoFrame")
        self.FColCombo = QtWidgets.QComboBox (self.FPhonoFrame)
        self.FColCombo.setGeometry (QtCore.QRect (90, 220, 81, 21))
        self.FColCombo.setObjectName ("FColCombo")
        self.label_7 = QtWidgets.QLabel (self.FPhonoFrame)
        self.label_7.setGeometry (QtCore.QRect (20, 50, 211, 31))
        self.label_7.setObjectName ("label_7")
        self.label_8 = QtWidgets.QLabel (self.FPhonoFrame)
        self.label_8.setGeometry (QtCore.QRect (20, 100, 211, 31))
        self.label_8.setObjectName ("label_8")
        self.label_9 = QtWidgets.QLabel (self.FPhonoFrame)
        self.label_9.setGeometry (QtCore.QRect (20, 0, 191, 31))
        self.label_9.setObjectName ("label_9")
        self.label_6 = QtWidgets.QLabel (self.FPhonoFrame)
        self.label_6.setGeometry (QtCore.QRect (20, 150, 211, 31))
        self.label_6.setObjectName ("label_6")
        self.label_10 = QtWidgets.QLabel (self.FPhonoFrame)
        self.label_10.setGeometry (QtCore.QRect (10, 220, 61, 21))
        self.label_10.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName ("label_10")
        self.FFiltering_Button = QtWidgets.QPushButton (self.Modifying_Tab)
        self.FFiltering_Button.setGeometry (QtCore.QRect (20, 550, 75, 23))
        self.FFiltering_Button.setObjectName ("FFiltering_Button")
        self.FShow_Button = QtWidgets.QPushButton (self.Modifying_Tab)
        self.FShow_Button.setGeometry (QtCore.QRect (110, 550, 75, 23))
        self.FShow_Button.setObjectName ("FShow_Button")
        self.FShow_Button.clicked.connect(lambda parameter_list: self.openFiles())
        self.FClear_Button = QtWidgets.QPushButton (self.Modifying_Tab)
        self.FClear_Button.setGeometry (QtCore.QRect (210, 550, 75, 23))
        self.FClear_Button.setObjectName ("FClear_Button")
        self.label = QtWidgets.QLabel (self.Modifying_Tab)
        self.label.setGeometry (QtCore.QRect (30, 10, 56, 21))
        self.label.setObjectName ("label")
        self.label_2 = QtWidgets.QLabel (self.Modifying_Tab)
        self.label_2.setGeometry (QtCore.QRect (30, 70, 56, 21))
        self.label_2.setObjectName ("label_2")
        self.label_3 = QtWidgets.QLabel (self.Modifying_Tab)
        self.label_3.setGeometry (QtCore.QRect (30, 130, 56, 21))
        self.label_3.setObjectName ("label_3")
        self.FInfo_Input = QtWidgets.QLineEdit (self.Modifying_Tab)
        self.FInfo_Input.setGeometry (QtCore.QRect (120, 220, 141, 21))
        self.FInfo_Input.setObjectName ("FInfo_Input")
        self.label_4 = QtWidgets.QLabel (self.Modifying_Tab)
        self.label_4.setGeometry (QtCore.QRect (30, 190, 81, 21))
        self.label_4.setObjectName ("label_4")

        self.FInfoCombo = QtWidgets.QComboBox (self.Modifying_Tab)
        self.FInfoCombo.setGeometry (QtCore.QRect (30, 220, 81, 21))
        self.FInfoCombo.addItem ("")
        self.FInfoCombo.setItemText (0, "")
        self.FInfoCombo.addItem ("")
        self.FInfoCombo.addItem ("")
        self.FInfoCombo.addItem ("")
        self.FInfoCombo.addItem ("")
        self.FInfoCombo.addItem ("")
        self.FInfoCombo.setObjectName ("FInfoCombo")

        self.label_5 = QtWidgets.QLabel (self.Modifying_Tab)
        self.label_5.setGeometry (QtCore.QRect (10, 270, 141, 31))
        font = QtGui.QFont ()
        font.setBold (True)
        font.setWeight (75)
        self.label_5.setFont (font)
        self.label_5.setObjectName ("label_5")
        self.tabWidget_1.addTab(self.Modifying_Tab, "")
        self.Edit_Tab = QtWidgets.QWidget()
        self.Edit_Tab.setObjectName("Edit_Tab")
        self.Push_addrow = QtWidgets.QPushButton(self.Edit_Tab)
        self.Push_addrow.setGeometry(QtCore.QRect(20, 530, 130, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Push_addrow.setFont(font)
        self.Push_addrow.setObjectName("Push_addrow")
        self.Push_Deleterow = QtWidgets.QPushButton(self.Edit_Tab)
        self.Push_Deleterow.setGeometry(QtCore.QRect(170, 530, 140, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Push_Deleterow.setFont(font)
        self.Push_Deleterow.setObjectName("Push_Deleterow")
        self.Push_Duplicaterow = QtWidgets.QPushButton(self.Edit_Tab)
        self.Push_Duplicaterow.setGeometry(QtCore.QRect(20, 580, 290, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Push_Duplicaterow.setFont(font)
        self.Push_Duplicaterow.setObjectName("Push_Duplicaterow")
        self.Edit_function_tab = QtWidgets.QTabWidget(self.Edit_Tab)
        self.Edit_function_tab.setGeometry(QtCore.QRect(0, 50, 321, 371))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Edit_function_tab.setFont(font)
        self.Edit_function_tab.setObjectName("Edit_function_tab")
        self.Add_tab = QtWidgets.QWidget()
        self.Add_tab.setObjectName("Add_tab")
        self.Add_column = QtWidgets.QComboBox(self.Add_tab)
        self.Add_column.setGeometry(QtCore.QRect(150, 80, 128, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Add_column.setFont(font)
        self.Add_column.setEditable(True)
        self.Add_column.setObjectName("Add_column")
        self.Add_column.addItem("")
        self.Add_column.setItemText(0, "")
        self.Add_column.addItem("")
        self.Add_column.addItem("")
        self.Add_position = QtWidgets.QComboBox(self.Add_tab)
        self.Add_position.setGeometry(QtCore.QRect(150, 150, 128, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Add_position.setFont(font)
        self.Add_position.setObjectName("Add_position")
        self.Add_position.addItem("")
        self.Add_position.addItem("")
        self.Add_oldText = QtWidgets.QLineEdit(self.Add_tab)
        self.Add_oldText.setGeometry(QtCore.QRect(150, 220, 128, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Add_oldText.setFont(font)
        self.Add_oldText.setAutoFillBackground(False)
        self.Add_oldText.setObjectName("Add_oldText")
        self.Add_start = QtWidgets.QPushButton(self.Add_tab)
        self.Add_start.setGeometry(QtCore.QRect(180, 290, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Add_start.setFont(font)
        self.Add_start.setObjectName("Add_start")
        self.label_12 = QtWidgets.QLabel(self.Add_tab)
        self.label_12.setGeometry(QtCore.QRect(10, 150, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.label_14 = QtWidgets.QLabel(self.Add_tab)
        self.label_14.setGeometry(QtCore.QRect(0, 10, 321, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.label_13 = QtWidgets.QLabel(self.Add_tab)
        self.label_13.setGeometry(QtCore.QRect(10, 220, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.label_11 = QtWidgets.QLabel(self.Add_tab)
        self.label_11.setGeometry(QtCore.QRect(10, 80, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.Edit_function_tab.addTab(self.Add_tab, "")
        self.Remove_tab = QtWidgets.QWidget()
        self.Remove_tab.setObjectName("Remove_tab")
        self.label_15 = QtWidgets.QLabel(self.Remove_tab)
        self.label_15.setGeometry(QtCore.QRect(10, 150, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.Remove_tab)
        self.label_16.setGeometry(QtCore.QRect(0, 10, 321, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.Remove_tab)
        self.label_17.setGeometry(QtCore.QRect(10, 220, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_17.setFont(font)
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.Remove_tab)
        self.label_18.setGeometry(QtCore.QRect(10, 80, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_18.setFont(font)
        self.label_18.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_18.setObjectName("label_18")
        self.Remove_column = QtWidgets.QComboBox(self.Remove_tab)
        self.Remove_column.setGeometry(QtCore.QRect(150, 80, 128, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Remove_column.setFont(font)
        self.Remove_column.setEditable(True)
        self.Remove_column.setObjectName("Remove_column")
        self.Remove_column.addItem("")
        self.Remove_column.setItemText(0, "")
        self.Remove_column.addItem("")
        self.Remove_column.addItem("")
        self.Remove_position = QtWidgets.QComboBox(self.Remove_tab)
        self.Remove_position.setGeometry(QtCore.QRect(150, 150, 128, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Remove_position.setFont(font)
        self.Remove_position.setObjectName("Remove_position")
        self.Remove_position.addItem("")
        self.Remove_position.addItem("")
        self.Remove_oldText = QtWidgets.QLineEdit(self.Remove_tab)
        self.Remove_oldText.setGeometry(QtCore.QRect(150, 220, 130, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Remove_oldText.setFont(font)
        self.Remove_oldText.setAutoFillBackground(False)
        self.Remove_oldText.setObjectName("Remove_oldText")
        self.Remove_start = QtWidgets.QPushButton(self.Remove_tab)
        self.Remove_start.setGeometry(QtCore.QRect(180, 290, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Remove_start.setFont(font)
        self.Remove_start.setObjectName("Remove_start")
        self.Edit_function_tab.addTab(self.Remove_tab, "")
        self.Replace_tab = QtWidgets.QWidget()
        self.Replace_tab.setObjectName("Replace_tab")
        self.Replace_column = QtWidgets.QComboBox(self.Replace_tab)
        self.Replace_column.setGeometry(QtCore.QRect(150, 70, 130, 30))
        self.Replace_column.setEditable(True)
        self.Replace_column.setObjectName("Replace_column")
        self.Replace_column.addItem("")
        self.Replace_column.setItemText(0, "")
        self.Replace_column.addItem("")
        self.Replace_column.addItem("")
        self.Replace_position = QtWidgets.QComboBox(self.Replace_tab)
        self.Replace_position.setGeometry(QtCore.QRect(150, 127, 130, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Replace_position.setFont(font)
        self.Replace_position.setObjectName("Replace_position")
        self.Replace_position.addItem("")
        self.Replace_position.addItem("")
        self.Replace_position.addItem("")
        self.Replace_position.addItem("")
        self.Replace_oldtext = QtWidgets.QLineEdit(self.Replace_tab)
        self.Replace_oldtext.setGeometry(QtCore.QRect(150, 183, 133, 30))
        self.Replace_oldtext.setObjectName("Replace_oldtext")
        self.Replace_newtext = QtWidgets.QLineEdit(self.Replace_tab)
        self.Replace_newtext.setGeometry(QtCore.QRect(150, 240, 133, 30))
        self.Replace_newtext.setObjectName("Replace_newtext")
        self.Replace_start = QtWidgets.QPushButton(self.Replace_tab)
        self.Replace_start.setGeometry(QtCore.QRect(210, 300, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Replace_start.setFont(font)
        self.Replace_start.setObjectName("Replace_start")
        self.label_19 = QtWidgets.QLabel(self.Replace_tab)
        self.label_19.setGeometry(QtCore.QRect(0, 10, 321, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_19.setFont(font)
        self.label_19.setAlignment(QtCore.Qt.AlignCenter)
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.Replace_tab)
        self.label_20.setGeometry(QtCore.QRect(20, 70, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_20.setFont(font)
        self.label_20.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.Replace_tab)
        self.label_21.setGeometry(QtCore.QRect(20, 127, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_21.setFont(font)
        self.label_21.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_21.setObjectName("label_21")
        self.label_22 = QtWidgets.QLabel(self.Replace_tab)
        self.label_22.setGeometry(QtCore.QRect(20, 183, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_22.setFont(font)
        self.label_22.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.Replace_tab)
        self.label_23.setGeometry(QtCore.QRect(20, 240, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_23.setFont(font)
        self.label_23.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_23.setObjectName("label_23")
        self.Edit_function_tab.addTab(self.Replace_tab, "")
        self.Irreg_tab = QtWidgets.QWidget()
        self.Irreg_tab.setObjectName("Irreg_tab")
        self.Irreg_cons = QtWidgets.QLineEdit(self.Irreg_tab)
        self.Irreg_cons.setGeometry(QtCore.QRect(150, 80, 128, 30))
        self.Irreg_cons.setObjectName("Irreg_cons")
        self.Irreg_oldinflec = QtWidgets.QLineEdit(self.Irreg_tab)
        self.Irreg_oldinflec.setGeometry(QtCore.QRect(150, 150, 128, 30))
        self.Irreg_oldinflec.setObjectName("Irreg_oldinflec")
        self.irreg_newinflec = QtWidgets.QLineEdit(self.Irreg_tab)
        self.irreg_newinflec.setGeometry(QtCore.QRect(150, 220, 128, 30))
        self.irreg_newinflec.setObjectName("irreg_newinflec")
        self.Irreg_start = QtWidgets.QPushButton(self.Irreg_tab)
        self.Irreg_start.setGeometry(QtCore.QRect(180, 290, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.Irreg_start.setFont(font)
        self.Irreg_start.setObjectName("Irreg_start")
        self.label_24 = QtWidgets.QLabel(self.Irreg_tab)
        self.label_24.setGeometry(QtCore.QRect(0, 10, 321, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_24.setFont(font)
        self.label_24.setAlignment(QtCore.Qt.AlignCenter)
        self.label_24.setObjectName("label_24")
        self.label_25 = QtWidgets.QLabel(self.Irreg_tab)
        self.label_25.setGeometry(QtCore.QRect(10, 80, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_25.setFont(font)
        self.label_25.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_25.setObjectName("label_25")
        self.label_26 = QtWidgets.QLabel(self.Irreg_tab)
        self.label_26.setGeometry(QtCore.QRect(10, 150, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_26.setFont(font)
        self.label_26.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_26.setObjectName("label_26")
        self.label_27 = QtWidgets.QLabel(self.Irreg_tab)
        self.label_27.setGeometry(QtCore.QRect(10, 220, 111, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_27.setFont(font)
        self.label_27.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_27.setObjectName("label_27")
        self.Edit_function_tab.addTab(self.Irreg_tab, "")
        self.tabWidget_1.addTab(self.Edit_Tab, "")
        self.gridLayout.addWidget(self.tabWidget_1, 0, 0, 1, 1)
        self.dataFrame_Tab = QtWidgets.QTabWidget(self.centralwidget)
        self.dataFrame_Tab.setObjectName("dataFrame_Tab")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout_2.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.dataFrame_Tab.addTab(self.tab, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.dataFrame_Tab.addTab(self.tab_5, "")
        self.gridLayout.addWidget(self.dataFrame_Tab, 0, 1, 1, 1)
        Deco_LexO.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Deco_LexO)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1015, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuRecent_files = QtWidgets.QMenu(self.menuFile)
        self.menuRecent_files.setObjectName("menuRecent_files")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        Deco_LexO.setMenuBar(self.menubar)
        self.actionOpen_file_s = QtWidgets.QAction(Deco_LexO)
        self.actionOpen_file_s.setShortcutContext(QtCore.Qt.WindowShortcut)
        self.actionOpen_file_s.setObjectName("actionOpen_file_s")
        self.actionNone = QtWidgets.QAction(Deco_LexO)
        self.actionNone.setObjectName("actionNone")
        self.actionSave = QtWidgets.QAction(Deco_LexO)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_file_as = QtWidgets.QAction(Deco_LexO)
        self.actionSave_file_as.setObjectName("actionSave_file_as")
        self.actionQuit = QtWidgets.QAction(Deco_LexO)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAcknowledgement = QtWidgets.QAction(Deco_LexO)
        self.actionAcknowledgement.setObjectName("actionAcknowledgement")
        self.actionAbout_DecoLexO = QtWidgets.QAction(Deco_LexO)
        self.actionAbout_DecoLexO.setObjectName("actionAbout_DecoLexO")
        self.menuRecent_files.addAction(self.actionNone)
        self.menuFile.addAction(self.actionOpen_file_s)
        self.menuFile.addAction(self.menuRecent_files.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_file_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAcknowledgement)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout_DecoLexO)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())


        self.tabWidget_1.addTab (self.Edit_Tab, "")
        self.gridLayout.addWidget (self.tabWidget_1, 0, 0, 1, 1)
        Deco_LexO.setCentralWidget (self.centralwidget)
        self.menubar = QtWidgets.QMenuBar (Deco_LexO)
        self.menubar.setGeometry (QtCore.QRect (0, 0, 709, 21))
        self.menubar.setObjectName ("menubar")
        self.menuFile = QtWidgets.QMenu (self.menubar)
        self.menuFile.setObjectName ("menuFile")
        self.menuRecent_files = QtWidgets.QMenu (self.menuFile)
        self.menuRecent_files.setObjectName ("menuRecent_files")
        self.menuHelp = QtWidgets.QMenu (self.menubar)
        self.menuHelp.setObjectName ("menuHelp")
        Deco_LexO.setMenuBar (self.menubar)
        self.actionOpen_file_s = QtWidgets.QAction (Deco_LexO)
        self.actionOpen_file_s.setShortcutContext (QtCore.Qt.WindowShortcut)
        self.actionOpen_file_s.setObjectName ("actionOpen_file_s")
        self.actionNone = QtWidgets.QAction (Deco_LexO)
        self.actionNone.setObjectName ("actionNone")
        self.actionSave = QtWidgets.QAction (Deco_LexO)
        self.actionSave.setObjectName ("actionSave")
        self.actionSave_file_as = QtWidgets.QAction (Deco_LexO)
        self.actionSave_file_as.setObjectName ("actionSave_file_as")
        self.actionQuit = QtWidgets.QAction (Deco_LexO)
        self.actionQuit.setObjectName ("actionQuit")
        self.actionAcknowledgement = QtWidgets.QAction (Deco_LexO)
        self.actionAcknowledgement.setObjectName ("actionAcknowledgement")
        self.actionAbout_DecoLexO = QtWidgets.QAction (Deco_LexO)
        self.actionAbout_DecoLexO.setObjectName ("actionAbout_DecoLexO")
        self.menuRecent_files.addAction (self.actionNone)
        self.menuFile.addAction (self.actionOpen_file_s)
        self.menuFile.addAction (self.menuRecent_files.menuAction ())
        self.menuFile.addSeparator ()
        self.menuFile.addAction (self.actionSave)
        self.menuFile.addAction (self.actionSave_file_as)
        self.menuFile.addSeparator ()
        self.menuFile.addAction (self.actionQuit)
        self.menuHelp.addAction (self.actionAcknowledgement)
        self.menuHelp.addSeparator ()
        self.menuHelp.addAction (self.actionAbout_DecoLexO)
        self.menubar.addAction (self.menuFile.menuAction ())
        self.menubar.addAction (self.menuHelp.menuAction ())

        self.retranslateUi (Deco_LexO)
        self.dataFrame_Tab.setCurrentIndex (1)
        self.tabWidget_1.setCurrentIndex (0)
        QtCore.QMetaObject.connectSlotsByName (Deco_LexO)

    def retranslateUi(self, Deco_LexO):
        _translate = QtCore.QCoreApplication.translate
        Deco_LexO.setWindowTitle (_translate ("Deco_LexO", "Deco-LexO"))
        self.dataFrame_Tab.setTabText (self.dataFrame_Tab.indexOf (self.tab), _translate ("Deco_LexO", "Tab 1"))
        self.FEntryCombo.setItemText (1, _translate ("Deco_LexO", "Equals"))
        self.FEntryCombo.setItemText (2, _translate ("Deco_LexO", "Starts with"))
        self.FEntryCombo.setItemText (3, _translate ("Deco_LexO", "Ends with"))
        self.FEntryCombo.setItemText (4, _translate ("Deco_LexO", "Contains"))
        self.FEntryCombo.setItemText (5, _translate ("Deco_LexO", "is empty"))

        self.FLemmaCombo.setItemText (1, _translate ("Deco_LexO", "Equals"))
        self.FLemmaCombo.setItemText (2, _translate ("Deco_LexO", "Starts with"))
        self.FLemmaCombo.setItemText (3, _translate ("Deco_LexO", "Ends with"))
        self.FLemmaCombo.setItemText (4, _translate ("Deco_LexO", "Contains"))
        self.FLemmaCombo.setItemText (5, _translate ("Deco_LexO", "is empty"))

        self.FCateCombo.setItemText (1, _translate ("Deco_LexO", "Equals"))
        self.FCateCombo.setItemText (2, _translate ("Deco_LexO", "Starts with"))
        self.FCateCombo.setItemText (3, _translate ("Deco_LexO", "Ends with"))
        self.FCateCombo.setItemText (4, _translate ("Deco_LexO", "Contains"))
        self.FCateCombo.setItemText (5, _translate ("Deco_LexO", "is empty"))

        self.FInfoCombo.setItemText (1, _translate ("Deco_LexO", "Equals"))
        self.FInfoCombo.setItemText (2, _translate ("Deco_LexO", "Starts with"))
        self.FInfoCombo.setItemText (3, _translate ("Deco_LexO", "Ends with"))
        self.FInfoCombo.setItemText (4, _translate ("Deco_LexO", "Contains"))
        self.FInfoCombo.setItemText (5, _translate ("Deco_LexO", "is empty"))

        self.label_7.setText (_translate ("Deco_LexO", "Second syllable:"))
        self.label_8.setText (_translate ("Deco_LexO", "Second-to-last syllable:"))
        self.label_9.setText (_translate ("Deco_LexO", "First syllable:"))
        self.label_6.setText (_translate ("Deco_LexO", "Last syllable:"))
        self.label_10.setText (_translate ("Deco_LexO", "Column:"))
        self.FFiltering_Button.setText (_translate ("Deco_LexO", "Filter"))
        self.FShow_Button.setText (_translate ("Deco_LexO", "Show all"))
        self.FClear_Button.setText (_translate ("Deco_LexO", "Clear"))
        self.label.setText (_translate ("Deco_LexO", "Entry:"))
        self.label_2.setText (_translate ("Deco_LexO", "Lemma:"))
        self.label_3.setText (_translate ("Deco_LexO", "Category:"))
        self.label_4.setText (_translate ("Deco_LexO", "Information:"))
        self.label_5.setText (_translate ("Deco_LexO", "Phonological shape"))
        self.tabWidget_1.setTabText (self.tabWidget_1.indexOf (self.Modifying_Tab), _translate ("Deco_LexO", "Filter"))
        self.Push_addrow.setText(_translate("Deco_LexO", "Add Row"))
        self.Push_Deleterow.setText(_translate("Deco_LexO", "Delete Row"))
        self.Push_Duplicaterow.setText(_translate("Deco_LexO", "Duplicate Row"))
        self.Add_column.setItemText(1, _translate("Deco_LexO", "Lemma"))
        self.Add_column.setItemText(2, _translate("Deco_LexO", "Category"))
        self.Add_position.setItemText(0, _translate("Deco_LexO", "beginning"))
        self.Add_position.setItemText(1, _translate("Deco_LexO", "ending"))
        self.Add_start.setText(_translate("Deco_LexO", "OK"))
        self.label_12.setText(_translate("Deco_LexO", "Position:"))
        self.label_14.setText(_translate("Deco_LexO", "Add Option"))
        self.label_13.setText(_translate("Deco_LexO", "New Text:"))
        self.label_11.setText(_translate("Deco_LexO", "Column Name:"))
        self.Edit_function_tab.setTabText(self.Edit_function_tab.indexOf(self.Add_tab), _translate("Deco_LexO", "Add"))
        self.label_15.setText(_translate("Deco_LexO", "Position:"))
        self.label_16.setText(_translate("Deco_LexO", "Remove Option"))
        self.label_17.setText(_translate("Deco_LexO", "Old Text:"))
        self.label_18.setText(_translate("Deco_LexO", "Column Name:"))
        self.Remove_column.setItemText(1, _translate("Deco_LexO", "Lemma"))
        self.Remove_column.setItemText(2, _translate("Deco_LexO", "Category"))
        self.Remove_position.setItemText(0, _translate("Deco_LexO", "beginning"))
        self.Remove_position.setItemText(1, _translate("Deco_LexO", "ending"))
        self.Remove_start.setText(_translate("Deco_LexO", "OK"))
        self.Edit_function_tab.setTabText(self.Edit_function_tab.indexOf(self.Remove_tab), _translate("Deco_LexO", "Remove"))
        self.Replace_column.setItemText(1, _translate("Deco_LexO", "Lemma"))
        self.Replace_column.setItemText(2, _translate("Deco_LexO", "Column"))
        self.Replace_position.setItemText(0, _translate("Deco_LexO", "anywhere"))
        self.Replace_position.setItemText(1, _translate("Deco_LexO", "whole string"))
        self.Replace_position.setItemText(2, _translate("Deco_LexO", "beginning"))
        self.Replace_position.setItemText(3, _translate("Deco_LexO", "ending"))
        self.Replace_start.setText(_translate("Deco_LexO", "OK"))
        self.label_19.setText(_translate("Deco_LexO", "Replace Option"))
        self.label_20.setText(_translate("Deco_LexO", "Column Name:"))
        self.label_21.setText(_translate("Deco_LexO", "Position:"))
        self.label_22.setText(_translate("Deco_LexO", "Old Text:"))
        self.label_23.setText(_translate("Deco_LexO", "New Text:"))
        self.Edit_function_tab.setTabText(self.Edit_function_tab.indexOf(self.Replace_tab), _translate("Deco_LexO", "Replace"))
        self.Irreg_start.setText(_translate("Deco_LexO", "OK"))
        self.label_24.setText(_translate("Deco_LexO", "Irregular Option"))
        self.label_25.setText(_translate("Deco_LexO", "Final Consonant:"))
        self.label_26.setText(_translate("Deco_LexO", "Old Inflection:"))
        self.label_27.setText(_translate("Deco_LexO", "New Inflection:"))
        self.Edit_function_tab.setTabText(self.Edit_function_tab.indexOf(self.Irreg_tab), _translate("Deco_LexO", "Irregular"))
        self.tabWidget_1.setTabText (self.tabWidget_1.indexOf (self.Edit_Tab), _translate ("Deco_LexO", "Edit"))
        self.menuFile.setTitle (_translate ("Deco_LexO", "File"))
        self.menuRecent_files.setTitle (_translate ("Deco_LexO", "Recent files"))
        self.menuHelp.setTitle (_translate ("Deco_LexO", "Help"))
        self.actionOpen_file_s.setText (_translate ("Deco_LexO", "Open files..."))
        self.actionOpen_file_s.setShortcut (_translate ("Deco_LexO", "Ctrl+O"))
        self.actionNone.setText (_translate ("Deco_LexO", "None"))
        self.actionSave.setText (_translate ("Deco_LexO", "Save file"))
        self.actionSave.setShortcut (_translate ("Deco_LexO", "Ctrl+S"))
        self.actionSave_file_as.setText (_translate ("Deco_LexO", "Save file as..."))
        self.actionSave_file_as.setShortcut (_translate ("Deco_LexO", "Ctrl+Shift+S"))
        self.actionQuit.setText (_translate ("Deco_LexO", "Quit"))
        self.actionQuit.setShortcut (_translate ("Deco_LexO", "Ctrl+Q"))
        self.actionAcknowledgement.setText (_translate ("Deco_LexO", "Acknowledgement"))
        self.actionAbout_DecoLexO.setText (_translate ("Deco_LexO", "About DecoLexO"))
        self.actionOpen_file_s.triggered.connect (self.openFiles)

    def openFiles(self):
        fname = QtWidgets.QFileDialog.getOpenFileName ()
        print(fname)
        self.new_tab = QtWidgets.QWidget ()
        self.new_tab.setObjectName ("new_tab")
        self.gridLayout_2 = QtWidgets.QGridLayout (self.new_tab)
        self.gridLayout_2.setObjectName ("gridLayout_2")
        self.new_tableWidget = QtWidgets.QTableWidget (self.new_tab)
        self.new_tableWidget.setObjectName ("new_tableWidget")
        self.new_tableWidget.setColumnCount (0)
        self.new_tableWidget.setRowCount (0)
        self.gridLayout_2.addWidget (self.new_tableWidget, 0, 1, 1, 1)
        self.dataFrame_Tab.addTab (self.new_tab, "")
        self.dataFrame_Tab.addTab (self.new_tab, str (fname).split ("', '")[0][2:])
        Ofileloc = str (fname).split ("', '")[0][2:]
        #함수를 읽어 주는 함수
        df = pd.read_csv (Ofileloc,encoding='utf-8-sig') 
        readFiles (self.new_tableWidget, df)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication (sys.argv)
    Deco_LexO = QtWidgets.QMainWindow ()
    ui = Ui_Deco_LexO ()
    ui.setupUi (Deco_LexO)
    Deco_LexO.show ()
    sys.exit (app.exec_ ())