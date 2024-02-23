from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

db = SQLAlchemy()
socketio = SocketIO()

def insert_test_data():
    from .model import User
    if not User.query.first():
        test_data = [
            {'name': 'Steve Smith', 'id': 211, 'points': 80},
            {'name': 'Jian Wong', 'id': 122, 'points': 92},
            {'name': 'Chris Peterson', 'id': 213, 'points': 91},
            {'name': 'Sai Patel', 'id': 524, 'points': 94},
            {'name': 'Andrew Whitehead', 'id': 425, 'points': 99},
            {'name': 'Lynn Roberts', 'id': 626, 'points': 90},
            {'name': 'Robert Sanders', 'id': 287, 'points': 75},
            
        ]
        for user_data in test_data:
            user = User(**user_data)
            db.session.add(user)
        db.session.commit()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Wkakklg7'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    db.init_app(app)

    socketio.init_app(app)

    from .views import views
    from .auth import auth

    with app.app_context():
        db.create_all()  # Create database tables
        insert_test_data()  # Insert test data into the database


    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    return app, socketio
