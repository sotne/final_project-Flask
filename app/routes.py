from app import app
from app.models import User, Updates
from flask import render_template, url_for, redirect, flash, request
from app.forms import SignUpForm, LoginForm, UpdatesForm
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/')
def index():
    updates = Updates.query.all()
    return render_template('index.html', updates=updates)

@app.route('/contactus')
def contactus():
    # if request.method == 'POST':
    #     return redirect(url_for('index'))
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

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out', 'border subtle')
    return redirect(url_for('index'))

@app.route('/calender')
def calender():
    return render_template('calender.html')

@app.route('/create', methods= ['GET', 'POST'])
@login_required
def create():
    form = UpdatesForm()
    if form.validate_on_submit():
        body=form.body.data
        new_update = Updates(user_id= current_user.id, body=body)
        flash('update posted', 'success')
        return redirect(url_for('index'))
    return render_template('create.html', form=form)

@app.route('/updates/<update_id>/edit', methods = ['GET', 'POST'])
@login_required
def edit(update_id):
    update = Updates.query.get(update_id)
    if not update:
        flash('this post doesntexist', 'danger')
        return redirect(url_for('index'))
    if update.user != current_user:
        flash('this post isnt yours', 'danger')
        return redirect(url_for('index'))
    form = UpdatesForm()
    if form.validate_on_submit():
        body=form.body.data
        update.update(body=body)
        flash('update changed','success')
        return redirect(url_for('index'))
    if request.method == 'GET':
        form.body.data = update.body
    return render_template('edit.html', update=update, form=form)

@app.route('/updates/<update_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(update_id):
    update = Updates.query.get(update_id)
    if not update:
        flash('this post doesntexist', 'danger')
        return redirect(url_for('index'))
    if update.user != current_user:
        flash("You do not have permission to delete this post", "danger")
        return redirect(url_for('index'))
    update.delete()
    flash('update deleted', 'success')
    return redirect(url_for('index'))
