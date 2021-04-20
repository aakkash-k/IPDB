from flask import Flask, request, redirect, render_template
from flask_mysqldb import MySQL
import yaml
app = Flask(__name__)
db = yaml.load(open("db.yaml"))
app.config["MYSQL_HOST"]=db["mysql_host"]
app.config["MYSQL_USER"]=db["mysql_user"]
app.config["MYSQL_PASSWORD"]=db["mysql_password"]
app.config["MYSQL_DB"]=db["mysql_db"]
mysql = MySQL(app)
@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userDetail = request.form
        name = userDetail['uname']
        password=userDetail['password']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users(name, password) VALUES(%s, %s)", (name, password))
        cursor.connection.commit()
        cursor.close()
        return redirect("/home")
    return render_template("index.html")
@app.route("/home", methods=['GET', 'POST'])
def home():
    
    return render_template("home.html")
@app.route("/registration", methods=['GET','POST'])
def regi():
    return render_template("registartion.html")
@app.route("/politician", methods=['GET','POST'])
def politician():
    if request.method == 'POST':
        details = request.form
        uname1 = details['uname1']
        uname2 = details['uname2']
        password1 = details['password1']
        password2 = details['password2']
        if uname1==uname2 and password1==password2 and uname1!="" and password1!="" and uname2!="" and password2!="":
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO politician(name, password) VALUES(%s, %s)",(uname1, password1))
            cur.connection.commit()
            cur.close()
            return redirect("/home")
        else:
            return "<h1>given wrong username  and password</h1>"
@app.route('/partyRegistration', methods=['POST', 'GET'])
def partyRegistration():
    if request.method =='POST':
        details = request.form
        party1 = details['party1']
        party2 = details['party2']
        password1 = details['password1']
        password2 = details['password2']
        if party1==party2 and password1==password2 and party1!="" and password1!="" and party2!="" and password2!="":
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO party(party, password) VALUES(%s, %s)", (party1, password1))
            cur.connection.commit()
            cur.close()
            return redirect('/home')
        else:
            return "<h1>given wrong username  and password</h1>"
    return render_template("party_registration.html")
@app.route("/result")
def result():
    return render_template("result.html")
@app.route("/viewPolitician",methods=['GET', 'POST'])
def viewPolitician():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        result = cur.execute("select * from politician")
        if result >0:
            politicians = cur.fetchall()
            return render_template("result.html", politicians = politicians)
@app.route("/viewParty",methods=['GET', 'POST'])
def viewParty():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        result = cur.execute("select * from party")
        if result >0:
            partys = cur.fetchall()
            return render_template("party.html", partys = partys)  

if __name__=="__main__":
    app.run(debug=True)