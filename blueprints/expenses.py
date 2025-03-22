from flask import Blueprint, redirect, render_template, url_for, flash, current_app
from flask_login import login_required, current_user
from blueprints.databases import db, Expenses
from blueprints.forms import ExpenseForm, ExpenseDateScopeForm
import matplotlib.pyplot as plt
import os


expense = Blueprint("expense", __name__)


def generate_expense_plot(expenses):
    # Extract data for the plot
    labels = [expense.name for expense in expenses]
    values = [expense.value for expense in expenses]

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='skyblue')
    plt.xlabel('Expense Name')
    plt.ylabel('Expense Value')
    plt.title('Expenses Overview')
    plt.xticks(rotation=45, ha='right')

    # Save the plot to a static folder
    plot_path = os.path.join(current_app.static_folder, 'expense_plot.png')
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()  # Close the plot to free memory

    return 'expense_plot.png'


@login_required
@expense.route("/expenses/<int:user_id>")
def expenses(user_id):
    form_date = ExpenseDateScopeForm()
    form = ExpenseForm()

    # Changing date scope to display expenses
    if form_date.validate_on_submit():
        start_date = form_date.date_start.data
        end_date = form_date.date_end.data

        user_expenses = Expenses.query.filter(Expenses.user_id == user_id, Expenses.date_posted >= start_date, Expenses.date_posted <= end_date).all()

        plot_filename = generate_expense_plot(user_expenses)
        return render_template("expenses.html", user_expenses=user_expenses, form=form_date, plot_filename=plot_filename)

    # Default bahaviour
    user_expenses = Expenses.query.filter(Expenses.user_id == user_id).all()
    plot_filename = generate_expense_plot(user_expenses)


    return render_template("expenses.html", user_expenses=user_expenses, form=form, form_date=form_date, plot_filename=plot_filename)


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

