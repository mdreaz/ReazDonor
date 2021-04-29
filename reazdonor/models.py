from flask import current_app
from reazdonor import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import secrets

@login_manager.user_loader
def load_user(id):
	donor = Donor.query.get(id)
	org = Organization.query.get(id)

	if (org):
		return org
	elif (donor):
		return donor
	
	return False

class Donor(db.Model, UserMixin):
	id = db.Column(db.String(32), primary_key = True, default = secrets.token_hex(16))
	email = db.Column(db.String(120), unique = True, nullable = False)
	password = db.Column(db.String(60), nullable = False)
	first_name = db.Column(db.String(20), nullable = False)
	last_name = db.Column(db.String(20), nullable = False)
	profile_picture = db.Column(db.String(20), nullable = False, default = 'default.png')
	city = db.Column(db.String(20), nullable = False)
	state = db.Column(db.String(2), nullable = False)
	description = db.Column(db.Text)
	transaction = db.relationship('Donations', backref = 'donor_txn', lazy = True)

	def get_reset_token(self, expires = 900):
		s = Serializer(current_app.config['SECRET_KEY'], expires)

		return s.dumps({'did': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			did = s.loads(token)['did']
		except:
			return None

		return Donor.query.get(did)

	def __repr__(self):
		return f"Donor('{self.id}', '{self.email}', '{self.first_name} {self.last_name}', '{self.city}', '{self.state}')"

class Organization(db.Model, UserMixin):
	id = db.Column(db.String(32), primary_key = True, default = secrets.token_hex(16))
	email = db.Column(db.String(120), unique = True, nullable = False)
	password = db.Column(db.String(60), nullable = False)
	organization_name = db.Column(db.String(50), nullable = False)
	first_name = db.Column(db.String(20), nullable = False)
	last_name = db.Column(db.String(20), nullable = False)
	address = db.Column(db.String(120), nullable = False)
	address2 = db.Column(db.String(120))
	city = db.Column(db.String(20), nullable = False)
	state = db.Column(db.String(2), nullable = False)
	phone = db.Column(db.String(10), nullable = False, default = '1235551234')
	logo = db.Column(db.String(20), nullable = False, default = 'default.png')
	mission = db.Column(db.Text)
	impact = db.Column(db.Text)
	assistance = db.Column(db.Boolean, nullable = False, default = False)
	transaction = db.relationship('Donations', backref = 'org_txn', lazy = True)

	def get_reset_token(self, expires = 900):
		s = Serializer(current_app.config['SECRET_KEY'], expires)

		return s.dumps({'oid': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			oid = s.loads(token)['oid']
		except:
			return None

		return Organization.query.get(oid)

	def __repr__(self):
		return f"Organization('{self.id}', '{self.email}', '{self.organization_name}', '{self.city}', '{self.state}', '{self.phone}')"

class Donations(db.Model):
	id = db.Column(db.String(16), primary_key = True)
	amount = db.Column(db.String(15), nullable = False)
	date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
	donor_id = db.Column(db.String(32), db.ForeignKey('donor.id'), nullable = False)
	org_id = db.Column(db.String(32), db.ForeignKey('organization.id'), nullable = False)
	
	def __repr__(self):
		return f"Donations('{self.id}', '{self.amount}', 'From: {self.donor_id}', '{self.date}', 'To: {self.org_id}')"