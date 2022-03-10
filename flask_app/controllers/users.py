from flask import render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register', methods=['POST'])
def create_user():

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirm_password': request.form['confirm_password']
    }
    if User.validate(data):
        print('successful')
        
        new_user_data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
        }
        new_user_id = User.create(new_user_data)

        session['user_id'] = new_user_id
        session['email'] = new_user_data['email']
        session['first_name'] = new_user_data['first_name']
        return redirect('/dashboard')
        flash('Creation successful!')
    
    else:
        print('Does not pass validation')
        return redirect('/')




@app.route('/login', methods=['POST'])
def login():
    user = User.get_one(request.form)
    if user == None:
        flash("no user")
        return redirect('/')

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Incorrect password, try again')
        return redirect('/')

    print("passes")
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    session['email'] = user.email
    return redirect('/dashboard')



@app.route('/dashboard')
def success():
    if 'user_id' not in session:
        flash('This page only available if logged in')
        return redirect('/')
    return render_template('dashboard.html')


@app.route('/logout')
def delete():
    session.clear()
    flash("logged out")
    return redirect('/')
