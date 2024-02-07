from flask import Blueprint, request, redirect, session, url_for, jsonify
from sqlalchemy import func,update,select
from datetime import datetime, timedelta
from flask_session import Session
from models import User, Post, Likes,Request,db

likefunction_controller = Blueprint('likefunction_controller', __name__)

@likefunction_controller.route("/likefunction",methods=['POST'])
def likefunction():
    if 'user_id' not in session:
        return redirect(url_for('login_controller.login'))
    post_id=request.json.get("post_id")
    liked=request.json.get("liked")

    def update_points(x,post_id):
        subquery = (
                select(Post.user_id)
                .where(Post.post_id == post_id) 
                .alias('subquery')
            )

        update_user_points = (
            update(User)
            .values(curr_points=User.curr_points +x, points=User.points + x)
            .where(User.user_id.in_(subquery))
        )

        update_post_points = (
            update(Post)
            .values(points=Post.points +x)
            .where(Post.post_id == post_id)
        )

        db.session.execute(update_post_points)
        db.session.execute(update_user_points)
        db.session.commit()
        
    if liked:
        new_likepost = Likes(user_id=session["user_id"], post_id=post_id)
        db.session.add(new_likepost)
        db.session.commit()
            #updating points
        update_points(5,post_id)

    else:
        # deleting the 
        db.session.query(Likes).filter_by(post_id=post_id, user_id=session["user_id"]).delete()
        db.session.commit()
            #updating points
        update_points(-5,post_id)
    
    return jsonify({'update': True})
