from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired(), EqualTo(password)])
    submit = SubmitField("Register")


class ExpenseForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    value = StringField("Value", validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()])
    submit = SubmitField("Add expense")


class ExpenseDateScopeForm(FlaskForm):
    date_start = DateField("Start date", validators=[DataRequired()])
    date_end = DateField("End date", validators=[DataRequired()])
    sumbit = SubmitField("Filter")
