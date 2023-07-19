#mysql.py

import pymysql
# 암호화 알고리즘. 256을 제일 많이 사용한다.

from passlib.hash import pbkdf2_sha256 


# 원문 비밀번호를, 암호화 하는 함수

def hash_password(original_password):
    salt = '1234'
    password = original_password + salt
    password = pbkdf2_sha256.hash(password)
    return password
def check_password(input_password, hashed_password):
    salt='eungok'
    password = input_password + salt
    result = pbkdf2_sha256.verify(password, hashed_password)
    return result

class Mysql:
    def __init__(self, host='localhost', user='root', db='os', password='', charset='utf8'):
        self.host = host
        self.user = user
        self.db = db
        self.password = password
        self.charset = charset

    def get_user(self):
       
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()
        
        sql = "select * from user";
        curs.execute(sql)
        
        rows = curs.fetchall()             
        db.commit()
        db.close()
        return rows

    def insert_user(self, username, email, phone, password):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()
        
        sql = '''insert into user (username, email, phone, password) values(%s,%s,%s,%s)'''
        hashed_password = hash_password(password)
        result = curs.execute(sql,(username, email, phone, hashed_password)) #sql로 보내는 것
        print(result)
        db.commit()
        db.close()
        return result

    def verify_password(self, password, email):    
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()

        sql = f'SELECT * FROM user WHERE email = %s;'
        curs.execute(sql, email)
        
        rows = curs.fetchall()             
        print(rows)
        # db.commit()
        db.close()

        if len(rows) != 0:
            hashed_password = rows[0][4]
            result = check_password(password, hashed_password)
            if result:
                print("SUCCESS")
            else:
                print("MissMatch Password!")
        else:
            print("User is not exist")

    def del_user(self, email):
        db = pymysql.connect(host=self.host, user=self.user, db=self.db, password=self.password, charset=self.charset)
        curs = db.cursor()
        
        sql =f"delete from user where email= %s;"
        curs.execute(sql,email)
        db.commit()
        db.close()

mysql = Mysql(password='java')
# rows = mysql.get_user()
# print(rows)

# mysql.insert_user("garykim", "1@naver.com", "010-8496-9889", "1234")

# mysql.del_user("1@naver.com")
# password = hash_pass

# result = check_password("2234","$pbkdf2-sha256$29000$Paf0PickxHiv1bp3jhEiRA$zZskLaHOk5pvGdwyeAYKEx4oNyzmrw3UHPDuwprUZhY")
# print(result)

# mysql.verify_password("1234","2@naver.com")

mysql.verify_password("1234", "1@naver.com" )
    