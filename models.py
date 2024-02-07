from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import aliased
from sqlalchemy import func,update,select
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt 
from flask_session import Session

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    manager_id = db.Column(db.Integer, nullable=True)
    is_manager = db.Column(db.Boolean, nullable=False, default=False)
    points = db.Column(db.Integer, default=0) 
    curr_points = db.Column(db.Integer, default=0) 

class Post(db.Model):
    __tablename__ = 'posts'  
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    points = db.Column(db.Integer, nullable=False, default=0) 
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    user = db.relationship('User', backref='posts')

class Request(db.Model):
    __tablename__= 'requests'
    request_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id')) 
    description = db.Column(db.String(100), nullable=False)
    values = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(15), nullable=False, default='pending')
    user = db.relationship('User', backref='requests')

class Likes(db.Model):
    __tablename__ = 'likes'  
    user_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'),primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),primary_key=True)

##this is in order to store the coupons generated and let the company know which coupon is valid
class Coupon(db.Model):
    __tablename__ = 'coupons'
    coupon_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    coupon_name = db.Column(db.String(20), nullable=False)
    coupon_code = db.Column(db.String(10), nullable=False)
    expiry_date=db.Column(db.Date, default=datetime.utcnow() + timedelta(days=30), nullable=False)
