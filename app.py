from flask import Flask,render_template,request,url_for,session,flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import TextField,PasswordField,validators,ValidationError,SubmitField

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


@app.route('/register',methods=['GET','POST'])
def register():
	#form = Regform(request.form)
	if request.method == "POST" :
		form = Regform(request.form)
		if not request.form["username"] or not request.form["email"] or not request.form["password"] or \
		   not request.form["confirm"] :
		   flash("Please fill all the fields","error")
		   return render_template("register.html",form=form,error="Some field empty")	   
		
		else:
		   user=users(request.form["username"],request.form["password"],request.form["email"])
		   db.session.add(user)
		   db.session.commit()

		   flash("Registered successfully !")
		   return render_template("home.html") 	 
	
	else :
		
		form = Regform(request.form)
		return render_template("register.html",form=form,error="post check condition fails") 

if __name__ == '__main__' :
	app.run(debug=True) 