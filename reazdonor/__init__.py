from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from reazdonor.config import Config

mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(config_class = Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	from reazdonor.users.routes import users
	from reazdonor.main.routes import main
	app.register_blueprint(users)
	app.register_blueprint(main)

	mail.init_app(app)
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)

	with app.app_context():
		db.create_all()

	return app
