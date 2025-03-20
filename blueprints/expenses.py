from flask import Blueprint, redirect, render_template, url_for, flash
from flask_login import login_required, current_user
from blueprints.databases import db, Expenses
from blueprints.forms import ExpenseForm


expense = Blueprint("expense", __name__)


@login_required
@expense.route("/expenses/<int:user_id>")
def expenses(user_id):
    user_expenses = Expenses.query.filter(Expenses.user_id == user_id).all()
    form = ExpenseForm()

    return render_template("expenses.html", user_expenses=user_expenses, form=form)


@login_required
@expense.route("/add_expense", methods=["GET", "POST"])
def add_expense():
    form = ExpenseForm()

    if form.validate_on_submit():
        name = form.name.data
        value = form.value.data
        date = form.date.data

        new_expense = Expenses(name=name, value=value, date_posted=date, user_id=current_user.id)
        db.session.add(new_expense)
        db.session.commit()

        flash("Expense added!")
        return redirect(url_for("expense.expenses", user_id=current_user.id))
    

@login_required
@expense.route("/delete_expense/<int:expense_id>")
def delete_expense(expense_id):
    expense = Expenses.query.filter(Expenses.id == expense_id).first()

    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted!")
    return redirect(url_for("expense.expenses", user_id=current_user.id))


@login_required
@expense.route("/edit_expense/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):
    expense = Expenses.query.filter(Expenses.id == expense_id).first()
    form = ExpenseForm()

    if form.validate_on_submit():
        expense.name = form.name.data
        expense.value = form.value.data
        expense.date_posted = form.date.data

        db.session.commit()
        flash("Expense edited!")
        return redirect(url_for("expense.expenses", user_id=current_user.id))

    return render_template("edit_expense.html", form=form, expense=expense)

