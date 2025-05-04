from flask import Blueprint, request, jsonify
import docker
from flask_login import login_required, current_user
from models.role import RoleType
from models.image import Image
from extensions import db

docker_images_bp = Blueprint('docker_images', __name__, url_prefix='/docker_images')
client = docker.from_env()

@docker_images_bp.route('/', methods=['POST'])
@login_required
def create_image():
    if current_user.role not in (RoleType.ADMIN, RoleType.TEACHER):
        return jsonify({'msg': 'Unauthorized'}), 403

    data = request.get_json()
    name = data.get('name')
    dockerfile = data.get('dockerfile')

    try:
        image, build_log = client.images.build(fileobj=dockerfile, tag=name)
        image_id = image.id
    except Exception as e:
        return jsonify({'msg': f'Error building image: {str(e)}'}), 500

    new_image = Image(name=name, image_id=image_id, teacher_id=current_user.id)
    db.session.add(new_image)
    db.session.commit()

    return jsonify({'msg': 'Image created successfully', 'image_id': image_id}), 201

@docker_images_bp.route('/<int:image_id>', methods=['DELETE'])
@login_required
def delete_image(image_id):
    if current_user.role != 'teacher':
        return jsonify({'msg': 'Unauthorized'}), 403

    image = Image.query.get_or_404(image_id)
    if image.teacher_id != current_user.id:
        return jsonify({'msg': 'Unauthorized'}), 403

    try:
        client.images.remove(image.image_id)
    except Exception as e:
        return jsonify({'msg': f'Error removing image: {str(e)}'}), 500

    db.session.delete(image)
    db.session.commit()

    return jsonify({'msg': 'Image deleted successfully'}), 200