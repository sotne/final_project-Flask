from app import app
from flask import render_template,url_for,redirect

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/seemore')
def see_more():
    return render_template('knowmore.html')