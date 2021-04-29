from reazdonor.models import Donor, Organization
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SelectField, PasswordField, IntegerField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, InputRequired, ValidationError
from flask_login import current_user

class SignUpForm(FlaskForm):
	member_types = ['Select...', 'Donator', 'Organization']
	states = ['Choose...', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
			'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
			'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
			'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
			'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

	member_type = SelectField('Member type', choices = member_types, validators = [DataRequired()])
	organization_name = StringField('Organization Name', validators = [Length(min = 1, max = 50), Optional()])
	first_name = StringField('First Name', validators = [DataRequired(), Length(min = 1, max = 20)])
	last_name = StringField('Last Name', validators = [DataRequired(), Length(min = 1, max = 20)])
	email = StringField('Email', validators = [DataRequired(), Email(granular_message = True)])
	password = PasswordField('Password', validators = [DataRequired()])
	confirm_password = PasswordField('Re-enter Password', validators = [DataRequired(), EqualTo('password')])
	address = StringField('Address', validators = [DataRequired()])
	address2 = StringField('Address 2', validators = [Optional()])
	city = StringField('City', validators = [DataRequired()])
	state = SelectField('State', choices = states, validators = [DataRequired()])
	zipcode = IntegerField('Zip', validators = [DataRequired()])
	terms = BooleanField('I agree to the Terms & Conditions', validators = [DataRequired()])
	submit = SubmitField('Sign Up')

	def validate_email(self, email):
		donor = Donor.query.filter_by(email = email.data).first()
		org = Organization.query.filter_by(email = email.data).first()

		if (donor or org):
			raise ValidationError('Email already exists. Please try a different email.')

	def validate_member_type(self, member_type):
		if (member_type.data == 'Select...'):
			raise ValidationError('Please select an option.')

	def validate_state(self, state):
		if (state.data == 'Choose...'):
			raise ValidationError('Please select an option')

class LoginForm(FlaskForm):
	email = StringField('Email', validators = [InputRequired(), Email(granular_message = True)], render_kw = {"placeholder": "Email"})
	password = PasswordField('Password', validators = [InputRequired()], render_kw = {"placeholder": "Password"})
	remember_me = BooleanField('Remember me')
	submit = SubmitField('Sign In')

class RequestResetForm(FlaskForm):
	email = StringField('Email', validators = [DataRequired(), Email(granular_message = True)], render_kw = {"placeholder": "Email"})
	submit = SubmitField('Request Password Reset')


	def validate_email(self, email):
		donor = Donor.query.filter_by(email = email.data).first()
		org = Organization.query.filter_by(email = email.data).first()
		if (donor is None and org is None):
			raise ValidationError('Account not found. Please try a different email.')

class PasswordResetForm(FlaskForm):
	password = PasswordField('Password', validators = [DataRequired()], render_kw = {"placeholder": "Password"})
	confirm_password = PasswordField('Re-enter Password', validators = [DataRequired(), EqualTo('password')], render_kw = {"placeholder": "Confirm Password"})
	submit = SubmitField('Reset Password')

class UpdateOrgAccountForm(FlaskForm):
	states = ['Choose...', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
			'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
			'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
			'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
			'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

	logo = FileField('Upload Logo', validators = [FileAllowed(['jpg', 'jpeg', 'png'])])
	first_name = StringField('First Name', validators = [DataRequired(), Length(min = 1, max = 20)])
	last_name = StringField('Last Name', validators = [DataRequired(), Length(min = 1, max = 20)])
	organization_name = StringField('Organization Name', validators = [Length(min = 1, max = 50)])
	phone = IntegerField('Phone Number', validators = [DataRequired()])
	email = StringField('Email', validators = [DataRequired(), Email(granular_message = True)])
	address = StringField('Address', validators = [DataRequired()])
	address2 = StringField('Address 2', validators = [Optional()])
	city = StringField('City', validators = [DataRequired()])
	state = SelectField('State', choices = states, validators = [DataRequired()])
	mission = TextAreaField('Organization Mission', validators = [DataRequired()], render_kw = {"rows": 4})
	impact = TextAreaField('Organization Impact', validators = [DataRequired()], render_kw = {"rows": 4})
	assistance = BooleanField('I need immediate assistance!')
	submit = SubmitField('Update')

	def validate_phone(self, phone):
		if (phone.data != current_user.phone):
			if (len(str(phone.data)) != 10):
				raise ValidationError('Invalid Phone Number.')

	def validate_email(self, email):
		if (email.data != current_user.email):
			donor = Donor.query.filter_by(email = email.data).first()
			org = Organization.query.filter_by(email = email.data).first()

			if (donor or org):
				raise ValidationError('Email already exists. Please try a different email.')

	def validate_state(self, state):
		if (state.data == 'Choose...'):
			raise ValidationError('Please select an option')

class UpdatePasswordForm(FlaskForm):
	old_password = password = PasswordField('Old Password', validators = [InputRequired()])
	password = PasswordField('New Password', validators = [DataRequired()])
	confirm_password = PasswordField('Confirm New Password', validators = [DataRequired(), EqualTo('password')])
	submit = SubmitField('Update')

class UpdateDonorAccountForm(FlaskForm):
	states = ['Choose...', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
			'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
			'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
			'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
			'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

	profile_picture = FileField('Upload Profile Picture', validators = [FileAllowed(['jpg', 'jpeg', 'png'])])
	first_name = StringField('First Name', validators = [DataRequired(), Length(min = 1, max = 20)])
	last_name = StringField('Last Name', validators = [DataRequired(), Length(min = 1, max = 20)])
	email = StringField('Email', validators = [DataRequired(), Email(granular_message = True)])
	city = StringField('City', validators = [DataRequired()])
	state = SelectField('State', choices = states, validators = [DataRequired()])
	description = TextAreaField('Profile Description', render_kw = {"rows": 4})
	submit = SubmitField('Update')

	def validate_email(self, email):
		if (email.data != current_user.email):
			donor = Donor.query.filter_by(email = email.data).first()
			org = Organization.query.filter_by(email = email.data).first()

			if (donor or org):
				raise ValidationError('Email already exists. Please try a different email.')

	def validate_state(self, state):
		if (state.data == 'Choose...'):
			raise ValidationError('Please select an option')