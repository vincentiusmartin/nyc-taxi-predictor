import os, datetime, json
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
        render_template, flash, Response
from pytz import timezone
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    s = ''
    s1 = ''
    s2 = ''
    s3 = ''
    if 'time' in request.form and 'location' in request.form:
        s = request.form['time'] + request.form['location']
        s2 = s + 'ss'
        s3 = s + '??' 
    img = ''
    if s != 0:
        img = '/static/google.png'

    return render_template("result.html", result=s, result2=s1, result3=s2, image=img)

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 10086 , debug = True)
