import pymysql
import ProgramModel as pg
# import menu


class MemVo:
    def __init__(self, mem_id=None, name=None, user_id=None, pwd=None, phone=None
                 , email=None, pg_id=None, l_id=None):
        self.mem_id = mem_id
        self.name = name
        self.user_id = user_id
        self.pwd = pwd
        self.phone = phone
        self.email = email
        self.pg_id = pg_id
        self.l_id = l_id

    def __str__(self):
        return 'mem_id:' + str(self.mem_id) + ' / name:' + self.name + ' / userid:' + self.user_id + \
               ' / pwd:' + self.pwd + ' / phone:' + self.phone + ' / email:' + self.email + ' \npg' \
               + str(self.pg_id) + '\nlocker:' + str(self.l_id)


class MemVo2:
    def __init__(self, name=None, pg_name=None, l_id=None):
        self.name = name
        self.pg_name = pg_name
        self.l_id = l_id

    def __str__(self):
        return 'name:' + self.name + ' \npg:' + str(self.pg_name)  + ' \nl_id:' + str(self.l_id)


class MemVo3:
    def __init__(self, name=None, pg_id=None, l_id=None):
        self.name = name
        self.pg_id = pg_id
        self.l_id = l_id

    def __str__(self):
        return 'name:' + self.name + ' \npg:' + str(self.pg_id) + '\nlocker:' + str(self.l_id)

class MemVo4:
    def __init__(self, mem_id=None, name=None, user_id=None, pwd=None, phone=None
                 , email=None, pg_name=None, l_id=None):
        self.mem_id = mem_id
        self.name = name
        self.user_id = user_id
        self.pwd = pwd
        self.phone = phone
        self.email = email
        #self.pg_id = pg_id
        self.pg_name = pg_name
        self.l_id = l_id

    def __str__(self):
        if self.pg_name == None:
            self.pg_name = '신청한 프로그램 없음'
        if self.l_id == None:
            self.l_id = '사용중인 락커 없음'
        return 'mem_id:' + str(self.mem_id) + ' / name:' + self.name + ' / userid:' + self.user_id + \
               ' / pwd:' + self.pwd + ' / phone:' + self.phone + ' / email:' + self.email + ' \nprogram name :' \
               + self.pg_name + '\nlocker:' + str(self.l_id)

class pg_id:
    def __init__(self, pg_id = None):
        self.pg_id = pg_id

    def __str__(self):
        return 'pg_id:' + str(self.pg_id)


class Memdao:
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='health', charset='utf8')

    def disconnect(self):
        self.conn.close()

    def mem_insert(self, vo):
        self.connect()
        cur = self.conn.cursor()
        sql = " insert into member(mem_name, mem_user_id, mem_pwd, mem_phone, mem_email) values(%s, %s, %s, %s, %s) "
        vals = (vo.name, vo.user_id, vo.pwd, vo.phone, vo.email)
        cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()

    def pg_idupdate(self, id, pg_id):
        self.connect()
        cur = self.conn.cursor()
        sql = "update member set pg_id = %s  where mem_user_id = %s"
        vals = (pg_id, id)
        cur.execute(sql, vals)
        self.conn.commit()

    def pg_id_set_null_update(self,id):  #수강 취소시 필요한 메서드
        self.connect()
        cur = self.conn.cursor()
        sql = "update member set pg_id =null  where mem_user_id = %s"
        vals = (id,)
        cur.execute(sql, vals)
        self.conn.commit()

    def mem_select(self, id):
        self.connect()
        cur = self.conn.cursor()
        sql = "select * from member where mem_user_id = %s"
        vals = (id,)
        cur.execute(sql, vals)
        row = cur.fetchone()
        self.conn.commit()
        if row != None:
            vo = MemVo(row[0], row[1], row[2], row[3], row[4], row[5], row[7])
            return vo

    def master_select2(self, id):
        self.connect()
        cur = self.conn.cursor()
        sql = "select * from member where mem_user_id = %s"
        vals = (id,)
        cur.execute(sql, vals)
        row = cur.fetchone()
        self.conn.commit()
        if row != None:
            vo = MemVo3(row[1], row[6], row[7])
            return vo

    def mem_editpwd(self, id, new_pwd):
        self.connect()
        cur = self.conn.cursor()
        sql = "update member set mem_pwd = %s  where mem_user_id = %s"
        vals = (new_pwd, id)
        cur.execute(sql, vals)
        self.conn.commit()

    def mem_editphone(self, id, new_phone):
        self.connect()
        cur = self.conn.cursor()
        sql = "update member set mem_phone = %s  where mem_user_id = %s"
        vals = (new_phone, id)
        cur.execute(sql, vals)
        self.conn.commit()

    def mem_editemail(self, id, new_email):
        self.connect()
        cur = self.conn.cursor()
        sql = "update member set mem_email = %s  where mem_user_id = %s"
        vals = (new_email, id)
        cur.execute(sql, vals)
        self.conn.commit()

    def mem_delmem(self, pwd):
        self.connect()
        cur = self.conn.cursor()
        sql = "del from member where pwd = %"
        vals = (pwd,)
        cur.execute(sql, vals)
        self.conn.commit()

    def master_select(self, name):
        self.connect()
        cur = self.conn.cursor()
        sql = "select * from member where mem_name=%s"
        vals = (name,)
        cur.execute(sql, vals)
        row = cur.fetchone()
        self.disconnect()
        if row != None:
            vo = MemVo(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            return vo

    def master_memberselectAll(self):
        members = []
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from member'
        try:
            cur.execute(sql)
            for row in cur:
                members.append(MemVo2(row[1], row[6]))
            return members
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    def select_user_prg_by_mem_id(self, id):       #회원 개인정보 조회, 본인이 신청한 프로그램 조회.
        self.connect()
        cur = self.conn.cursor()
        sql = 'select m.mem_id, m.mem_name, m.mem_user_id, m.mem_pwd, m.mem_phone, m.mem_email, ' \
              'p.pg_name, m.l_id from member m LEFT JOIN ' \
              'program p on m.pg_id = p.pg_id where m.mem_user_id=%s'
        vals = (id,)
        try:
            cur.execute(sql, vals)
            row = cur.fetchone()
            if row != None:
                vo = MemVo4(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                return vo
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    def select_user_prg(self,):       #본인이 신청한 프로그램 조회. 회원 조회시, 수강신청, 취소시 사용
        members = []
        self.connect()
        cur = self.conn.cursor()
        sql = 'select m.mem_name, p.pg_name, m.l_id from member m LEFT JOIN program p on m.pg_id = p.pg_id'

        try:
            cur.execute(sql)
            for row in cur:
                members.append(MemVo2(row[0], row[1], row[2]))
            return members
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

'''
    def LSelect(self):
        lockers = []
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from locker'
        try:
            cur.execute(sql)
            for row in cur:
                lockers.append(MemVo(row[0], row[1], row[2]))
            return lockers
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

'''


class MemService:
    login_user_id = None
    login_pwd = None
    login_name = None

    def __init__(self):
        self.dao = Memdao()
        # self.m = menu

    def mem_join(self):
        print('회원가입')
        name = input('name:')
        user_id = input('user_id:')
        pwd = input('pwd:')
        print('세부사항 입력')
        phone = input('phone:')
        email = input('email:')
        try:
            self.dao.mem_insert(MemVo(name=name, user_id=user_id, pwd=pwd, phone=phone, email=email))
        except Exception as e:
            print(e)
        else:
            print('회원가입완료')

    def mem_login(self):
        print('로그인')
        # if MemService.login_user_id ==None:
        #     print('로그인 먼저 해주세요')

        if MemService.login_user_id != None:
            print('이미 로그인중 입니다')
            return

        user_id = input('id:')
        pwd = input('pwd')
        vo = self.dao.mem_select(user_id)

        if vo == None:
            print('없는 회원아이디')
            return
        else:
            if pwd == vo.pwd:
                print('로그인 성공')
                MemService.login_user_id = user_id
                MemService.login_pwd = pwd

            else:
                print('패스워드 불일치')

    # def master2(self):
    #     print('확인')
    #     user_id = input('id:')
    #     vo = self.dao.select(user_id)
    #     if vo == None:
    #         print('없는 회원아이디')
    #     else:
    #         MemService.login_user_id = user_id

    # def check(self):
    #     print('관리자 확인')
    #     vo = self.dao.select(MemService.login_user_id)
    #     members = self.dao.plotect()
    #     if vo != members:
    #         print('관리자가 아닙니다')
    #         return
    #     else:
    #         print('관리자 가 맞습니다')

    def master_login2(self):
        print('로그인')
        name = input('name:')
        vo = self.dao.master_select(name)
        if vo == None:
            print('없는 회원아이디')
        else:
            login_name=MemService.login_name

    def mem_logout(self):
        print('로그아웃')
        if MemService.login_user_id == None:  # 로그인 상태 확인
            print('로그인 부터 해주십시요')
            return
        MemService.login_user_id = None
        MemService.login_pwd = None

    def master_logout2(self):
        if MemService.login_name == None:  # 로그인 상태 확인
            print('이름부터 적어주십시요')
            return
        MemService.login_name = None
        print('수정완료')

    def master_end(self):
        if MemService.login_name == None:  # 로그인 상태 확인
            print('이름부터 적어주십시요')
            return
        MemService.login_name = None

    def mem_printMemInfo(self):
        print('내정보확인')
        if MemService.login_user_id == None:
            print('일치하지 않습니다')
            return
        else:
            pwd = input('패스워드를 입력해 주십시오:')
            if MemService.login_pwd == pwd:
                print('패스워드가 일치합니다')
                #vo = self.dao.mem_select(MemService.login_user_id)
                vo = self.dao.select_user_prg_by_mem_id(MemService.login_user_id)
                print(vo)
            else:
                print('패스워드가 일치하지 않습니다')
                return

    def mem_editMemInfo(self):
        n = MemService.login_pwd
        pwd = input('비밀번호 입력')
        if pwd == n:
            print('일치합니다')
        else:
            print('비밀번호가 일치하지 않습니다')
            return

        if MemService.login_user_id == None:
            print('아이디 불일치')
            return
        m = input('수정할정보 1.패스워드 2.핸드폰번호 3.새 이메일 4.수정취소')
        if m == '1':
            new_pwd = input('새 pwd:')
            self.dao.mem_editpwd(MemService.login_pwd, new_pwd)
            MemService.login_pwd = new_pwd
            return
        elif m == '2':
            new_phone = input('새 phone:')
            self.dao.mem_editphone(MemService.login_user_id, new_phone)
            return
        elif m == '3':
            new_email = input('새 email:')
            self.dao.mem_editemail(MemService.login_user_id, new_email)
            return
        elif m == '4':
            return

    # 마스터가 일반회원 수정할때 사용하는 함수
    # def master_editMemInfo(self):
    #     m = input('수정할정보 1.패스워드 2.핸드폰번호 3.새 이메일')
    #     if m == '1':
    #         new_pwd = input('새 pwd:')
    #         self.dao.editpwd(MemService.login_pwd, new_pwd)
    #         return
    #     elif m == '2':
    #         new_phone = input('새 phone:')
    #         self.dao.editphone(MemService.login_user_id, new_phone)
    #         return
    #     elif m == '3':
    #         new_email = input('새 email:')
    #         self.dao.editemail(MemService.login_user_id, new_email)
    #         return

    def mem_delmember(self):
        print('계정탈퇴')
        if MemService.login_user_id == None:
            print('아이디 불일치')
            return
        n = MemService.login_pwd
        pwd = input('비밀번호 입력')
        if pwd == n:
            print('일치합니다')
            self.dao.mem_delmem(MemService.login_user_id)
            MemService.login_id = None
            print('탈퇴완료')
        else:
            print('비밀번호가 일치하지 않습니다')
            return


class Master:
    def __init__(self):
        self.conn = None
        self.dao = Memdao()
        self.service = MemService()
        self.programDao = pg.ProgramDao()

    def connect(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='health', charset='utf8')

    def disconnect(self):
        self.conn.close()

    def masterselect(self):
        self.service.master_login2()
        vo = self.dao.master_select(self.service.login_name)
        print(vo)
        if vo == None:
            return
        m = input('1.pwd 변경, 2.phone 변경, 3.email 변경, 4.변경안함')
        if m == '1':
            new_pwd = input('새 pwd:')
            self.dao.mem_editpwd(self.service.login_name, new_pwd)
            self.service.master_logout2()
            return
        elif m == '2':
            new_phone = input('새 phone:')
            self.dao.mem_editphone(self.service.login_name, new_phone)
            self.service.master_logout2()
            return
        elif m == '3':
            new_email = input('새 email:')
            self.dao.mem_editemail(self.service.login_name, new_email)
            self.service.master_logout2()
            return
        elif m == '4':
            print('수정안함')
            self.service.master_end()
            return

    def master_MemAll(self):
        print('등록된사람')
        #members = self.dao.master_memberselectAll()
        members = self.dao.select_user_prg1()
        for m in members:
            print(m, '\n-----------')

    # 이름으로 검색결과 받아서 수정
    # def master2(self):
    #     print('확인')
    #     user_id = input('id:')
    #     vo = self.dao.select(user_id)
    #     if vo == None:
    #         print('없는 회원아이디')
    #     else:
    #         MemService.login_user_id = user_id

    # def check(self):
    #     print('관리자 확인')
    #     vo = self.dao.select(MemService.login_user_id)
    #     members = self.dao.plotect()
    #     if vo != members:
    #         print('관리자가 아닙니다')
    #         return
    #     else:
    #         print('관리자 가 맞습니다')




