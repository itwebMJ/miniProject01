import pymysql
import miniProject.healthClub.MemberModel as mem

class LockerVo:
    def __init__(self, l_id=0, l_pw=None, l_status=None):
        self.l_id = l_id
        self.l_pw = l_pw
        self.l_status = l_status

    def __str__(self):
        return 'l_id:'+str(self.l_id)+' / l_pw:'+str(self.l_pw)+' / l_status:'+str(self.l_status)

class LockerDao:
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='health', charset='utf8')

    def disconnect(self):
        self.conn.close()

    def update(self, l_id, new_l_pw):
        self.connect()
        cur = self.conn.cursor()
        sql = "update locker set l_pw=%s, l_status=%s where l_id=%s"
        vals = (new_l_pw, '이용중', l_id)
        try:
            line = cur.execute(sql, vals)
            self.conn.commit()
            return line
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    def update2(self, l_id):
        self.connect()
        cur = self.conn.cursor()
        sql = "update locker set l_pw=0, l_status='이용가능' where l_id=%s"
        vals = (l_id,)
        try:
            line = cur.execute(sql, vals)
            self.conn.commit()
            return line
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    def selectAll(self):
        lockers = []
        self.connect()
        cur = self.conn.cursor()
        sql = "select l_id,l_status from locker"
        try:
            cur.execute(sql)
            for row in cur:
                lockers.append(LockerVo(row[0], row[1], row[2]))
            return lockers
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    def selectByL_id(self, l_id):
        self.connect()
        cur = self.conn.cursor()
        sql = "select * from locker where l_id=%s"
        vals = (l_id,)
        try:
            cur.execute(sql, vals)
            row = cur.fetchone()
            if row != None:
                return LockerVo(row[0], row[1], row[2])
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

#로그인 기능 추가 -> 메뉴에서 할거라 참조값은 없어도 될것 같은데 혹시 몰라 남겨둡니다
class LockerService:
    login_user_id = None
    login_pwd = None

    def __init__(self):
        self.dao = LockerDao()

    def print_LockerInfo(self):
        print('락커 현황')
        vo = self.dao.selectAll()
        for i in vo:
            print(i)

    def l_select(self):
        print('이용할 락커를 고르시오')
        l_id = int(input('락커 번호 선택: '))
        if l_id > 20 or l_id<0:
            print('사용할 수 없는 번호입니다')
            return
        else:
            if self.dao.selectByL_id(l_id).l_status=='이용가능':
                l_pw = input('비밀번호 입력: ')
                self.dao.update(l_id, l_pw)
            else:
                print('이미 이용중인 자리입니다')
                return

    def edit_LockerInfo(self):
        print('락커 비밀번호 수정')
        l_id = int(input('락커 번호 선택: '))
        if self.dao.selectByL_id(l_id).l_status=='이용중':
            new_l_pw = input('새로운 비밀번호: ')
            self.dao.update(l_id, new_l_pw)
        else:
            print('비어있는 락커입니다')
            return

    def del_LockerInfo(self):
        print('락커이용 해지')
        l_id = int(input('락커 번호 선택: '))
        vo = self.dao.selectByL_id(l_id)
        if vo == None:
            print('비어있는 락커번호 입니다')
        elif vo.l_status == '이용중':
            l_pw = input('비밀번호 입력: ')
            if vo.l_pw == l_pw:
                self.dao.update2(l_id)
                print('락커 해지 완료')
            else:
                print('비밀번호가 일치하지않습니다')
        else:
            print('비어있는 락커입니다')
            return






class Menu:
    def __init__(self):
        self.memService = mem.MemService()
        self.lockerService=LockerService()


    # def run(self):
    #     while True:
    #         m = input('1.회원관리 2.락커 3.종료')
    #         if m=='1':
    #             self.memRun()
    #         elif m=='2':
    #             if mem.MemService.login_mem_userid == None:
    #                 print('로그인 후 사용할 수 있는 서비스')
    #             else:
    #                 self.LockerRun()
    #         elif m=='3':
    #             print('안녕히 가세요')
    #             break
    #
    #
    # def memRun(self):
    #     while True:
    #         m = input('1.회원가입 2.로그인 3.내정보 확인 4.로그아웃 5.로그아웃 6.탈퇴 7.메뉴 나감')
    #         if m=='1':
    #             self.memService.join()
    #         if m=='2':
    #             self.memService.login()
    #         if m=='3':
    #             self.memService.printMemInfo()
    #         if m=='4':
    #             self.memService.editMemInfo()
    #         if m=='5':
    #             self.memService.logout()
    #         if m=='6':
    #             self.memService.delmember()
    #         if m=='7':
    #             print('종료')
    #             break
    #


    def LockerRun(self):
        while True:
            m = input('1.락커현황 2.락커선택 3.락커 비밀번호 수정 4.락커 이용 해지 5.메뉴나감')
            if m=='1':
                self.lockerService.print_LockerInfo()
            if m=='2':
                self.lockerService.l_select()
            if m=='3':
                self.lockerService.edit_LockerInfo()
            if m=='4':
                self.lockerService.del_LockerInfo()
            if m=='5':
                print('메뉴로')
                break


class Master_Menu:
    def __init__(self):
        self.lockerService = LockerService()

    def Master_LockerRun(self):
        while True:
            m = input('1.락커현황 2.메뉴나감')
            if m == '1':
                if mem.MemService.login_user_id == None:
                    print('로그인 후 사용할 수 있는 서비스')
                else:
                    self.lockerService.print_LockerInfo()
            if m=='2':
                print('메뉴로')
                break





# def main():
#     menu = Menu_miniproject1.Menu()
#     menu.run()
#
#
# main()





















