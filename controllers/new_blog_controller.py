from flask import Blueprint, render_template, request, redirect, session, url_for
from flask_bcrypt import Bcrypt 
from flask_session import Session
from models import User, Post,Request,db

new_blog_controller = Blueprint('new_blog_controller', __name__)

@new_blog_controller.route("/new_blog", methods=['GET', 'POST'])
def new_blog():
    if 'user_id' not in session:
        return redirect(url_for('logint_controller.login'))
        
    if not session.get('is_manager', False):
        return redirect(url_for('feed_controller.feed'))

    if request.method == 'POST':

        employee_id = request.form.get('employee_id')
        post_content = request.form.get('post_content')
        category = request.form.get('category')
        points = int(request.form.get('points'))
        print(employee_id)
        print(post_content)
        print(category)
        print(points)

        employee = db.session.get(User, employee_id)
        
        if employee:
            employee.points += points
            employee.curr_points+=points
            db.session.commit()

        request_id = request.form.get('request_id')
        print(request_id)
        if request_id:
            request_to_accept = db.session.query(Request).filter_by(request_id=request_id).first()
            if request_to_accept:
                request_to_accept.status = 'accepted'
                db.session.commit()

        new_post = Post(user_id=employee_id, content=post_content, category=category, points=points)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('feed_controller.feed'))

    else:

        manager_id = session['user_id'] 
        employees = User.query.filter_by(manager_id=manager_id).all()

        user_id = request.args.get('user_id')
        description = request.args.get('description')
        values = request.args.get('values')
        request_id = request.args.get('request_id')
        is_manager_view = request.args.get('is_manager_view')


        employee_choices = [(employee.user_id, f"{employee.name} ({employee.user_id})") for employee in employees]
        return render_template('new_blog.html', title = 'New Post', employee_choices=employee_choices, user_id=user_id, description=description, values=values,
                               is_manager_view=is_manager_view,
                               request_id=request_id)
