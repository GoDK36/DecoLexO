##########################################
##########################################
##########################################


        ##connenct code##
        self.Add_start.released.connect(self.add_function)
        self.Remove_start.released.connect(self.remove_function)
        self.Replace_start.released.connect(self.replace_function)
        self.Irreg_start.released.connect(self.irregular_function)
        self.Push_addrow.released.connect(self.add_row_function)
        self.Push_Deleterow.released.connect(self.delete_row_function)
        self.Push_Duplicaterow.released.connect(self.duplicate_row_function)



    ######################
    ##Edit Function 함수##
    ######################


    #Add function에서 ok를 누르면 실행될 함수

    def add_function(self):
        global handle_df

        ##입력값 텍스트화
        add_col_txt = str(self.Add_column.currentText())  ##combobox는 currentText()사용
        add_pos_txt = str(self.Add_position.currentText())
        add_new_txt = str(self.Add_oldText.text())
        handle_df = add(handle_df, add_col_txt, add_pos_txt, add_new_txt) ##새로운 변수에 저장하기
        #     handle_df (작업창에 떠있는 데이터프레임),

        self.readFiles2 (handle_df) ##readfiles함수에 넣으면 나타남.    

    #Remove Function에서 ok를 누르면 실행될 함수

    def remove_function(self):
        global handle_df

        ##입력값 텍스트화
        rem_col_txt = str(self.Remove_column.currentText())
        rem_pos_txt = str(self.Remove_position.currentText())
        rem_old_txt = str(self.Remove_oldText.text())
        
        handle_df = rmv(handle_df, rem_col_txt, rem_pos_txt, rem_old_txt)

        self.readFiles2 (handle_df)

    #Replace Function에서 ok를 누르면 실행될 함수
    
    def replace_function(self):
        global handle_df

        ##입력값 텍스트화
        rep_col_txt = str(self.Replace_column.currentText())
        rep_pos_txt = str(self.Replace_position.currentText())
        rep_old_txt = str(self.Replace_oldtext.text())
        rep_new_txt = str(self.Replace_newtext.text())
        
        if rep_pos_txt == 'anywhere':
            handle_df = anywhere_rpl(handle_df, rep_col_txt, rep_old_txt, rep_new_txt)
        if rep_pos_txt == 'whole string':
            handle_df = whole_rpl(handle_df, rep_col_txt, rep_old_txt, rep_new_txt)
        if rep_pos_txt == 'beginning':
            handle_df = begin_rpl(handle_df, rep_col_txt, rep_old_txt, rep_new_txt)
        if rep_pos_txt == 'ending':
            handle_df = end_rpl(handle_df, rep_col_txt, rep_old_txt, rep_new_txt)

        self.readFiles2(handle_df)

    #Replace Function에서 ok를 누르면 실행될 함수

    def irregular_function(self):
        global handle_df

        fin_con_txt = str(self.Irreg_cons.text())
        old_inf_txt = str(self.Irreg_oldinflec.text())
        new_inf_txt = str(self.irreg_newinflec.text())

        handle_df = irreg(handle_df, fin_con_txt, old_inf_txt, new_inf_txt)

        self.readFiles2(handle_df)

    ##Add row 버튼을 누르면 실행될 함수

    def add_row_function(self):
        global handle_df

        handle_df = addrow(handle_df)

        self.readFiles2(handle_df)

    ##Delete row 버튼을 누르면 실행될 함수

    def delete_row_function(self):
        global handle_df

        handle_df = delrow(handle_df)
        
        self.readFiles2(handle_df)

        
    ##Duplicate row 버튼을 누르면 실행될 함수
    def duplicate_row_function(self):
        global handle_df

        cell_idx = self.new_tableWidget.selectedIndexes() ##선택한 행의 인덱스 정보 반환하는 함수

        sel_cells = list(set(( idx.row() for idx in cell_idx))) ##인덱스 정보 중 row의 인덱스 값(정수)로 변환
        # sel_cell = self.new_tableWidget.currentRow()  선택한 단일의 행의 인덱스 값(정수)반환하는 함수 

        for i in sel_cells:
            handle_df = duprow(handle_df, i)

        self.readFiles2(handle_df)
