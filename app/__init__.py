import os
import bcrypt

from flask import Flask, render_template, request, redirect, url_for
from flask import session


from flask_login import LoginManager, UserMixin, login_required, current_user
from flask_login.mixins import AnonymousUserMixin


from app.account.routes import acc_bp
from app.manager.routes import man_bp

from .database import db, init_db
from .models import *

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/account/login?next=' + request.path)



basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

@app.route("/")
def home(endpoint="home"):
    print(current_user)
    if isinstance(current_user, AnonymousUserMixin):
        username=""
        return redirect(url_for("account.login"))
    else:
        username=current_user.username
        return render_template("base.html", username=username)

@app.route("/logs")
@login_required
def fetch_logs():
    return "test fetch logs"


@app.route("/settings")
@login_required
def settings():
    return "test settings page"

def create_app(config_class='config.Config'):
    app.config.from_object(config_class)
    app.secret_key = b'_1#y2Lc9EQ0zcd9ubr])'

    init_db(app)
    login_manager.init_app(app)
    app.register_blueprint(acc_bp)
    app.register_blueprint(man_bp)

    return app
