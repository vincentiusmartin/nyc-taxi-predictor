import os, datetime, json
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
        render_template, flash, Response
from pytz import timezone
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    s = []
    s1 = ''
    s2 = ''
    s3 = ''
    if 'weekday' in request.form and 'hour' in request.form and 'temp' in request.form and 'zipcode' in request.form:
        s1 = request.form['weekday'] + request.form['hour']+ request.form['temp']+ request.form['zipcode']
        s2 = s1 + 'ss'
        s3 = s1 + '??' 
        s.append(s1)
        s.append(s2)
        s.append(s3)
    else:
        if 'weekday' in request.form and 'hour' in request.form and 'temp' in request.form:
            s1 = request.form['weekday'] + request.form['hour']+ request.form['temp']
            s2 = s1 + 'ss'
            s3 = s1 + '??' 
            s.append(s1)
            s.append(s2)
            s.append(s3)
    img = ''
    if s != []:
        img = '/static/google.png'

    return render_template("result.html", result=s1, result2=s2, result3=s3, result_list = s, image=img)

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 10086 , debug = True)
