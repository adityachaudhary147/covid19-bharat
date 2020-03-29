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
import sqlite3

# sys.stdin = open('input.in', 'r')  
# sys.stdout = open('output.out', 'w')
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,Date,desc
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db= SQLAlchemy(app)
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
	URL = 'https://www.mohfw.gov.in/index.html'
	r=requests.get(URL)
	soup=BeautifulSoup(r.content, 'html5lib')
	conn= sqlite3.connect('test.db')
	tbody=soup('tbody')
	# print("Source https://www.mohfw.gov.in/index.html")
	# print("S. No.","State","Numbers")
	list_of_all_tr=tbody[-1]('tr')
	intot=0
	now = datetime.datetime.now()
	# print ("UPDATED AT  date and time : ")
	# print (now.strftime("%Y-%m-%d %H:%M:%S"))
	for w in list_of_all_tr:
		state=w('td')
		if len(state)==5:
			number=0
			conn.execute('''INSERT OR REPLACE INTO CORONACASES(ID,NAMEOFSTATE,INDIANCASES,FOREIGNCASES,RECOVEREDCASES,DEATHCASES) VALUES(?,?,?,?,?,?);''',(int(state[0].contents[0]),str(state[1].contents[0]),int(state[2].contents[0]),0,int(state[3].contents[0]),int(state[4].contents[0])))
			# print("inserted Success")
			for val in state:
				if number==2:
					intot+=int(val.contents[0])
				# print((val.contents[0]),end="     ")
				number+=1
			# print()
		elif len(state)==4:
			state=w('strong')
			listtot=[]
			intc=0
			for val in state:
				# print(val.contents[0],end=" ")
				if intc==1:
					strval=val.contents[0]
					intval=""
					for e in range(len(strval)):
						if e!=len(strval)-1:
							intval+=strval[e]
					intval=int(intval)
					listtot.append(intot)
				elif intc!=0:
					listtot.append(int(val.contents[0]))
				intc+=1
			# print(listtot)
			conn.execute('''INSERT OR REPLACE INTO TOTCORONACASES(ID,INDIANCASES,FOREIGNCASES,RECOVEREDCASES,DEATHCASES) VALUES(?,?,?,?,?);''',(1,listtot[0],0,listtot[1],listtot[2]))		
			# print()
	qwer=listtot[0]
	# print("indian confirmed total  ",intot)
	conn.commit()
	# print("commited")
	conn.close()
	case=CORONACASES.query.all()
	desccase=CORONACASES.query.order_by(desc(CORONACASES.INDIANCASES)).all()
	total=TOTCORONACASES.query.all()
	return render_template("home.html",cases=case,totalcase=total,desccases=desccase,totindia=qwer)

@app.route("/",methods=["POST","GET"])
def home():
	case=CORONACASES.query.all()
	desccase=CORONACASES.query.order_by(desc(CORONACASES.INDIANCASES)).all()
	total=TOTCORONACASES.query.all()
	return render_template("home.html",cases=case,totalcase=total,desccases=desccase)
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