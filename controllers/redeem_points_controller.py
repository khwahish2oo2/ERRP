from flask import Blueprint, render_template, request, session ,redirect,url_for
from flask_session import Session
from models import User,Coupon,db
import random
import string


redeem_points_controller = Blueprint('redeem_points_controller', __name__)
def get_random_string(length):
     letters = string.ascii_uppercase
     result_str=''.join(random.choice(letters) for i in range(length))
     return result_str
     
@redeem_points_controller.route('/redeem_points', methods=['GET', 'POST'])
def redeem_points():
    if 'user_id' not in session:
        return redirect(url_for('login_controller.login'))
      
    employee = session['user_id']
    employee_points = User.query.filter_by(user_id=employee).first()

    if employee_points:
        points = employee_points.curr_points
        user_id=employee_points.user_id

        if request.method == 'POST':
            success_messages = []
            error_messages = []
            redeem_option = request.form.get('redeem_option')
            if redeem_option:
                points_key = f"{redeem_option}_points"
                required_points = int(request.form.get(points_key, 0))
                if employee_points.curr_points >= required_points:
                    employee_points.curr_points -= required_points
                    db.session.commit()                   
                    success_messages.append(f'Redeemed {redeem_option.capitalize()} voucher successfully!, {required_points} points deducted.')
                    voucher_name = f"{redeem_option.capitalize()} Voucher"
                    voucher_worth = required_points
                    if required_points==0:
                        return render_template('redeem.html',points=points)                    
                else:
                    error_messages.append(f'Insufficient points to redeem {redeem_option.capitalize()}.')

            if success_messages:
                        s=voucher_name[0]+get_random_string(4)+str(voucher_worth)
                        new_coupon = Coupon(user_id=user_id, coupon_name=voucher_name, coupon_code=s)
                        db.session.add(new_coupon)
                        db.session.commit()
                        return render_template('redeem_success.html', points=employee_points.curr_points, s=s, voucher_name=voucher_name, voucher_worth=voucher_worth)
            elif error_messages:
                        return render_template('redeem_success.html', error_messages=error_messages, points=employee_points.curr_points)
        return render_template('redeem.html', points=points)


