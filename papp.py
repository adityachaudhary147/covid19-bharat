from flask import Flask
from flask import render_template
from flask import request
import datetime
#jai mata di#
import sys
import time
import requests
import datetime
from bs4 import BeautifulSoup
import json

# sys.stdin = open('input.in', 'r')  
# sys.stdout = open('output.out', 'w')
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,Date,desc
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db= SQLAlchemy(app)
def APIUSE():
	URL = 'https://api.covid19india.org/states_daily.json'
	response_json=requests.get(URL)
	response_json=response_json.json()
	states_daily=response_json['states_daily']
	many_keys=states_daily[0].keys()
	total_Active=0
	total_Confirmed=0
	total_Recovered=0
	total_Deceased=0
	new__dict_Confirmed=dict()
	new__dict_Recovered=dict()
	new__dict_Deceased=dict()
	new_active_Cases=dict()
	status_can_be=['Recovered','Confirmed','Deceased']
	otherthan_numer=['status','date','tt']
	for k in many_keys:
		if k not in otherthan_numer:
			new__dict_Deceased[k]=0
			new__dict_Recovered[k]=0
			new__dict_Confirmed[k]=0
			new_active_Cases[k]=0
		else:
			if k=='date':
				new__dict_Confirmed[k]='FINAL'
				new__dict_Deceased[k]='FINAL'
				new__dict_Recovered[k]='FINAL'
				new_active_Cases[k]='PRESENT'

	for day in states_daily:
		if day['status']=='Confirmed':
			for ke in many_keys:
				if ke not in otherthan_numer:
					# print(type(day[ke]),day[ke],ke)
					new__dict_Confirmed[ke]+=int(day[ke])
		if day['status']=='Recovered':
			for ke in many_keys:
				if ke not in otherthan_numer:
					new__dict_Recovered[ke]+=int(day[ke])
		if day['status']=='Deceased':
			for ke in many_keys:
				if ke not in otherthan_numer:
					new__dict_Deceased[ke]+=int(day[ke])
	for k in many_keys:
		if k not in otherthan_numer:
			new_active_Cases[k]=new__dict_Confirmed[k]-new__dict_Recovered[k]-new__dict_Deceased[k]
			total_Deceased+=new__dict_Deceased[k]
			total_Recovered+=new__dict_Recovered[k]
			total_Active+=new_active_Cases[k]
			total_Confirmed+=new__dict_Confirmed[k]
	# print('CORONA VIRUS UPDATES IN INDIA')
	# print("Active Cases",total_Active)
	# print("Confirmed Cases",total_Confirmed)
	# print("Recovered CASES",total_Recovered)
	# print("Deceased Cases",total_Deceased)
	# print("LATEST TREND PREVIOUS DAY")
	# print("Deceased")
	# print(states_daily[-1]['tt'])
	# print("RECOVERED")
	# print(states_daily[-2]['tt'])
	# print("Confirmed")
	# print(states_daily[-3]['tt'])
	current=dict()
	LATEST_Increase=dict()
	total_Active="{:,}".format(total_Active)
	
	current['Active']=total_Active

	current['Confirm']="{:,}".format(total_Confirmed)
	current['Recovered']="{:,}".format(total_Recovered)
	current['Deceased']="{:,}".format(total_Deceased)
	LATEST_Increase['Confirm']="{:,}".format(int(states_daily[-3]['tt']))
	LATEST_Increase['Recovered']="{:,}".format(int(states_daily[-2]['tt']))
	LATEST_Increase['Deceased']="{:,}".format(int(states_daily[-1]['tt']))
	LATEST_Increase['Active']="{:,}".format(int(states_daily[-3]['tt'])-int(states_daily[-2]['tt'])-int(states_daily[-1]['tt']))
	returnobj=[current,LATEST_Increase]
	return returnobj


class CORONACASES(db.Model):
	'''
	table CORONACASES
	'''
	ID=db.Column(db.Integer,primary_key=True,nullable=False)
	NAMEOFSTATE=db.Column(db.Text,nullable=False)
	INDIANCASES=db.Column(db.Integer,nullable=False)
	FOREIGNCASES=db.Column(db.Integer,nullable=False)
	RECOVEREDCASES=db.Column(db.Integer,nullable=False)
	DEATHCASES=db.Column(db.Integer,nullable=False)
class TOTCORONACASES(db.Model):
	'''
	table TOTCORONACASES
	'''
	ID=db.Column(db.Integer,primary_key=True,nullable=False)
	INDIANCASES=db.Column(db.Integer,nullable=False)
	FOREIGNCASES=db.Column(db.Integer,nullable=False)
	RECOVEREDCASES=db.Column(db.Integer,nullable=False)
	DEATHCASES=db.Column(db.Integer,nullable=False)

@app.route("/update",methods=["POST","GET"])
def update():
	abh=APIUSE()
	current=abh[0]
	LATEST_Increase=abh[1]


	return render_template("home.html",Current=current,Latest_increase=LATEST_Increase)

@app.route("/",methods=["POST","GET"])
def home():
	abh=APIUSE()
	current=abh[0]
	LATEST_Increase=abh[1]


	return render_template("home.html",Current=current,Latest_increase=LATEST_Increase)

@app.route("/info",methods=["POST","GET"])
def info():
	return render_template("info.html")
@app.route("/about",methods=["POST","GET"])
def about():
	return render_template("about.html")
@app.route("/contactus",methods=["POST","GET"])
def contactus():
	return render_template("contactus.html")





port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
# if __name__ == "__main__":
#     app.run(debug=True)