from flask import Flask,render_template,request,url_for,session,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import TextField,PasswordField,validators,ValidationError,SubmitField
from functools import wraps

app=Flask(__name__)
app.secret_key = "seinfeld is awesome"
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:////home/shyam/flask-application/blog/users.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class users(db.Model):
	__tablename__ = 'users'
	username=db.Column(db.String(75),primary_key=True)
	password=db.Column(db.String(75))
	email=db.Column(db.String(75))

	def __init__(self,username,password,email):
		self.username=username
		self.password=password
		self.email=email


db.create_all()

class Regform(Form):
	username=TextField("Username",[validators.Required("Please fill out this field")])
	email=TextField("Email",[validators.Required("Please fill out this field")])
	password=PasswordField("Password",[validators.Required("Please fill out this field")])
	confirm=PasswordField("Re-enter Password",[validators.EqualTo('password',message='This should match with the chosen password')] )
	submit=SubmitField("Register!")

@app.route('/')
def index():
	return render_template("index.html")


def login_required(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session :
			return f(*args,**kwargs)
		else :
			flash("You need to login first !","error")
			return redirect(url_for("index"))

	return wrap


@app.route('/home')
@login_required
def home():
	return render_template("home.html")

		
@app.route('/register',methods=['GET','POST'])
def register():
	#form = Regform(request.form)
	if request.method == "POST" :
		form = Regform(request.form)
		if not request.form["username"] or not request.form["email"] or not request.form["password"] or \
		   not request.form["confirm"] :
		   flash("Please fill all the fields","error")
		   return render_template("register.html",form=form,error="Some field is empty")	   
		
		else:
		   x=users.query.filter_by(username=request.form["username"])
		   if x is None :
			  user=users(request.form["username"],request.form["password"],request.form["email"])
			  db.session.add(user)
			  db.session.commit()

			  flash("Registered successfully !")
			  return redirect(url_for('home'))
		   else :
			  flash("This username is already taken. Kindly choose another handle","error")
			  return render_template("register.html",form=form)    	 
	
	else :
		
		form = Regform(request.form)
		return render_template("register.html",form=form,error="post check condition fails") 

@app.route("/login",methods=['GET','POST'])
def login():
	if request.method == "POST" :
		username= request.form["username"]
		password= request.form["password"]
		registered_user= users.query.filter_by(username=username,password=password).first()
		if registered_user is None :
		   flash("Username or Password is incorrect","error")
		   return redirect(url_for('index'))  
		
		session["logged_in"] = True
		session["username"] = username
		flash("Logged in successfully")
		return redirect(url_for('home'))
	
	return redirect(url_for("index"))  
 
@app.route("/logout")
@login_required
def logout():
	session.clear()
	return redirect(url_for("index")) 


if __name__ == '__main__' :
	app.run(debug=True) 