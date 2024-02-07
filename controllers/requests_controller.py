from flask import Blueprint, render_template, request, redirect, session, url_for, jsonify
from flask_session import Session
from models import User, Post,Request,db

requests_controller = Blueprint('requests_controller', __name__)

@requests_controller.route('/requests',methods=['POST','GET'])
def request_route():
    if 'user_id' not in session:
        return redirect(url_for('login_controller.login'))
        
    if request.method=='POST':
        description=request.form['Content']
        values=request.form['value']
        new_task=Request(user_id=session["user_id"],description=description,values=values)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('feed_controller.feed'))
        except Exception as e:
            print(f"Error: {e}")
            return redirect(url_for('feed_controller.feed'))    
    else:
        return render_template('request.html')


@requests_controller.route('/requests/<int:request_id>', methods=['DELETE'])
def reject_request(request_id):
    request_to_reject = Request.query.get(request_id)

    if request_to_reject:
        request_to_reject.status = 'rejected'
        db.session.commit()

        print(f"Request {request_id} Rejected")

        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Request not found'}), 404
  