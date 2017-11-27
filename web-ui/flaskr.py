import os, datetime, json
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
        render_template, flash, Response
from pytz import timezone
from prediction import prediction
from prediction import prediction_nozip
from plotter import get_plot
import random
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    flag = False
    ans = []
    if 'weekday' in request.form and 'hour' in request.form and 'rain' in request.form and 'temp' in request.form and 'zipcode' in request.form:
        if (request.form['weekday']!='') and (request.form['hour']!='') and (request.form['rain']!='') and (request.form['temp']!='') and (request.form['zipcode']!=''):
            weekday = int(request.form['weekday'])
            hour = int(request.form['hour'])
            rain = float(request.form['rain'])
            temp = float(request.form['temp'])
            zipcode = int(request.form['zipcode'])
            df = prediction(weekday,hour,temp,rain,zipcode)
            ans_zip = df[0]
            ans_count = df[1]
            ans.append([ans_zip,ans_count])
            flag = True
            get_plot(hour)
        else:
            if (request.form['weekday']!='') and (request.form['hour']!=''):
                flag = True
                weekday = int(request.form['weekday'])
                hour = int(request.form['hour'])
                df = prediction_nozip(weekday, hour)
                get_plot(hour) 
                ans_zip = df['zipcode'].tolist()
                ans_count = df['count'].tolist()
                for i in range(0,len(ans_zip)):
                    ans.append([ans_zip[i].decode("utf-8").split('.')[0] ,ans_count[i]])
    img = ''
    if (flag) :
        img = 'static/thismap.html'+'?rand=' + str(round(random.random() * 10000000))

    return render_template("result.html", result = flag, result_list = ans, image=img)

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 10086 , debug = True)
