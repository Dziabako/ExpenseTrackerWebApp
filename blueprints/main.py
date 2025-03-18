from flask import Blueprint, render_template, flash, redirect
from flask_login import login_user, logout_user, current_user, LoginManager
from blueprints.forms import LoginForm
from blueprints.databases import User


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
        if user and user.password == form.password.data:
            login_user(user)
            # return to user main page with user data
            pass
        elif user and user.password != form.password.data:
            flash("Incorrect password!")
            return redirect("index")
        else:
            flash("User not found!")
            return redirect("index")
        

    return render_template("index.html", form=form)


@main.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect("index")


@main.route("/register", methods=["GET", "POST"])
def register():
    

    return render_template("register.html")
