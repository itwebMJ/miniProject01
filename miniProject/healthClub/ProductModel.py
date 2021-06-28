import pymysql


#VO객체 생성
class ProductVo:
    def __init__(self,pd_id=None,pd_name=None,pd_price=None,pd_num=None):
        self.pd_id=pd_id
        self.pd_name=pd_name
        self.pd_price=pd_price
        self.pd_num=pd_num

    def __str__(self):
        return 'product_id: ' +str(self.pd_id) + '\nproduct_name: ' + str(self.pd_name) + '\nproduct_price: ' + str(self.pd_price) + '\nproduct_numer: ' + str(self.pd_num)


#DAO 객체 생성
class ProductDao:
    def __init__(self):
        self.conn = None


    def connect(self):
        self.conn=pymysql.connect(host='localhost', user='root', password='1234', db='health', charset='utf8')

    def disconnect(self):
        self.conn.close()

    def pd_insert(self,vo):
        self.connect()
        cur=self.conn.cursor()
        sql= 'insert into product values(%s,%s,%s,%s)' #%s에는 pd_id,pd_name,pd_price,pd_num이 들어가게 될거임
        vals= (vo.pd_id, vo.pd_name, vo.pd_price, vo.pd_num)
        try:
            cur.execute(sql,vals)
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    def pd_select(self,pd_id): #특정 상품만 선택
        self.connect()
        cur = self.conn.cursor()  # 사용할 커서 객체 생성
        sql = 'select * from product where pd_id=%s'
        vals = (pd_id,)
        try:
            cur.execute(sql, vals)
            row=cur.fetchone()
            if row!=None:
                vo=ProductVo(row[0],row[1],row[2],row[3])
                return vo
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    def pd_select_all(self): #상품 전체 선택
        products=[]
        self.connect()
        cur=self.conn.cursor()
        sql='select * from product'
        try:
            cur.execute(sql)
            for row in cur:
                products.append(ProductVo(row[0],row[1],row[2],row[3]))
            return products
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    def pd_update(self,vo):
        self.connect()
        cur = self.conn.cursor()  # 사용할 커서 객체 생성
        sql = 'update product set pd_name=%s, pd_price=%s, pd_num=%s where pd_id=%s'
        vals = (vo.pd_name,vo.pd_price,vo.pd_num,vo.pd_id)
        try:
            line=cur.execute(sql, vals)
            self.conn.commit()
            return line
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    # def editBoard(self,vo):
    #     self.connect()
    #     cur = self.conn.cursor()
    #     sql = 'update board set title=%s, content=%s where num=%d'
    #     vals = (vo.title, vo.content, vo.num)
    #     try:
    #         line= cur.execute(sql, vals) #execute() 쓰기작업(insert,update, delete)하면 적용된 줄 수를 반환 (숫자)
    #         self.conn.commit()
    #         return line
    #     except Exception as e:
    #         print(e)
    #     finally:
    #         self.disconnet()



    def pd_delete(self,pd_id):
        self.connect()
        cur = self.conn.cursor()  # 사용할 커서 객체 생성
        sql = 'delete from product where pd_id=%s'
        vals = (pd_id,)
        try:
            cur.execute(sql, vals)
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    def pd_buy(self,pd_id,num):
        self.connect()
        cur=self.conn.cursor()
        sql= 'update  product set pd_num =pd_num-%s where pd_id=%s ' #%s에는 pd_id,pd_name,pd_price,pd_num이 들어가게 될거임
        vals= (num,pd_id)
        try:
            cur.execute(sql,vals)
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

class ProductService:
    #앞에서 login_id를 정의했다는 가정하에 진행. -> 로그인한 사람의 id보관, None이면 로그인 안된 상태
    #제품 등록, 수정, 삭제는 관리자 아이디로만 가능

    def __init__(self):
        self.dao=ProductDao()

    def pd_add(self): #관리자가 상품 등록하는 것
        print('상품 등록')
        pd_id= int(input('등록할 상품 번호: '))
        pd_name=input('상품명: ')
        pd_price=int(input('상품 가격: '))
        pd_num=int(input('상품 수량: '))

        try:
            self.dao.pd_insert(ProductVo(pd_id,pd_name,pd_price,pd_num))
        except Exception as e:
            print(e)
        else:
            print('상품 등록 완료')

    # def editBoard(self):
    #     print('글 수정')
    #     num=int(input('수정할 글 번호: '))
    #     vo=self.dao.selectByNum(num)
    #     if vo==None:
    #         print('없는 글번호')
    #     else:
    #         if mem.MemService.login_id == vo.writer:
    #             new_title = input('new title:')
    #             new_content = input('new content: ')
    #             line=self.dao.editBoard(boardVo(num=num, title=new_title,content=new_content))
    #             print(line, '줄이 수정됨')
    #         else:
    #             print('남의 글은 수정할 수 없음')



    def pd_update(self): #관리자가 상품 수정
        print('상품 정보 수정')
        pd_id=int(input('수정하고 싶은 상품의 번호를 입력하세요: '))
        vo=self.dao.pd_select(pd_id)
        if vo==None:
            print('없는 상품번호')
        else:
            new_pd_name= input('새로운 상품 이름: ')
            new_pd_price=int(input('새로운 상품 가격: '))
            new_pd_num=int(input('새로운 상품 수량: '))
            line=self.dao.pd_update(ProductVo(pd_id=pd_id,pd_name=new_pd_name,pd_price=new_pd_price,pd_num=new_pd_num))
            print(line, '줄이 수정됨')


    def pd_delete(self): #관리자가 상품 삭제
        print('상품 삭제')
        pd_id=int(input('삭제할 상품 번호: '))

        try:
            self.dao.pd_delete(pd_id)
        except Exception as e:
            print(e)
        else:
            print('상품 삭제 완료')

    def pd_print_all(self): #관리자,개인 모두 출력
        print('상품 전체 목록 출력')
        products=self.dao.pd_select_all()
        try:
            for p in products:
                print(p)
                print()
        except Exception as e:
            print(e)
        finally:
            print('상품 전체 목록 출력 완료')

    def pd_print_one(self): #상품 아이디로 조회하여 하나만 출력
        print('상품 정보 출력')
        pd_id=int(input('조회할 상품 번호: '))

        try:
            s=self.dao.pd_select(pd_id)
            print(s)
            print()
        except Exception as e:
            print(e)
        finally:
            print('상품 출력 완료')

    def pd_buy(self):
        print('상품 구매')
        self.pd_print_all()
        pd_id=int(input('구매할 상품의 번호: '))
        num=int(input('구매할 상품의 갯수: '))
        try:
            self.dao.pd_buy(pd_id,num)
        except Exception as e:
            print(e)
        finally:
            print('상품 구매 완료')


class MasterProductMenu:
    def __init__(self):
        self.pdService=ProductService()

    def masterMenu(self):
        while True:
            m = int(input('1.상품등록\n2.특정 상품조회\n3.전체 상품조회 \n4.상품수정 \n5.상품삭제 \n6.종료 \n입력: '))

            if m==1:
                self.pdService.pd_add()
            elif m==2:
                self.pdService.pd_print_one()
            elif m==3:
                self.pdService.pd_print_all()
            elif m==4:
                self.pdService.pd_update()
            elif m==5:
                self.pdService.pd_delete()
            else:
                break


class NormalProductMenu:
    def __init__(self):
        self.pdService = ProductService()

    def normalMenu(self):
        while True:
            m = int(input('1.전체 상품조회\n2.특정 상품조회\n3.상품 구매\n4.종료\n입력: '))
            if m==1:
                self.pdService.pd_print_all()
            elif m == 2:
                self.pdService.pd_print_one()
            elif m ==3:
                self.pdService.pd_buy()
            else:
                break


