from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import sys
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key="hello"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'sample1'
mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == "POST":
        details = request.form
        username = details['id']
        password = details['pass']
        app.logger.info(password)
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from Usertable WHERE username = (%s) and pass = (%s)", (username,password))
        result=cur.fetchall()
        cur.close()
        if (len(result) == 1):
            session['username'] = username
            return redirect('/home')
        else:
            return render_template('index.html',relogin = "Password or Username is incorrect !")
    return render_template('index.html',relogin = "1")

@app.route('/home', methods=['GET', 'POST'])
def chat():
    if 'username' in session:
        username = session['username']
        if request.method == "POST":

            details = request.form
            message = details['message']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO temp VALUES((%s),DEFAULT,(%s))",(message,username))
            mysql.connection.commit()
            cur.close()

            return redirect('/home')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from temp ")
        result=cur.fetchall()
        cur.close()
        return render_template('chat.html',result=result)
    else:
        return redirect('/')
if __name__ == '__main__':
    app.run()