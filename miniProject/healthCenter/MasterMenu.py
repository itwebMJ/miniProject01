import ProgramModel as pro

class MasterMenu:
    def __init__(self):
        self.proService = pro.ProgramService()

    def teacher_prog_menu(self):

        while True:
            p = input('1.프로그램 목록 2.프로그램 추가 3. 프로그램 수정 4.삭제 5.종료')
            if p == '1':
                self.proService.getAll()
            elif p == '2':
                self.proService.addPro()
            elif p == '3':
                self.proService.editPro()
            elif p == '4':
                self.proService.delPro()
            elif p == '5':
                break

    def prog_search_menu(self):  # 프로그램 검색 방법 메뉴
        p = input('검색할 방법 1.번호 2.프로그램 이름 3. 강사이름 4.종료')
        if p == '1':
            self.proService.getByPg_id()
        elif p == '2':
            self.proService.getByPg_name()
        elif p == '3':
            self.proService.getByPg_teacher_name()
        elif p == '4':
            return
def main():
    m = MasterMenu()
    m.teacher_prog_menu()
#main()