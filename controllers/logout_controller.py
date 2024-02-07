from flask import Blueprint, redirect, session, url_for 
from flask_session import Session

logout_controller = Blueprint('logout_controller', __name__)

@logout_controller.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home_controller.home'))