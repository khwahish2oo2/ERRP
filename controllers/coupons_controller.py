from flask import Blueprint, render_template, request, redirect, session, url_for
from flask_session import Session
from models import Coupon

coupons_controller = Blueprint('coupons_controller', __name__)

@coupons_controller.route("/coupons")
def coupons():
    if 'user_id' not in session:
        return redirect(url_for('login_controller.login'))
    employee_id=session['user_id']
    print(employee_id)
    details = Coupon.query.with_entities(Coupon.coupon_name, Coupon.coupon_code, Coupon.expiry_date).filter_by(user_id=employee_id).all()
    return render_template('coupons.html', title = 'coupons', len = len(details), details=details)
