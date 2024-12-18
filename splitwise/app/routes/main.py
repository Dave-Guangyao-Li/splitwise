from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing expenses and groups"""
    return render_template('dashboard.html')
