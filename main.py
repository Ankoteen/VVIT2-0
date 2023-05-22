import requests
from flask import Flask, render_template, request, redirect
import psycopg2
app = Flask(__name__)
conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="stalkerdanila13",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()
@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            if password == "" or username == "":
                return render_template("login.html", error="поля нельзя оставлять не заполненными")
            cursor.execute("SELECT * FROM service_users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())
            if records == []:
                return render_template("login.html", error="неправильный login или пароль")
            return render_template('account.html', full_name=records[0][1],password=password,login=username)
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')
@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if password =="" or login == "" or name == "":
            return render_template("registration.html", error="поля нельзя оставлять не заполненными")
        cursor.execute("SELECT * FROM service_users WHERE login=%s ", (str(login),))
        records = list(cursor.fetchall())
        if records != []:
            return render_template("registration.html", error="пользователь с таким логином уже существует")
        cursor.execute('INSERT INTO service_users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
        conn.commit()

        return redirect('/login/')
    return render_template('registration.html')
if __name__=="__main__":
    app.run()