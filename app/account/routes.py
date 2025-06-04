import os
import bcrypt

from flask import Blueprint, render_template, request, redirect, url_for
from flask import session


from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

from app.models import Users
from app.database import db

acc_bp = Blueprint('account', __name__, url_prefix='/account')


@acc_bp.route('/login',methods=['GET'])
def get_login():
    return render_template('login.html')

@acc_bp.route("/test", methods=['GET'])
@login_required
def test_acc():
    return "test"

@acc_bp.route("/login", methods=['POST'])
def login():
    l_user = Users.query.filter(Users.username == request.form["username"]).first()
    print(l_user)
    if l_user and l_user.check_password(password=request.form["password"]):
        login_user(l_user)
        return redirect(url_for('home'))
    return render_template('login.html', form=request.form)


@acc_bp.route('/logout',methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/account/login')
