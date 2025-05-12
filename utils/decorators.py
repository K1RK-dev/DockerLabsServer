from functools import wraps
from flask import jsonify

def roles_required(roles, user):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not user.role:
                return jsonify({'msg': 'Unauthorized'}), 401
            if user.role.name not in roles:
                return jsonify({'msg': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator