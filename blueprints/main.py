from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, LoginManager
from blueprints.forms import LoginForm, RegisterForm
from blueprints.databases import User, db
from werkzeug.security import generate_password_hash, check_password_hash



main = Blueprint("main", __name__)

login_manager = LoginManager()
login_manager.login_view = "main.index"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main.route("/", methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        # return to user main page with user data
        pass

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            # return to user main page with user data
            pass
        elif user and not check_password_hash(user.password, form.password.data):
            flash("Incorrect password!")
            return redirect(url_for("index"))
        else:
            flash("User not found!")
            return redirect(url_for("index"))
        

    return render_template("index.html", form=form)


@main.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for("index"))


@main.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        # return to user main page with user data
        pass

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        user = User.query.filter(User.username == username).first()

        if user:
            flash("Username already exists! Log in now!")
            redirect(url_for("index"))
        else:
            new_user = User(username=username, password=generate_password_hash(password, method="sha256"), email=email)
            db.session.add(new_user)
            db.session.commit()
            flash("Successfully registered! You can now log in!")
            redirect(url_for("index"))


    return render_template("register.html", form=form)
