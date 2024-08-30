from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError

database = SQLAlchemy()

def db_init(app):
    database.init_app(app=app)
    
    with app.app_context():
        try:
            database.create_all()
            print("Create DB")
        except OperationalError as e:
            print(f"Error {e}")

