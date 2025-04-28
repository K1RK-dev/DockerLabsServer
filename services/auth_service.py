from extensions import db
from models.user import User
from sqlalchemy.exc import IntegrityError

def register_user(username, password):
    if User.query.filter_by(username=username).first():
        return None, "Username already exists"

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    try:
        db.session.commit()
        return new_user, None
    except IntegrityError as e:
        db.session.rollback()
        return None, "Database error: " + str(e)

def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or user.password != password:
        return None, "Invalid username or password"

    return user, None