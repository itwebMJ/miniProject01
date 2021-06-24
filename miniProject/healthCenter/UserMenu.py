import ProgramModel as pro
#import member.MemModel as mem
class MasterMenu:
    def __init__(self):
        self.progService = pro.ProgramService()

    def user_prog_menu(self):

        while True:
            p = input('1.프로그램 목록 2. 프로그램 검색 3. 프로그램 신청 4. 프로그램 신청 취소 5.종료')
            if p == '1':
                self.proService.getAll()
            elif p == '2':
                self.prog_search_menu()  # 프로그램 검색 방법 메뉴
            elif p == '3':
                self.proService.user_apply_program()
            elif p == '4':
                self.proService.user_cancle_program()

            elif p == '5':
                break
