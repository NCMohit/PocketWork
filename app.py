from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/register')
def register():
   return render_template('register.html')

@app.route('/forgotpass')
def forgotpass():
   return render_template('forgotpassword.html')

@app.route('/aboutus')
def aboutus():
   return render_template('aboutus.html')

if(__name__ == "__main__"):
	app.run(debug = True,host="0.0.0.0")