import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Resource, Api
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_SECRET_KEY'] = 'askdmaskdms12qdwed!W!adnasa1343432'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

db = SQLAlchemy(app)

from server.views import auth_blueprint
app.register_blueprint(auth_blueprint)