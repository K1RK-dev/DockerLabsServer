from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from services import docker_service
from utils.decorators import roles_required
from services.docker_service import *
from models.role import RoleType

docker_bp = Blueprint('docker', __name__, url_prefix='/docker')

@docker_bp.route('/create_dockerfile', methods=['POST'])
@login_required
@roles_required([RoleType.ADMIN, RoleType.TEACHER], current_user)
def create_dockerfile():
    file = request.files['dockerfile']
    if file.filename == '' or not file:
        return jsonify({'msg': 'No file selected'}), 403
    dockerfile, error = docker_service.create_dockerfile(file)
    if error:
        return jsonify({'msg': error}), 403
    return jsonify({'msg': 'File saved', 'filename': dockerfile.path}), 201

@docker_bp.route('/create_image', methods=['POST'])
@login_required
@roles_required([RoleType.ADMIN, RoleType.TEACHER], current_user)
def create_image():
    data = request.get_json()
    name = data.get('name')
    dockerfile_id = data.get('dockerfile_id')
    image, error = docker_service.create_image(name, dockerfile_id, current_user.id)
    if error:
        return jsonify({'msg': error}), 403
    return jsonify({'msg': 'Image created successfully', 'id': image.id}), 201

@docker_bp.route('/delete_image/<int:image_id>', methods=['DELETE'])
@login_required
@roles_required([RoleType.ADMIN, RoleType.TEACHER], current_user)
def delete_image(image_id):
    image = Image.query.get_or_404(image_id)
    image, error = docker_service.delete_image(image)
    if error:
        return jsonify({'msg': error}), 403
    return jsonify({'msg': 'Image deleted successfully'}), 200

@docker_bp.route('/build_image/<int:image_id>', methods=['POST'])
@login_required
@roles_required([RoleType.ADMIN, RoleType.TEACHER], current_user)
def build_image(image_id):
    image = Image.query.get_or_404(image_id)
    image, error = docker_service.build_image(image)
    if error:
        return jsonify({'msg': error}), 403
    return jsonify({'msg': 'Image built successfully', 'id': image.id}), 201

@docker_bp.route('/start_container/<int:container_id>', methods=['POST'])
@login_required
def start_container(container_id):
    container = Container.query.get_or_404(container_id)
    container, error = docker_service.start_container(container)
    if error:
        return jsonify({'msg': error}), 403
    return jsonify({'msg': 'Container started successfully'}), 201

@docker_bp.route('/stop_container/<int:container_id>', methods=['POST'])
@login_required
def stop_container(container_id):
    container = Container.query.get_or_404(container_id)
    container, error = docker_service.stop_container(container)
    if error:
        return jsonify({'msg': error}), 403
    return jsonify({'msg': 'Container stopped successfully'}), 201

@docker_bp.route('/run_container/<int:image_id>', methods=['POST'])
@login_required
def run_container(image_id):
    image = Image.query.get_or_404(image_id)
    image, error = docker_service.run_container(image)
    if error:
        return jsonify({'msg': error}), 403
    return jsonify({'msg': 'Container started successfully'}), 201

