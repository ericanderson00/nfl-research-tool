from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user #this is why I need UserMixin in models.py

auth = Blueprint('auth', __name__)


# my actual hotamil and password: Spiderman3
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first() # filter all users that have this email and return the first result
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True) #unless browser history is cleared or web app restarts, user remains logged in
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password, try again.", category='error')
        else:
            flash('Email does not exist', category='error')
    
    return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.landing_page'))
    # return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(first_name) < 2:
            flash('First must be greater than 1 characters', category='error')
        elif password1 != password2:
            flash('Passwords dont\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must must be at least 7 characters', category='error')
        else:
            
            # creates a new User
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method="pbkdf2:sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True) #unless browser history is cleared or web app restarts, user remains logged in
            flash('Account Created!', category='success')
            return redirect(url_for('views.home'))
            
            
    return render_template("sign_up.html",user=current_user)
