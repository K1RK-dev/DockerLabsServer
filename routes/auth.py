from flask import Blueprint, request, jsonify
from services.auth_service import *

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user, error_message = register_user(username, password)
    if error_message:
        return jsonify({"msg": error_message}), 400

    return jsonify({"msg": "User created successfully"}), 201

@auth_bp.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user, error_message = login_user(username, password)

    if error_message:
        return jsonify({"msg": error_message}), 401

    return jsonify({"msg": "Login successful"}), 200