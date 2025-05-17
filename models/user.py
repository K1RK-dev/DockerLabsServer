from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password_hash = db.Column(db.String(200), nullable=False)
	is_active = db.Column(db.Boolean, nullable=False, default=True)
	role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
	role = db.relationship('Role', backref='user', lazy=True)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def set_role(self, role):
		from models.role import Role
		db_role = Role.query.filter_by(name=role).first()
		if db_role:
			self.role_id = db_role.id
		else:
			raise ValueError('Role not found')

	def to_dict(self):
		return {
			'id': self.id,
			'username': self.username,
			'is_active': self.is_active,
			'role_id': self.role_id,
		}

	def __repr__(self):
		return f'<User {self.username}>'
