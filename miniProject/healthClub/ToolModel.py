import pymysql

class toolVo:
    def __init__(self, t_id=None, t_name=None, t_num=None, t_date=None):
        self.t_id=t_id
        self.t_name=t_name
        self.t_num=t_num
        self.t_date=t_date

    def __str__(self):
        return 'id:' + str(self.t_id) + ' / 기구 이름 :' + str(self.t_name) + ' / 대수 :' + str(self.t_num) + ' / 입관 날짜 :' +str(self.t_date)

class toolDao:
    def __init__(self):
        self.conn=None

    def connect(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='health', charset='utf8')

    def disconnect(self):
        self.conn.close()

    def insert(self,vo):   #기구 등록
        self.connect()
        cur = self.conn.cursor()
        sql="insert into tool(t_name, t_num, t_date) values(%s, %s, date(now()))"
        vals = (vo.t_name, vo.t_num)
        try:
            cur.execute(sql, vals)
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    def selectAll(self):    #기구 전체 출력
        boards=[]
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from tool'
        try:
            cur.execute(sql)
            for row in cur:
                boards.append(toolVo(row[0], row[1], row[2], row[3]))
            return boards
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    def update(self, t_id, t_num):    #기구 수정
        self.connect()
        cur = self.conn.cursor()
        sql = 'update tool set t_num=%s where t_id=%s'
        vals = (t_num, t_id)
        line = cur.execute(sql, vals)
        self.conn.commit()
        self.disconnect()
        return line

    def delete(self, t_id):   #기구 삭제
        self.connect()
        cur = self.conn.cursor()
        sql = 'delete from tool where t_id=%s'
        vals = (t_id,)
        line = cur.execute(sql, vals)  #처리된 줄 수를 반환.
        self.conn.commit()
        self.disconnect()
        return line

class toolService:

    def __init__(self):
        self.dao = toolDao()

    def addtool(self):      #기구 추가 화면
        print('기구 추가')
        t_name = input('기구 이름 :')
        t_num = input('기구 갯수 :')
        self.dao.insert(toolVo(t_name=t_name, t_num=t_num))

    def getAll(self):       #기구 조회 화면
        print('기구 목록')
        boards = self.dao.selectAll()
        for b in boards:
            print(b)

    def edittool(self):     #기구 수정 화면
        print('기구 수정')
        num = int(input('수정할 기구 번호 :'))
        cnt = int(input('수정할 수량 :'))
        line = self.dao.update(num,cnt)
        if line == 0:
            print('없는 기구입니다.')
        else :
            print('수정되었습니다.')


    def deltool(self):      #기구 삭제 화면
        print('기기 삭제')
        name = int(input('삭제할 기구 번호 :'))
        line = self.dao.delete(name)
        if line == 0:
            print('없는 기구입니다.')
        else :
            print('삭제되었습니다.')


class menu():
    def __init__(self):
        self.service=toolService()   # 변수=데이터 타입(c에서 구조체와 비슷한 부분.), 객체 중심 언어의 특징. 이것을 안 쓴다는 것=""

    def Menu(self):
        while True:
            num=input('1.기구 추가 2.기구 목록 출력 3.기구 정보 수정 4.기구 삭제 5.종료 \n입력: ')

            if num=='1':
                self.service.addtool()
            elif num=='2':
                self.service.getAll()
            elif num == '3':
                self.service.edittool()
            elif num == '4':
                self.service.deltool()
            else:
                break

# def main():
#     m=menu()
#     m.Menu()
#
# main()