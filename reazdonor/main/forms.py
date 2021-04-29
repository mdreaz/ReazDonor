from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError, Length

class ContactForm(FlaskForm):
	name = StringField(validators = [DataRequired()], render_kw = {"placeholder": "Please enter your name"})
	email = StringField(validators = [DataRequired(), Email(granular_message = True)], render_kw = {"placeholder": "Please enter your email"})
	message = TextAreaField(validators = [DataRequired()], render_kw = {"placeholder": "Please write your message here", "rows": 5})
	submit = SubmitField('Submit')

class DonateForm(FlaskForm):
	card_types = ['Select...', 'MasterCard', 'VISA', 'Discover', 'AMEX']

	dollar_amount = IntegerField('Amount', validators = [DataRequired()], render_kw = {"placeholder": "50"})
	cent_amount = IntegerField(render_kw = {"placeholder": "00"})
	card_type = SelectField('Card Type', choices = card_types, validators = [DataRequired()])
	cardholder = StringField('Cardholder Name', validators = [DataRequired()], render_kw = {"placeholder": "Cardholder Name"})
	card_number = IntegerField('Card Number', validators = [DataRequired()], render_kw = {"placeholder": "Card Number"})
	expiration_month = StringField('Expiration Date (MM/YY)', validators = [DataRequired()], render_kw = {"placeholder": "MM"})
	expiration_year = StringField(validators = [DataRequired()], render_kw = {"placeholder": "YY"})
	cvv = StringField('CVV', validators = [DataRequired(), Length(min = 3, max = 3)], render_kw = {"placeholder": "CVV"})
	billing_zip = IntegerField('Billing ZIP Code', validators = [DataRequired()], render_kw = {"placeholder": "ZIP"})
	submit = SubmitField('Process Donation')

	def validate_card_type(self, card_type):
		if (card_type.data == 'Select...'):
			raise ValidationError('Please select an option.')

	def validate_exp_month(self, expiration_month):
		if (len(expiration_month) != 2 or int(expiration_month) < 1 or int(expiration_month) > 12):
			raise ValidationError('Invalid month.')

	def validate_exp_year(self, expiration_year):
		if (len(expiration_year) != 2):
			raise ValidationError('Invalid year.')