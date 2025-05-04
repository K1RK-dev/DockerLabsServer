from extensions import db
from sqlalchemy import Enum
import enum

class RoleType(enum.Enum):
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(Enum(RoleType), unique=True, nullable=False)

    def __repr__(self):
        return f'<Role {self.name}>'