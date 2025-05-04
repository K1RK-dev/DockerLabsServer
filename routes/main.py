from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"