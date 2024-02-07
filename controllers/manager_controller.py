from flask import Blueprint, render_template, redirect, session, url_for
from sqlalchemy.orm import joinedload
from flask_session import Session
from models import User, Request,db

manager_controller = Blueprint('manager_controller', __name__)

@manager_controller.route("/manager", methods=["GET"])
def manager():
    if "user_id" not in session:
        return redirect(url_for("login_controller.login"))

    if not session.get("is_manager", False):
        return redirect(url_for("feed_controller.feed"))

    manager_user_id = session["user_id"]
    requests = (
        db.session.query(Request)
        .join(User, Request.user_id == User.user_id)
        .filter(User.manager_id == manager_user_id)
        .filter(Request.status == 'pending') 
        .order_by(Request.timestamp.desc())
        .options(joinedload(Request.user))
        .all()
    )

    return render_template("manager.html", requests=requests)