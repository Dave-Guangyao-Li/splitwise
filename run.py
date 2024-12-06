from splitwise.app import create_app
from splitwise.app.models import db
from flask_migrate import Migrate
import os

app = create_app()
migrate = Migrate(app, db)

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
