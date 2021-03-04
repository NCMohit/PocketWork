from flask import Flask, redirect, url_for, request, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SECRET_KEY'] = 'mysecretcode'

db = SQLAlchemy(app)

class User(db.Model):
   email = db.Column(db.String(120), unique=True, nullable=False,primary_key=True)
   password_hash = db.Column(db.String(128))
   def set_password(self, password):
      self.password_hash = generate_password_hash(password)
   def check_password(self, password):
      return check_password_hash(self.password_hash, password)

class Posts(db.Model):
   title = db.Column(db.Text, unique=True, nullable=False,primary_key=True)
   desc = db.Column(db.Text)
   category = db.Column(db.Text)
   money = db.Column(db.Integer)
   city = db.Column(db.Text)
   poster = db.Column(db.String(120),db.ForeignKey('user.email'))

class Applications(db.Model):
   id = db.Column(db.Integer,primary_key=True)
   title = db.Column(db.Text,db.ForeignKey('posts.title'), nullable=False)
   poster = db.Column(db.String(120),db.ForeignKey('posts.poster'))
   applier = db.Column(db.String(120),db.ForeignKey('user.email'))

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/login',methods=["POST","GET"])
def login():
   if(request.method == "POST"):
      email = request.form["email"]
      password = request.form["pass"]
      if(User.query.filter_by(email=email).first() is not None):
         if(User.query.filter_by(email=email).first().check_password(password)):
            session['email'] = email
            return redirect(url_for("dashboard"))
         else:
            flash("Wrong password! Please try again")
            return redirect(url_for("login"))
      else:
         flash("Email dosen't exist! Make sure you typed the email correctly")
         return redirect(url_for("login"))
   else:
      return render_template('login.html')

@app.route('/register',methods=["POST","GET"])
def register():
   if(request.method == "POST"):
      email = request.form["email"]
      password = request.form["pass"]
      secondpass = request.form["secondpass"]
      if(password == secondpass):
         if(User.query.filter_by(email=email).first() is None):
            newuser = User(email=email)
            newuser.set_password(password)
            db.session.add(newuser)
            db.session.commit()
            return redirect(url_for("login"))
         else:
            flash("Error email already exists")
            return redirect(url_for("register"))
      else:
         flash("Error passwords do not match")
         return redirect(url_for("register"))
   else:
      return render_template('register.html')

@app.route('/forgotpass')
def forgotpass():
   return render_template('forgotpassword.html')

@app.route('/aboutus')
def aboutus():
   return render_template('aboutus.html')

@app.route('/dashboard')
def dashboard():
   if("email" not in session):
      flash("Please log in first to use the dashboard !")
      return redirect(url_for("login"))
   else:
      allposts = Posts.query.all()
      return render_template('dashboard.html',posts = allposts)

@app.route('/createjob',methods=["POST","GET"])
def createjob():
   if("email" not in session):
      flash("Please log in first to create a job !")
      return redirect(url_for("login"))
   if(request.method == "POST"):
      title = request.form["title"]
      desc = request.form["desc"]
      money = request.form["money"]
      city = request.form["city"]
      cat = request.form["cat"]
      newpost = Posts(title=title,desc=desc,category=cat,money=money,city=city,poster=session['email'])
      db.session.add(newpost)
      db.session.commit()
      return redirect(url_for("dashboard"))
   else:
      return render_template('createjob.html')

@app.route('/applications')
def applications():
   if("email" not in session):
      flash("Please log in first to see your applications !")
      return redirect(url_for("login"))
   else:
      myposts = Posts.query.filter_by(poster=session['email'])
      myapps = []
      for app in Applications.query.filter_by(applier=session['email']):
         myapps.append(Posts.query.filter_by(title=app.title))
      return render_template('applications.html',myposts = myposts,applications = myapps)

@app.route('/apply',methods=["POST","GET"])
def apply():
   if("email" not in session):
      flash("Please log in first to apply for any job !")
      return redirect(url_for("login"))
   else:
      title = request.args.get("title")
      poster = request.args.get("poster")
      applier = session['email']
      newapply = Applications(title=title,poster=poster,applier=applier)
      db.session.add(newapply)
      db.session.commit()
      return redirect(url_for("applications"))

@app.route('/checkapp',methods=["POST","GET"])
def checkapp():
   if("email" not in session):
      flash("Please log in first to apply for any job !")
      return redirect(url_for("login"))
   else:
      title = request.args.get("title")
      poster = session['email']
      applications = Applications.query.filter_by(title=title,poster=poster)
      return render_template("checkapp.html",apps=applications)

@app.route('/logout')
def logout():
   session.clear()
   return redirect(url_for("index"))

if(__name__ == "__main__"):
	app.run(debug = True,host="0.0.0.0")