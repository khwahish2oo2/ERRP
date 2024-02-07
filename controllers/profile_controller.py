from flask import Blueprint, render_template, redirect, session, url_for
from flask_session import Session
from models import User, Post, Likes,Request,Coupon,db

profile_controller = Blueprint('profile_controller', __name__)

@profile_controller.route("/Profile", methods=['GET'])
def Profile():
    if 'user_id' not in session:
        return redirect(url_for('login_controller.login'))

    userid = session['user_id'] 
    employees = User.query.filter_by(user_id=userid).first()
    employee_id = employees.user_id
    employee_name=employees.name
    manager=employees.manager_id
    if manager: 
        manager_query = User.query.filter_by(user_id=manager).first()
        employee_manager=manager_query.name
    employee_points = employees.points
    employee_curr_points=employees.curr_points
    if manager: 
        return render_template('profile.html', title = 'New Post', id=employee_id, name=employee_name, manager=employee_manager, points=employee_points, curr_points=employee_curr_points)
    else:
        return render_template('profile.html', title = 'New Post', id=employee_id, name=employee_name, points=employee_points, curr_points=employee_curr_points)
