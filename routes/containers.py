from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from extensions import db
from models import Container, Lab
import docker

containers_bp = Blueprint('containers', __name__, url_prefix='/containers')
client = docker.from_env()

@containers_bp.route('/create_container', methods=['POST'])
@login_required
def create_container():
    data = request.get_json()
    lab_id = data.get('lab_id')
    lab = Lab.query.get_or_404(lab_id)
    image_id = lab.image.image_id
    try:
        container = client.containers.run(image_id, detach=True)
    except Exception as e:
        return jsonify({'msg': f'Error creating container: {str(e)}'}), 500

    new_container = Container(container_id=container.id, lab_id=lab_id, user_id=current_user.id)
    db.session.add(new_container)
    db.session.commit()
    return jsonify({'msg': 'Container created successfully', 'container_id': container.id}), 201

@containers_bp.route('/delete_container/<string:container_id>', methods=['DELETE'])
@login_required
def delete_container(container_id):
    container = Container.getById(container_id)
    if container:
        if container.student_id != current_user.id:
            return jsonify({'msg': 'Unauthorized'}), 403
        try:
            container = client.containers.get(container.container_id)
            container.stop()
            container.remove()
        except Exception as e:
            return jsonify({'msg': f'Error stopping/removing container: {str(e)}'}), 500

        db.session.delete(container)
        db.session.commit()
        return jsonify({'msg': 'Container deleted successfully'}), 200
    else:
        return jsonify({'msg': 'Container not found'}), 404