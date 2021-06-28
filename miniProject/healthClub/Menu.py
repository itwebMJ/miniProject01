import pymysql
import miniProject.healthClub.MemberModel as m
import miniProject.healthClub.ToolModel as t
import miniProject.healthClub.LockerModel as l
import miniProject.healthClub.ProgramModel as pg
import miniProject.healthClub.ProductModel as pd



class Final_Menu:
    def __init__(self):
        self.memService = m.MemService()
        self.memMasterMenu =m.Master()

        self.pdService=pd.ProductService()
        self.pgService=pg.ProgramService()

        self.toolService=t.toolService()
        self.toolmenu=t.menu()

        self.lockService = l.LockerService()
        self.lockMasterMenu=l.Master_Menu()
        self.lockNormalMenu=l.Menu()

        self.programMasterMenu=pg.MasterMenu()
        self.programNormalMenu=pg.UserMenu()


        self.productMasterMenu=pd.MasterProductMenu()
        self.productNormalMenu=pd.NormalProductMenu()



    def run(self):
        while True:
            m=int(input('1.로그인\n2.회원가입\n3.종료\n번호 입력: '))
            if m==1:
                self.memService.mem_login()
                self.login_menu()

            elif m==2:
                self.memService.mem_join()
            else:
                break
    def login_menu(self):
        if (self.memService.login_user_id != None) and ('master' in self.memService.login_user_id):  # 관리자 아이디로 로그인시
            print('관리자 아이디로 로그인하셨습니다')
            while True:
                m1 = int(input('1.회원\n2.락커\n3.기구\n4.프로그램\n5.상품\n6.종료\n입력: '))
                if m1 == 1:
                    m2 = int(input('1.회원정보 전체출력\n2.개인회원 조회\n3.종료\n입력: '))
                    if m2 == 1:
                        self.memMasterMenu.master_MemAll()  # 전체회원 정보 출력하는 함수
                    elif m2 == 2:
                        self.memMasterMenu.masterselect()  # 개인회원 정보 출력하는 함수 호출
                        m3 = int(input('1.수정\n2.삭제\n3.종료\n4.입력: '))
                    elif m2 == 3:
                        return
                elif m1 == 2:
                    self.lockMasterMenu.Master_LockerRun()
                elif m1 == 3:
                    self.toolmenu.Menu()
                elif m1 == 4:
                    self.programMasterMenu.teacher_prog_menu()
                elif m1 == 5:
                    self.productMasterMenu.masterMenu()
                else:
                    return

        elif (self.memService.login_user_id != None) and ('master' not in self.memService.login_user_id):
            while True:
                n1 = int(input('1.회원\n2.락커\n3.기구\n4.프로그램\n5.상품\n6.종료\n입력: '))  # 일반 회원이 보는 화면의 메뉴 실행
                if n1 == 1:
                    n2 = int(input('1.내정보확인\n2.내정보수정'))
                    if n2 == 1:
                        self.memService.mem_printMemInfo()
                    elif n2 == 2:
                        self.memService.mem_editMemInfo()
                    else:
                        return
                elif n1 == 2:
                    self.lockNormalMenu.LockerRun()
                elif n1 == 3:
                    self.toolService.getAll()
                elif n1 == 4:
                    self.programNormalMenu.user_prog_menu()
                elif n1 == 5:
                    self.productNormalMenu.normalMenu()
                else:
                    return


def main():
    menu=Final_Menu()
    menu.run()

main()










