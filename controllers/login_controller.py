from flask import Blueprint, render_template, request, redirect, session, url_for
from flask_bcrypt import Bcrypt 
from flask_session import Session
from models import User


login_controller = Blueprint('login_controller', __name__)
bcrypt=Bcrypt()
@login_controller.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['username'] = username
            session['user_id'] = user.user_id
            session['is_manager'] = user.is_manager
            return redirect(url_for('feed_controller.feed'))
        else:
            return render_template('login.html', message='Invalid credentials. Please try again.')

    return render_template('login.html', title = 'Login', message=None)
