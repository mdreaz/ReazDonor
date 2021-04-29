import json

with open('reazconfig.json') as config_file:
	config = json.load(config_file)

class Config:
	SECRET_KEY = config.get('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_USERNAME = config.get('MAIL_USERNAME')
	MAIL_PASSWORD = config.get('MAIL_PASSWORD')
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_DEFAULT_SENDER = 'ReazDonor Contact'
