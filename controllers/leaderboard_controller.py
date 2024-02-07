from flask import Blueprint,Flask, render_template, redirect, session, url_for, flash, jsonify
from models import User
from flask_session import Session

leaderboard_controller = Blueprint('leaderboard_controller', __name__)

@leaderboard_controller.route("/leaderboard")
def leaderboard():
    if 'user_id' not in session:
        return redirect(url_for('login_controller.login'))
    details = User.query.with_entities(User.name, User.points).order_by(User.points.desc()).all()
    return render_template('leaderboard.html', title = 'leaderboard', len = len(details), details = details)
