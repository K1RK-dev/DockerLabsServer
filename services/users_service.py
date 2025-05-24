from models.role import Role, RoleType
from models.user import User

def get_students():
    try:
        student_role = Role.query.filter_by(name=RoleType.STUDENT).first()
        users = User.query.filter_by(role_id=student_role.id).all()
        if not users:
            return None, "No users found"
        return users, None
    except Exception as e:
        return None, f"Error getting users: {e}"