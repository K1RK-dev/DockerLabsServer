from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password_hash = db.Column(db.String(200), nullable=False)
	is_active = db.Column(db.Boolean, nullable=False, default=True)
	first_name = db.Column(db.String(80), nullable=True)
	last_name = db.Column(db.String(80), nullable=True)
	middle_name = db.Column(db.String(80), nullable=True)
	role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
	role = db.relationship('Role', backref='user', lazy=True)
	group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)
	group = db.relationship('Group', backref='user', lazy=True)

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

	def set_group(self, group):
		from models.group import Group
		print(group)
		db_group = Group.query.filter_by(id=group['id']).first()
		if db_group:
			self.group_id = db_group.id
		else:
			raise ValueError('Group not found')

	def set_first_name(self, first_name):
		self.first_name = first_name

	def set_last_name(self, last_name):
		self.last_name = last_name

	def set_middle_name(self, middle_name):
		self.middle_name = middle_name

	def to_dict(self):
		return {
			'id': self.id,
			'username': self.username,
			'is_active': self.is_active,
			'role_id': self.role_id,
			'first_name': self.first_name,
			'last_name': self.last_name,
			'middle_name': self.middle_name,
			'group_id': self.group_id,
		}

	def __repr__(self):
		return f'<User {self.username}>'
