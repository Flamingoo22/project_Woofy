from flask import render_template, redirect, session, flash, request, jsonify
from flask_app import bcrypt,app
from flask_app.models.user_model import User
from datetime import datetime

dt = datetime.now()



@app.route('/')
def index():
    return render_template('splash_page.html')

@app.route('/woofy/register')
def reg_page():
    return render_template('log_in.html')

'''
********************************
ACTION ROUTES
********************************
'''

@app.route('/register', methods = ['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/woofy/register')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password':pw_hash
    }
    user = User.create(data)
    session['uuid'] = user
    return redirect('/dashboard')

@app.route('/login', methods = ['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/woofy/register')
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    del session['uuid']
    return redirect('/dashboard')

@app.route('/woofy/update', methods = ['POST'])
def update_user():
    data = {
        **request.form,
        'id':session['uuid']
    }
    User.update(data)
    return jsonify()

@app.route('/woofy/user_update')
def get_user():
    if 'uuid' not in session:
        return redirect('/woofy/register')
    user = User.show_one({'id':session['uuid']})
    str_dob = user.dob.strftime('%Y-%m-%d')
    res = {
        'username':user.username,
        'dob':str_dob
    }
    return jsonify(res)