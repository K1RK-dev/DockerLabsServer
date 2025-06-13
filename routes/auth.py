from flask import Blueprint, request, jsonify
from flask_login import login_required, logout_user, login_user as flask_login_user, current_user
from services.auth_service import *

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    first_name = data.get('firstname')
    last_name = data.get('lastname')
    middle_name = data.get('middlename')
    group = data.get('group')

    if not username or not password:
        return jsonify({"msg": "Username and password is required"}), 400

    user, error_message = register_user(username, password,
                                        group, first_name, last_name, middle_name)
    if error_message:
        return jsonify({"msg": error_message}), 400

    return jsonify({"msg": "User created successfully"}), 201

@auth_bp.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    user, error_message = login_user(username, password)

    if error_message:
        return jsonify({"msg": error_message}), 401

    flask_login_user(user)
    if current_user.is_authenticated:
        return jsonify({
            "msg": "Login successful",
            "username": current_user.username,
            "user_id": current_user.id,
        }), 200
    else:
        return jsonify({"msg": "Login failed"}), 401

@auth_bp.route("/userInfo", methods=['GET'])
@login_required
def user_info():
    role, error_message = get_user_role(current_user)
    if not role:
        return jsonify({"msg": error_message}), 404
    return jsonify({"id": current_user.id, "username": current_user.username, "role": role.name})

@auth_bp.route("/getRole", methods=['GET'])
@login_required
def get_role():
    role, error_message = get_user_role(current_user)
    if not role:
        return jsonify({"msg": error_message}), 404
    return jsonify({"role": role.name}), 200

@auth_bp.route("/logout", methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"msg": "Logout successful"}), 200

@auth_bp.route("/protected", methods=['GET'])
@login_required
def protected():
    return jsonify({"msg": f"Hello, {current_user.username}! This is a protected route."}), 200
