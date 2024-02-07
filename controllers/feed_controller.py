from flask import Blueprint,render_template, redirect, session, url_for
from sqlalchemy.orm import aliased
from sqlalchemy import func
from flask_session import Session
from models import User, Post, Likes,db

feed_controller = Blueprint('feed_controller', __name__)

@feed_controller.route("/feed")
def feed():
    if 'user_id' not in session:
        return redirect(url_for('login_controller.login'))
    manager_alias = aliased(User, name="manager")

    subquery = (
        db.session.query(Likes.post_id)
        .filter(
            Likes.post_id == Post.post_id,
            Likes.user_id == session["user_id"],
        )
        .exists()
    )

    query = (
        db.session.query(
            User.username.label("user_name"),
            manager_alias.username.label("manager_name"),
            func.date_format(Post.timestamp,'%d/%m/%Y').label('timestamp'),
            Post.post_id,
            Post.content,
            Post.category,
            Post.points,
            subquery.label("liked"),
        )
        .join(manager_alias, User.manager_id == manager_alias.user_id)
        .join(Post, User.user_id == Post.user_id)
        .order_by(Post.timestamp.desc())
    )

    result = query.all()
    return render_template('feed.html', posts=result, session = session,len=len(result))
