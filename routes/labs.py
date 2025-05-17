from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required

from models import Lab
from models.role import RoleType
from utils.decorators import roles_required
import services.labs_service as labs_service

labs_bp = Blueprint('labs', __name__, url_prefix='/labs')

@labs_bp.route('/get_labs', methods=['GET'])
@login_required
def get_labs():
    labs, error = labs_service.get_labs()
    if error:
        return jsonify({'error': error}), 400
    labs_list = [lab.to_dict() for lab in labs]
    return jsonify({'labs': labs_list}), 200

@labs_bp.route('/create_lab', methods=['POST'])
@login_required
@roles_required([RoleType.ADMIN, RoleType.TEACHER], current_user)
def create_lab():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    image_id = data.get('image_id')
    result, error = labs_service.create_lab(title, description, image_id, current_user.id)
    if error:
        return jsonify({'msg': error}), 403
    return jsonify({'msg': 'Lab created successfully'}), 201

@labs_bp.route('/delete_lab/<int:lab_id>', methods=['DELETE'])
@login_required
@roles_required([RoleType.ADMIN, RoleType.TEACHER], current_user)
def delete_lab(lab_id):
    lab = Lab.query.get_or_404(lab_id)
    if lab.user_id != current_user.id and current_user.role.name != RoleType.ADMIN:
        return jsonify({'msg': 'You are not authorized to perform this action'}), 403
    else:
        lab.delete()
        return jsonify({'msg': 'Lab deleted successfully'}), 200