from app import app
from flask import render_template
from app.forms import SignUpForm, LoginForm

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    return render_template('signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)
