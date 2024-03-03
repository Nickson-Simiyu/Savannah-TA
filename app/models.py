from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from app import db
from flask_login import UserMixin
from config import SQLALCHEMY_DATABASE_URI
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash


engine = create_engine(
    "postgresql+psycopg2://postgres:mombasa123@localhost:5432/savannah", pool_size=20, max_overflow=0
)

class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    item = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    time = db.Column(db.DateTime, nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)