from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Import and register blueprints
    from .routes import main, auth, groups, expenses
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(groups.bp)
    app.register_blueprint(expenses.bp)

    # Import models to ensure they are recognized by Flask-Migrate
    from .models import User, Group, Expense, ExpenseSplit

    return app
