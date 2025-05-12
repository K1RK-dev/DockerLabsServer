from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from extensions import db
from models import Lab
from models.role import RoleType
from utils.decorators import roles_required

labs_bp = Blueprint('labs', __name__, url_prefix='/labs')

@labs_bp.route('/', methods=['POST'])
@login_required
@roles_required([RoleType.ADMIN, RoleType.TEACHER], current_user)
def create_lab():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    image_id = data.get('image_id')

    new_lab = Lab(title=title, description=description, image_id=image_id, teacher_id=current_user.id)
    db.session.add(new_lab)
    db.session.commit()

    return jsonify({'msg': 'Lab created successfully'}), 201