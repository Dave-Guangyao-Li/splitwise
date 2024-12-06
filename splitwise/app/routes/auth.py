from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
from ..models import db, User
from werkzeug.security import check_password_hash

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validate input
        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return redirect(url_for('auth.register'))
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email is already registered. Please use a different email.', 'error')
            return redirect(url_for('auth.register'))
        
        # Create new user
        try:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('auth.login'))
        
        except IntegrityError:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'error')
            return redirect(url_for('auth.register'))
    
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        
        flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    """User logout route"""
    logout_user()
    return redirect(url_for('main.index'))
