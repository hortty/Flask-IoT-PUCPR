from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, login_required, logout_user, current_user 
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

auth = Blueprint("auth", __name__, 
                    template_folder="./views/", 
                    static_folder='./static/', 
                    root_path="./")

@auth.route("/")
@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    
    logout_user()
    
    return redirect(url_for('index'))

@auth.route('/login_post', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    
    login_user(user)
    
    return redirect("/admin")

@auth.route('/cadastro_user')
def cadastro_user():
    return render_template("/cadastro_user.html")

@auth.route('/cadastrar_user', methods=['POST'])
def cadastrar_user():
    # code to validate and add user to database goes here
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    permission = request.form.get("permission")
    
    User.save_user(username=username, email=email, password=generate_password_hash(password), permission=permission)

    return redirect(url_for('auth.login'))

