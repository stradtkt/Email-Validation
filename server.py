from flask import Flask, request, redirect, render_template, session, flash, url_for
from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)
mysql = MySQLConnector(app, 'email')
app.secret_key = 'dfkndf.cdfsd.sd.dsv.sdv.sd.d.ds.v.v.v.!!'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
@app.route('/')
def index():
	query = "SELECT email FROM `email`.`emails`;"
	emails = mysql.query_db(query)
	return render_template('index.html', emails=emails)

@app.route('/add_email', methods=['POST'])
def add_email():
	email = request.form['email']
	valid = True
	if email == "":
		valid = False
		flash("You need to enter something in the email field", 'danger')	
	if not EMAIL_REGEX.match(email):
  		valid = False
		flash("Email is not valid", 'danger')
		return redirect('/')
	if valid != True:
  		return redirect('/')
	else:
  		query1 = "SELECT * FROM `email`.`emails`;"
  		query2 = "INSERT INTO  `email`.`emails`(`email`) VALUES (:email);"
		data = {
			"email": request.form['email']
		}
		emails = mysql.query_db(query1)
		if len(email) != 0:
  			for i in emails:
  				  if i['email'] == request.form['email']:
  						flash("Email already exists!", 'danger')
						return redirect('/')
		mysql.query_db(query2, data)
		flash("Email Successfully Added", 'success')
		return redirect('/')
	return render_template('index.html')


	
app.run(debug=True)

