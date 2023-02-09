from app import app
from app.models import User
from flask import render_template, url_for, redirect, flash
from app.forms import SignUpForm, LoginForm
from flask_login import login_user, logout_user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Form Submitted and Validated!')
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(email, username, password)
        check_user = User.query.filter( (User.username == username) | (User.email == email) ).all()
        if check_user:
            flash('Please choose another username.email', 'danger')
            return redirect(url_for('signup'))
        new_teamate = User(email=email, username=username, password=password)
        flash(f'{new_teamate.username} has been created!', 'success-subtle')
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm() 
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email, password)
        user = User.query.filter_by(email=email).first()
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f"{user.username} is now logged in", "warning")
            return redirect(url_for('index'))
        else:
            flash("Incorrect username and/or password", "danger")
            return redirect(url_for('login'))
        
    return render_template('login.html', form=form)

@app.route('/calender')
def calender():
    return render_template('calender.html')
