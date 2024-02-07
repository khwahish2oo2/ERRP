from flask import Flask
from flask_bcrypt import Bcrypt 
from flask_session import Session
from controllers import home_controller, feed_controller, login_controller,leaderboard_controller,logout_controller, new_blog_controller, requests_controller, manager_controller, likefunction_controller, redeem_points_controller, coupons_controller, profile_controller
from models import User, Post, Likes,Request,Coupon,db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Khwahish21@localhost/errp_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db.init_app(app)
bcrypt = Bcrypt(app)

app.register_blueprint(home_controller.home_controller)

app.register_blueprint(feed_controller.feed_controller)

app.register_blueprint(login_controller.login_controller)

app.register_blueprint(leaderboard_controller.leaderboard_controller)

app.register_blueprint(logout_controller.logout_controller)

app.register_blueprint(new_blog_controller.new_blog_controller)

app.register_blueprint(manager_controller.manager_controller)

app.register_blueprint(requests_controller.requests_controller)

app.register_blueprint(likefunction_controller.likefunction_controller)    

app.register_blueprint(redeem_points_controller.redeem_points_controller)    

app.register_blueprint(coupons_controller.coupons_controller)

app.register_blueprint(profile_controller.profile_controller)

if __name__ == '__main__':
    app.run(debug=True)



