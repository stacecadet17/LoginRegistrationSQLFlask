# not finished!
# still need to validate login information





from flask import Flask, render_template, redirect, request, flash, session
from mysqlconnection import MySQLConnector
import re
import os, binascii
import md5
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
app.secret_key = "poptarts"
mysql = MySQLConnector(app, 'newpeeps')
salt = binascii.b2a_hex(os.urandom(15))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def register():
#Registration Validation
    if request.form['validation'] == 'register':
        session['first_name'] = False
        session['last_name'] = False
        session['email'] = False
        session['pw'] = False
        session['pw_confirm'] = False

        query = 'SELECT * FROM users;'
        trueSTORY = mysql.query_db(query)

        if trueSTORY:
            session['first_name'] = True
            session['last_name'] = True
            session['email'] = True
            session['pw'] = True
            session['pw_confirm'] = True


    #email check
    if len(request.form['email']) < 1:
        flash("email cannot be empty!")
    elif not EMAIL_REGEX.match(request.form['email']):
        flash('invalid input!')
        return redirect('/')
    else:
        query = 'SELECT * FROM users WHERE email = :email'
        data = {
            "email": request.form['email'],
        }
        array = mysql.query_db(query, data)
        if len(array) < 1:
            query = 'INSERT INTO users(email) VALUES(:email);'

            data = {
                "email": request.form['email'],
            }
            mysql.query_db(query, data)
            return redirect('/success')
        else:
            flash('This email is already taken!')
            return redirect('/')

    #name check
    if len(request.form['first_name']) < 2:
        flash('Name is too short!')
    elif len(request.form['last_name']) < 2:
        flash('Name is too short!')
    else:
        return render_template('success.html')







    #password check
    if len(request.form['pw']) < 8:
        flash('password is too short!')
    elif request.form['pw'] != request.form['pw_confirm']:
        flash('passwords must match!')
    else:
        password = request.form['pw']
        hashed = md5.new(request.form(password + salt)).hexidigest()
        session['pw'] = True
        return render_template('success.html')

#Login Validation
    if request.form['validation'] == 'login':
        session['email'] = False
        session['logged_in'] = False
        session['pw'] = False

        query = 'SELECT email FROM users WHERE email = :email;'
        trueDAT = mysql.query_db(query)
        if(trueDAT):
            session['email'] = True
        else:
            flash('Email does not match')


@app.route('/success')
def success():
   query = "SELECT * FROM users;"
   all_users = mysql.query_db(query)
   return render_template('success.html', users =  all_users )
#
app.run(debug=True)
