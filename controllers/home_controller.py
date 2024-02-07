from flask import Blueprint, render_template

home_controller = Blueprint('home_controller', __name__)

@home_controller.route("/")
@home_controller.route("/home")
def home():
    return render_template('home.html',title='Home')
