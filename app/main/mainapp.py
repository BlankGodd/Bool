#!/usr/bin/python
# Author:   @BlankGodd_

# packages
from flask import *
from flask_login import login_required, current_user
from flask_login import login_user, logout_user

# user created 
from . import main
from .. import db
from ..models import Account, User
from ..generator import *
from .schema import *
from .payment import *

# system
import re

@main.route('/')
def index():
    return render_template('index.html')


"""Authentication"""
@main.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        data = {"email":email,"password":password}
        # schema validation
        schemaval = validate_login(data)
        if schemaval["msg"] != "success":
            flash("Invalid Credentials")
            return render_template('login.html')
        user = User.query.filter_by(email=email).first()
        if user and validate_pass(user, password):
            login_user(user, request.form.get('remember_me'))
            return redirect(url_for('.dashboard'))
        flash('Invalid Username or Password!')
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.index'))

@main.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        phone = request.form.get('phone')
        location = request.form.get('location')

        data = {
            "email":email,"firstname":firstname,
            "lastname":lastname,"password":password,
            "address":location,"phone":phone
        }

        # schema validation here
        schemaval = validate_reg(data)
        if schemaval["msg"] != 'success':
            flash("Incorrect or Incomplete Credentials")
        # other validations
        elif User.query.filter_by(email=email).first():
            flash("Email already registered!")
        elif password != cpassword:
            flash("Passwords do not match!")
        elif not re.fullmatch(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", email):
            flash('Enter valid email')
        # check if phone is valid
        else:
            # hash password
            password = password_gen(password)
            user = User(email=email,password_hash=password,
                    fullname=firstname+" "+lastname,
                    phone=phone, location=location)
            db.session.add(user)
            db.session.commit()
            # open account and get id
            acc_id = create_acc(user.id)
            user.acc_id = acc_id
            db.session.add(user)
            db.session.commit()
            
            # create confirmation token
            token = gen_confirm_token(user)
            # send email
            flash('Check email to confirm account!')
            return redirect(url_for('.login'))

        return render_template('register.html')
    return render_template('register.html')


def create_acc(user_id):
    # generate account id
    acc_id = int(gen_acc_id(user_id))
    # check db to see if its unique
    que = Cash_account.query.filter_by(_id=acc_id).first()
    while que:
        acc_id = int(gen_acc_id(user_id))
        que = Cash_account.query.filter_by(_id=acc_id).first()
    # add account to db if unique
    acc = Account(_id=acc_id)
    db.session.add(acc)
    db.session.commit()
    return acc_id

@main.route('/confirmtoken/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('.profile'))
    if confirm_token(current_user, token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('.dashboard'))

# confirm account from profile view func

"""Done with Authentication"""

"""Profiling"""
@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@main.route('/savings', methods=['POST','GET'])
@login_required
def savings():
    if request.method == 'POST':
        method = request.form.get('method')
        amount = request.form.get('amount')

    return render_template('save_history.html')

"""Paystack Implementation"""
