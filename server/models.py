from datetime import datetime

from server import db
from flask import jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from server import jwt

class User(db.Model):
    """
    User model
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    logs = db.relationship('Logs', backref='user', lazy=False)

    def __init__(self, username, name, last_name, password):
        self.username = username
        self.name = name
        self.last_name = last_name
        self.password = generate_password_hash(password, method='sha256')

    @classmethod
    def auth(cls, username, password):

        # check if user provide login and password
        if not username or not password:
            return None

        user = cls.query.filter_by(username=username).first()

        # check if user exist and provide proper password
        if not user or not check_password_hash(user.password, password):
            return None

        # if everything ok, return jwt token
        token = create_access_token(identity=user.id)
        log = Logs(user_id=user.id)
        db.session.add(log)
        db.session.commit()
        return token



class Logs(db.Model):
    """
    Logs model
    """
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, user_id):
        self.date = datetime.now()
        self.user_id = user_id


    @staticmethod
    def get_user_logs(user_id):

        logs= Logs.query.filter_by(user_id=user_id).all()
        login_dates = [log.date for log in logs]
        return login_dates


class ExpiredToken(db.Model):
    """
    Expired token model
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.date = datetime.now()

    @staticmethod
    @jwt.token_in_blacklist_loader
    def check_token(token):
        token_object = ExpiredToken.query.filter_by(token=str(token['jti'])).first()
        if token_object:
            return True
        return False

    @staticmethod
    def save_expired_token(token):
        token = ExpiredToken(token=token)
        try:
            db.session.add(token)
            db.session.commit()
            return 'Success'
        except Exception as e:
            return e
