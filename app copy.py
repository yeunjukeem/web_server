#app.py
from flask import Flask, render_template, request, redirect, session
from data import Articles
from mysql import Mysql
import config
import pymysql
# print(Articles())

app = Flask(__name__)
mysql = Mysql(password=config.PASSWORD)

app.secret_key = "My_Key" #세션을 위해서 추가
# session['is_logged_in'] =False
# session['username'] = ''


@app.route('/', methods=['GET','POST'])
def index():
#     if request.method == "GET":
#         os_info = dict(request.headers)
#         # req_data = request.get_json()
#         print(os_info)
#         name = request.args.get("name")
#         print(name)
#         hello = request.args.get("hello")
#         print(hello)
#         return render_template('index.html', header=f'{name}님, {hello} <3')
#     elif request.method == "POST":
#         data = request.form.get("name")
#         data2 = request.form["hello"]
#         print(data2)
#         return render_template('index.html', header="안녕하세요.")

    return render_template('layouts.html')

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method =="GET":
        return render_template('hello.html')
    elif request.method == "POST":
        name = request.form['name']
        hello = request.form['hello']
        return render_template('index.html', name=name, hello=hello)

@app.route('/list', methods=['GET'])
def list():
    data = Articles()
    return render_template('list.html', data=data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        print(username, email, phone, password)
        
        
        db = pymysql.connect(host=mysql.host, user=mysql.user, db=mysql.db, password=mysql.password, charset=mysql.charset)
        curs = db.cursor()

        sql = f'SELECT * FROM user WHERE email = %s;'
        curs.execute(sql, email)
        
        rows = curs.fetchall()             
        print(rows)
        # 아래 오류방지를 위해서...
        if rows:
            return render_template('register.html', data = 1)
        else:
            result = mysql.insert_user(username, email, phone, password)
            print(result)
            return redirect('/login')
    elif request.method == 'GET':
        return render_template('register.html', data = 0)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method =='GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
    
        db = pymysql.connect(host=mysql.host, user=mysql.user, db=mysql.db, password=mysql.password, charset=mysql.charset)
        curs = db.cursor()

        sql = f'SELECT * FROM user WHERE email = %s;'
        curs.execute(sql, email)
        
        rows = curs.fetchall()             
        print(rows)
        # 아래 오류방지를 위해서...
        if rows:
            result = mysql.verify_password(password, rows[0][4])
            print(result)
            if result:
                session['is_logged_in'] = True
                session['username'] = rows[0][1]
                return redirect('/')
                # return render_template('index.html', is_logged_in = session['is_logged_in'], username=session['username'])
            else:
                return redirect('/login')
            return str(rows[0][4])
        else:
            return render_template('login.html')
        
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)