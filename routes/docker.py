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

@docker_bp.route('/get_images', methods=['GET'])
@login_required
@roles_required([RoleType.ADMIN, RoleType.TEACHER], current_user)
def get_images():
    if current_user.role == RoleType.ADMIN:
        images, error = docker_service.get_images(0)
        if error:
            return jsonify({'msg': error}), 403
        return jsonify({'images': images}), 200
    else:
        images, error = docker_service.get_images(current_user.id)
        if error:
            return jsonify({'msg': error}), 403
        images_list = [image.to_dict() for image in images]
        return jsonify({'images': images_list}), 200

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

@docker_bp.route('/delete_dockerfile/<int:dockerfile_id>', methods=['DELETE'])
@login_required
@roles_required([RoleType.ADMIN, RoleType.TEACHER], current_user)
def delete_dockerfile(dockerfile_id):
    dockerfile = Dockerfile.query.get_or_404(dockerfile_id)
    if dockerfile.user_id != current_user.id and current_user.role.name != RoleType.ADMIN:
        return jsonify({'msg': 'You are not authorized to perform this action'}), 403
    else:
        result, error = docker_service.delete_dockerfile(dockerfile)
        if error:
            return jsonify({'msg': error}), 403
        return jsonify({'msg': result}), 200


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

@docker_bp.route('/start_container/<string:container_id>', methods=['POST'])
@login_required
def start_container(container_id):
    container = Container.get_by_id(container_id)
    if container:
        container, error = docker_service.start_container(container)
        if error:
            return jsonify({'msg': error}), 403
        return jsonify({'msg': 'Container started successfully'}), 201
    else:
        return jsonify({'msg': 'Container not found'}), 404

@docker_bp.route('/stop_container/<string:container_id>', methods=['POST'])
@login_required
def stop_container(container_id):
    container = Container.get_by_id(container_id)
    if container:
        container, error = docker_service.stop_container(container)
        if error:
            return jsonify({'msg': error}), 403
        return jsonify({'msg': 'Container stopped successfully'}), 201
    else:
        return jsonify({'msg': 'Container not found'}), 403

@docker_bp.route('/run_container/<string:image_id>', methods=['POST'])
@login_required
def run_container(image_id):
    image = Image.query.get_or_404(image_id)
    container_id, error = docker_service.run_container(image)
    if error:
        return jsonify({'msg': error}), 403
    return jsonify({'msg': 'Container started successfully', "id": container_id}), 201

