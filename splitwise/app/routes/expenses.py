from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import db, Expense, ExpenseSplit, Group, User
import math

bp = Blueprint('expenses', __name__)

def split_expense(expense, group, split_type):
    """
    Calculate expense splits based on different methods
    """
    members = group.members
    total_amount = expense.amount
    splits = []

    if split_type == 'equal':
        # Equal split among group members
        split_amount = round(total_amount / len(members), 2)
        
        # Adjust for rounding errors
        remainder = total_amount - (split_amount * len(members))
        
        for i, member in enumerate(members):
            if member != expense.payer:
                # Add slight adjustment to last split to account for rounding
                adjusted_split = split_amount + (remainder if i == len(members) - 1 else 0)
                splits.append({
                    'user': member,
                    'amount': adjusted_split
                })
    
    elif split_type == 'percentage':
        # Percentage-based split (placeholder for future implementation)
        split_amount = round(total_amount / len(members), 2)
        for member in members:
            if member != expense.payer:
                splits.append({
                    'user': member,
                    'amount': split_amount
                })
    
    elif split_type == 'exact':
        # Exact amount split (to be implemented with frontend input)
        split_amount = round(total_amount / len(members), 2)
        for member in members:
            if member != expense.payer:
                splits.append({
                    'user': member,
                    'amount': split_amount
                })
    
    return splits

@bp.route('/expense/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    """Add a new expense"""
    if request.method == 'POST':
        description = request.form.get('description')
        amount = float(request.form.get('amount'))
        group_id = request.form.get('group_id')
        split_type = request.form.get('split_type')
        
        # Create expense
        group = Group.query.get(group_id)
        expense = Expense(
            description=description, 
            amount=amount, 
            payer=current_user,
            group_id=group_id,
            split_type=split_type
        )
        db.session.add(expense)
        
        # Calculate and save splits
        expense_splits = split_expense(expense, group, split_type)
        
        for split in expense_splits:
            expense_split = ExpenseSplit(
                expense=expense, 
                user=split['user'], 
                amount=split['amount']
            )
            db.session.add(expense_split)
        
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    # GET request: show add expense form
    groups = Group.query.filter(Group.members.contains(current_user)).all()
    return render_template('add_expense.html', 
                           groups=groups, 
                           split_types=['equal', 'percentage', 'exact'])

@bp.route('/expenses')
@login_required
def list_expenses():
    """List user's expenses"""
    expenses = Expense.query.filter_by(payer=current_user).all()
    return render_template('expenses.html', expenses=expenses)

@bp.route('/expense/<int:expense_id>')
@login_required
def expense_detail(expense_id):
    """Show expense details and splits"""
    expense = Expense.query.get_or_404(expense_id)
    return render_template('expense_detail.html', expense=expense)
