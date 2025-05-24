from flask import Blueprint, jsonify
import services.groups_service as groups_service

groups_bp = Blueprint("groups", __name__)

@groups_bp.route('/get_groups', methods=['GET'])
def get_groups():
    groups, error = groups_service.get_groups()
    if error:
        return jsonify({'error': error}), 400
    groups_list = [group.to_dict() for group in groups]
    return jsonify({'groups': groups_list}), 200