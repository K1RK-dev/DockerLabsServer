from extensions import db
from models.role import RoleType
from models.user import User

def register_user(username, password, group=None, first_name='', last_name='', middle_name=''):
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return None, "Username already exists"

    new_user = User(username=username)
    new_user.set_password(password)
    new_user.set_role(RoleType.STUDENT)
    new_user.first_name = first_name
    new_user.last_name = last_name
    new_user.middle_name = middle_name
    if group:
        new_user.set_group(group)
    db.session.add(new_user)
    db.session.commit()

    return new_user, None

def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if not user:
        return None, "Incorrect username"
    if not user.check_password(password):
        return None, "Incorrect password"
    return user, None

def get_user_role(user):
    user = User.query.filter_by(username=user.username).first()
    if not user:
        return None, "User not found"
    return user.role.name, ""