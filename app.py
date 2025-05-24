from flask import Flask
from config import Config
from routes.auth import auth_bp
from routes.groups import groups_bp
from routes.main import main_bp
from routes.docker import docker_bp
from routes.labs import labs_bp
from routes.users import users_bp
from extensions import *
from services.socketio_service import register_socketio_handlers

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
cors.init_app(app, supports_credentials=True, origins=['http://localhost:5173'])
migrate.init_app(app, db)
socketio.init_app(app, cors_allowed_origins="http://localhost:5173")

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(docker_bp, url_prefix='/docker')
app.register_blueprint(labs_bp, url_prefix='/labs')
app.register_blueprint(groups_bp, url_prefix='/groups')
app.register_blueprint(users_bp, url_prefix='/users')

@login_manager.user_loader
def load_user(user_id):
	from models.user import User
	return User.query.get(int(user_id))

register_socketio_handlers(socketio)

if __name__ == '__main__':
	with app.app_context():
		db.create_all()
	socketio.run(app, debug=True)