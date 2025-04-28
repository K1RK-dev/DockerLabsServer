from flask import Flask
from config import Config
from routes.auth import auth_bp
from extensions import *
import pymysql

pymysql.install_as_MySQLdb()
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(auth_bp, url_prefix='/auth')
@app.route("/")
def hello_world():
	return "<h1>Hello, World!</h1>"
