from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import db, Group, User

bp = Blueprint('groups', __name__)

@bp.route('/group/create', methods=['GET', 'POST'])
@login_required
def create_group():
    """Create a new group"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        # Create group
        group = Group(name=name, description=description)
        group.members.append(current_user)
        
        db.session.add(group)
        db.session.commit()
        
        flash('Group created successfully!')
        return redirect(url_for('main.dashboard'))
    
    return render_template('create_group.html')

@bp.route('/group/<int:group_id>/add_member', methods=['GET', 'POST'])
@login_required
def add_member(group_id):
    """Add a member to a group"""
    group = Group.query.get_or_404(group_id)
    
    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        
        if user:
            if user not in group.members:
                group.members.append(user)
                db.session.commit()
                flash(f'{username} added to the group!')
            else:
                flash(f'{username} is already in the group.')
        else:
            flash('User not found.')
        
        return redirect(url_for('groups.group_detail', group_id=group_id))
    
    return render_template('add_member.html', group=group)

@bp.route('/group/<int:group_id>')
@login_required
def group_detail(group_id):
    """Show group details and expenses"""
    group = Group.query.get_or_404(group_id)
    expenses = group.expenses.all()
    return render_template('group_detail.html', group=group, expenses=expenses)
