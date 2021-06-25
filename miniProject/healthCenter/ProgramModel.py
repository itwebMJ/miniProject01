import pymysql
import datetime as date
import miniProject.healthCenter.member1 as mem

class ProgramVo:
    def __init__(self, pg_id=None, pg_name=None, pg_desc=None, pg_max=None,
                 pg_min=None, pg_st_date=None, pg_en_date=None, member_mem_id=None, pg_teacher_name=None,
                 pg_user_cnt=None):
        self.pg_id = pg_id  # 프로그램 번호
        self.pg_name = pg_name
        self.pg_desc = pg_desc
        self.pg_max = pg_max
        self.pg_min = pg_min
        self.pg_st_date = pg_st_date
        self.pg_en_date = pg_en_date
        self.member_mem_id = member_mem_id  # 강사 번호
        self.pg_teacher_name = pg_teacher_name  # 프로그램의 해당 강사 varchar.
        self.pg_user_cnt = pg_user_cnt  # 현재 수강 중인 인원 int. pg_max 넘지 x

    def __str__(self):
        st_d = str(self.pg_st_date)[0:10]      #2021-01-01  시간 자르고 출력
        en_d = str(self.pg_en_date)[0:10]

        return '번호 : '+str(self.pg_id)+' / 프로그램 명 : ' + self.pg_name + '\n프로그램 내용 : ' + self.pg_desc + \
               '\n강사 : ' + self.pg_teacher_name + ' / 수강중인 인원 : '+ str(self.pg_user_cnt) +\
               '명\n최소 수강인원 ' + str(self.pg_min) + '명, 최대 수강인원 ' + str(self.pg_max) + \
               '명 / 기간 : ' + st_d + ' ~ ' + en_d


class ProgramDao:  # db작업 구현
    def __init__(self):
        self.conn = None

    # db연결 함수
    def connect(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='health', charset='utf8')

    # db닫는 함수
    def disconnect(self):
        self.conn.close()

    def insert(self, vo):  # 프로그램 추가. pg_id 자동 할당
        self.connect()  # db 연결
        cur = self.conn.cursor()  # 사용할 커서 객체 생성
        sql = 'insert into program(pg_name, pg_desc, pg_max, pg_min, pg_st_date, pg_en_date,' \
              ' member_mem_id, pg_teacher_name, pg_user_cnt)' \
              ' values (%s, %s, %s, %s, %s, %s, %s, %s, 0)' #pg_user_cnt null값을 0으로 추가
        vals = (vo.pg_name, vo.pg_desc, int(vo.pg_max), int(vo.pg_min), vo.pg_st_date, vo.pg_en_date,
                int(vo.member_mem_id), vo.pg_teacher_name)
        try:
            result = cur.execute(sql, vals)
            self.conn.commit()
            return result
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    def selectAll(self):  # 프로그램 전체 출력
        prog = []
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from program'
        try:
            cur.execute(sql)
            for row in cur:
                prog.append(ProgramVo(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
            return prog
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    def selectByPg_id(self, pg_id):
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from program where pg_id=%s'
        vals = (pg_id,)
        try:
            cur.execute(sql, vals)
            row = cur.fetchone()
            if row != None:
                vo = ProgramVo(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
                return vo
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    def checkPg_name(self, pg_name):  # 프로그램 이름으로 검색. 중복확인
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from program where pg_name=%s'
        vals = (pg_name,)
        try:
            cur.execute(sql, vals)
            row = cur.fetchone()
            if row != None:
                vo = ProgramVo(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
                return vo
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    def selectByPg_name(self, pg_name):  # 프로그램 이름으로 검색.
        prog = []
        self.connect()
        cur = self.conn.cursor()
        pg_name = '%' + pg_name + '%'
        sql = 'select * from program where pg_name like %s'
        vals = (pg_name,)
        try:
            cur.execute(sql, vals)
            for row in cur:
                prog.append(ProgramVo(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
            return prog
        except Exception as e:
            print(e)
        finally:
            self.disconnect()


    def selectByPg_teacher_name(self, pg_teacher_name):  # 강사 이름으로 검색
        prog = []
        self.connect()
        cur = self.conn.cursor()
        pg_teacher_name = '%' + pg_teacher_name + '%'
        sql = 'select * from program where pg_teacher_name like %s'
        vals = (pg_teacher_name,)
        try:
            cur.execute(sql, vals)
            for row in cur:
                prog.append(ProgramVo(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
            return prog
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    '''
    def select_user_prg(self, mem_id):       #본인이 신청한 프로그램 조회. 회원 조회시, 수강신청, 취소시 사용
        prog = []
        self.connect()
        cur = self.conn.cursor()

        sql = 'select m.mem_id, m.mem_name, m.mem_user_id, m.pg_id, p.pg_name,' \
              ' p.pg_desc, p.pg_max, pg_min, p.member_mem_id, p.pg_teacher_name, p.pg_user_cnt ' \
              ' from member m, program p  where m.mem_id=%s and p.pg_id in (m.pg_id)'
        vals = (mem_id,)       #로그인 번호
        try:
            cur.execute(sql, vals)
            row = cur.fetchone()
            if row != None:
                for i in range(0, 11):
                    prog.append(row[i])
                return prog         #[1, '홍길동', 'honggil', 6, '프로그램10', '프로그램내용', 7, 1, 2, '강사1', 4]
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    '''
    def editAllProByPg_id(self, vo):  # 프로그램 번호를 선택해서 전부 수정
        self.connect()
        cur = self.conn.cursor()
        sql = 'update program set pg_name=%s, pg_desc=%s, pg_max=%s, pg_min=%s, ' \
              'pg_st_date=%s, pg_en_date=%s, member_mem_id=%s, pg_teacher_name=%s where pg_id=%s'
        vals = (vo.pg_name, vo.pg_desc, vo.pg_max, vo.pg_min, vo.pg_st_date, vo.pg_en_date,
                vo.member_mem_id, vo.pg_teacher_name, vo.pg_id)
        try:
            result = cur.execute(sql, vals)
            self.conn.commit()
            return result
        except Exception as e:
            print(e)
        finally:
            self.disconnect()


    # 프로그램 번호를 선택해서 pg_user_cnt 수정
    def edit_user_cnt_byPg_id(self, vo):  # pg_user_cnt  +1 , -1
        self.connect()
        cur = self.conn.cursor()
        sql = 'update program set pg_user_cnt=pg_user_cnt+%s where pg_id=%s'
        vals = (vo.pg_user_cnt, vo.pg_id)
        try:
            result = cur.execute(sql, vals)
            self.conn.commit()
            return result
        except Exception as e:
            print(e)
        finally:
            self.disconnect()


    def delete(self, pg_id):
        self.connect()
        cur = self.conn.cursor()
        sql = 'delete from program where pg_id=%s'
        vals = (pg_id,)  # 튜플
        try:
            result = cur.execute(sql, vals)
            self.conn.commit()
            return result
        except Exception as e:
            print(e)
        finally:
            self.disconnect()


class ProgramService:
    def __init__(self):
        self.programDao = ProgramDao()
        self.memDao = mem.Memdao()

    def addPro(self):  # 관리자가 프로그램 등록
        print('프로그램 등록')
        while True:
            pg_name = input('새 프로그램 명 : ')
            vo = self.programDao.checkPg_name(pg_name)
            if vo != None:
                print('프로그램 이름 중복 불가')
                return
            pg_desc = input('새 프로그램 내용 : ')
            pg_min = int(input('최소 수강 인원 : '))
            pg_max = int(input('최대 수강 인원 : '))
            if pg_min > pg_max:
                print('최소인원 보다 큰 숫자 입력')
                return

            pg_st_date = input('시작일(ex 20210101) : ')   #날짜 문자열
            pg_en_date = input('종료일(ex 20210101) : ')
            if len(pg_st_date) !=8 or len(pg_en_date) != 8:
                print('날짜 입력 오류')
                return
            if int(pg_st_date) > int(pg_en_date):
                    print('종료일이 시작일보다 빠름')
                    return

            login_user_id = mem.MemService.login_user_id    #작성자 : 로그인 번호

            memVo = self.memDao.select(login_user_id)      #본인 정보 가져오는 메서드드            #강사 로그인 아이디로 본인 강사번호, 이름 자동insert
            member_mem_id = memVo.mem_id
            pg_teacher_name = memVo.name

            try:
                result =self.programDao.insert(ProgramVo(pg_name=pg_name, pg_desc=pg_desc, pg_max=pg_max, pg_min=pg_min,
                                          pg_st_date=pg_st_date, pg_en_date=pg_en_date, member_mem_id=member_mem_id,
                                          pg_teacher_name=pg_teacher_name))
                if result == 1:
                    print('프로그램 등록 완료')
                    break

            except Exception as e:
                print(e)

    def getAll(self):
        print('프로그램 목록')
        prog = self.programDao.selectAll()
        for b in prog:
            print(b)

    def printVo(self, vo):  #테이블 1행
        if vo == None :
            print('검색 결과 없음')
        else:
            print(vo)

    def printList(self, vo_list):   #테이블 여러행
        if vo_list == None :
            print('검색 결과 없음')
        else:
            for b in vo_list:
                print(b)

    def getByPg_id(self):  # 프로그램 아이디로 1개 프로그램 가져오기
        print('번호로 검색')
        pg_id = int(input('프로그램 번호 : '))
        vo_list = self.programDao.selectByPg_id(pg_id)
        self.printVo(vo_list)

    def getByPg_name(self):  # 프로그램 이름으로  1개 프로그램 가져오기. 중복 불가 컬럼이므로 1개 검색
        print('프로그램 이름으로 검색')
        pg_name = input('프로그램 이름 : ')
        vo_list = self.programDao.selectByPg_name(pg_name)
        self.printList(vo_list)

    def getByPg_teacher_name(self):  # 강사 이름으로 1개의 프로그램 가져오기
        print('강사 이름으로 검색')
        pg_teacher_name = input('강사이름 이름 : ')
        vo_list = self.programDao.selectByPg_teacher_name(pg_teacher_name)
        self.printList(vo_list)

    def user_apply_program(self):
        print('프로그램 신청')
        self.getAll()  # 전체 출력
        pg_user_cnt = +1

        while True:
            pg_id = int(input('신청할 프로그램 번호(메뉴 나가기:999): '))
            vo_list = self.programDao.selectByPg_id(pg_id)

            login_user_id = mem.MemService.login_user_id  # 작성자 : 로그인 번호

            memVo = self.memDao.select(login_user_id)  # 본인 정보 가져오는 메서드드     #강사 로그인 아이디로 본인 강사번호, 이름 자동insert
            member_mem_id = memVo.mem_id    #로그인 번호

            if pg_id == 999:
                break
            elif vo_list ==None:
                print('신청할 프로그램이 없습니다.')
            else:       #리스트 검색 됐을 경우

                if vo_list.pg_user_cnt == None or vo_list.pg_max > vo_list.pg_user_cnt:
                    try:
                        result = self.programDao.edit_user_cnt_byPg_id(ProgramVo(pg_id=pg_id,
                                            member_mem_id=member_mem_id,pg_user_cnt=pg_user_cnt))
                        # login 아이디 받아서 member 테이블에 pg_id 저장
                        if result > 0:
                            self.memDao.pg_idupdate(login_user_id, pg_id)
                            print('프로그램 신청 완료')
                            break
                    except Exception as e:
                        print(e)
                        break
                else:
                    print('프로그램의 신청이 마감되었습니다.(최대인원 ' + str(vo_list.pg_max) + '명)\n 다른 프로그램을 선택해 주세요.')
                    break


    def user_cancle_program(self):
        print('내가 신청한 프로그램 취소')
        pg_user_cnt = -1
        login_user_id = mem.MemService.login_user_id  # 작성자 : 로그인 번호
        memVo = self.memDao.select(login_user_id)  # 본인 정보 가져오는 메서드

        vo_list = self.programDao.selectByPg_id(memVo.pg_id)    #내가 신청한 프로그램
        self.printVo(vo_list)
        #list = self.programDao.select_user_prg(member_mem_id)

        if vo_list !=None:
            while True:
                pg_id = int(input('취소할 프로그램 번호(메뉴 나가기:999): '))
                if pg_id == 999:
                    break
                else:
                    try:
                        #프로그램 테이블에서 pg_user_cnt -1
                        result = self.programDao.edit_user_cnt_byPg_id(ProgramVo(pg_id=pg_id, pg_user_cnt=pg_user_cnt))
                        # login 아이디 받아서 member의 pg_id null로 업데이트

                        if result > 0:
                            self.memDao.pg_id_set_null_update(login_user_id)
                            print('프로그램 취소 완료')
                            break

                    except Exception as e:
                        print(e)

        else:
            print('신청 취소할 프로그램이 없습니다.')


    def editPro(self):  # 관리자가 프로그램 수정
        print('프로그램 수정')

        while True:
            pg_id = int(input('수정할 프로그램 번호(메뉴 나가기:999): '))

            try:
                vo = self.programDao.selectByPg_id(pg_id)
                if pg_id == 999:
                    break
                elif vo == None:
                    print('없는 프로그램')
                else:
                    pg_name = input('새 프로그램 명 : ')
                    vo = self.programDao.checkPg_name(pg_name)
                    if vo != None:
                        print('프로그램 이름 중복 불가')
                        return
                    pg_desc = input('새 프로그램 내용 : ')
                    pg_min = int(input('최소 수강 인원 : '))
                    pg_max = int(input('최대 수강 인원 : '))
                    if vo.pg_user_cnt > pg_min or vo.pg_user_cnt > pg_max:
                        print('현제 수강중인 인원보다 큰숫자 입력')
                        return
                    if pg_min > pg_max:
                        print('최소인원 보다 큰 숫자 입력')
                        return
                    try:
                        pg_st_date = input('시작일(ex 20210101) : ')  # 날짜 문자열
                        pg_en_date = input('종료일(ex 20210101) : ')
                        if len(pg_st_date) != 8 or len(pg_en_date) != 8:
                            print('날짜 입력 오류')
                            return
                        if int(pg_st_date) > int(pg_en_date):
                            print('종료일이 시작일보다 빠름')
                            return
                    except Exception as e:
                        print(e)

                    login_user_id = mem.MemService.login_user_id  # 작성자 : 로그인 번호
                    memVo = self.memDao.select(login_user_id)  # 본인 정보 가져오는 메서드드     #강사 로그인 아이디로 본인 강사번호, 이름 자동insert
                    member_mem_id = memVo.mem_id
                    pg_teacher_name = memVo.name
                    result = self.programDao.editAllProByPg_id(ProgramVo(pg_id=pg_id, pg_name=pg_name, pg_desc=pg_desc,
                                                    pg_max=pg_max, pg_min=pg_min, pg_st_date=pg_st_date, pg_en_date=pg_en_date,
                                                    member_mem_id=member_mem_id, pg_teacher_name=pg_teacher_name))

                    if result > 0:
                        print('프로그램 수정 완료')
                        break
            except Exception as e:
                print(e)

    def delPro(self):
        print('프로그램 삭제')
        while True:
            pg_id = int(input('삭제할 프로그램 번호(메뉴 나가기:999): '))
            vo = self.programDao.selectByPg_id(pg_id)
            if pg_id == 999:
                break
            elif vo == None:
                print('없는 프로그램')
            elif vo.pg_user_cnt > 0:    # member 테이블의 pg_id 참조중이므로 삭제 불가
                print('회원 수강 중인 프로그램 삭제 불가')
                break
            else:
                try:
                    result = self.programDao.delete(pg_id)
                    if result > 0:
                        print('프로그램 삭제 완료')
                        break
                except Exception as e:
                    print(e)


