from flask import Blueprint, jsonify
from flask_login import login_required, current_user

import services.users_service as users_service
from models.role import RoleType
from utils.decorators import roles_required

users_bp = Blueprint("users", __name__)

@login_required
@roles_required([RoleType.ADMIN, RoleType.TEACHER], current_user)
@users_bp.route('/get_students', methods=['GET'])
def get_students():
    students, error = users_service.get_students()
    if error:
        return jsonify({'error': error}), 400
    students_list = [student.to_dict() for student in students]
    return jsonify({'students': students_list}), 200