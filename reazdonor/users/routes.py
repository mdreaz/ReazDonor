from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from reazdonor import db, bcrypt, mail
from reazdonor.users.forms import SignUpForm, LoginForm, RequestResetForm, PasswordResetForm, UpdateOrgAccountForm, UpdateDonorAccountForm, UpdatePasswordForm
from reazdonor.models import Donor, Organization
from flask_login import login_user, current_user, logout_user
from flask_mail import Message
import secrets
import os
from PIL import Image

users = Blueprint('users', __name__)

@users.route('/login', methods = ['GET', 'POST'])
def login():
	if (current_user.is_authenticated):
		return redirect(url_for('main.home'))
	
	form = LoginForm()

	if (form.validate_on_submit()):
		donor = Donor.query.filter_by(email = form.email.data).first()
		org = Organization.query.filter_by(email = form.email.data).first()

		if (donor and bcrypt.check_password_hash(donor.password, form.password.data)):
			login_user(donor, remember = form.remember_me.data)

			flash("Welcome back!", 'success')
			return redirect(url_for('main.home'))
		elif (org and bcrypt.check_password_hash(org.password, form.password.data)):
			login_user(org, remember = form.remember_me.data)

			flash("Welcome back!", 'success')
			return redirect(url_for('main.home'))
		else:
			flash("Account not found. Please check email and password.", 'danger')

	return render_template('login.html', title = 'Login', form = form)

@users.route('/signup', methods = ['GET', 'POST'])
def signup():
	if (current_user.is_authenticated):
		return redirect(url_for('main.home'))
	
	form = SignUpForm()

	if (form.validate_on_submit()):
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

		if (form.member_type.data == 'Donator'):
			donor = Donor(email = form.email.data, password = hashed_pw, first_name = form.first_name.data, last_name = form.last_name.data, city = form.city.data, state = form.state.data)
			db.session.add(donor)
			db.session.commit()

			flash("Account creation was successful. Please login.", 'success')
			return redirect(url_for('users.login'))
		elif (form.member_type.data == 'Organization'):
			org = Organization(email = form.email.data, password = hashed_pw, organization_name = form.organization_name.data, first_name = form.first_name.data, last_name = form.last_name.data, address = form.address.data, address2 = form.address2.data, city = form.city.data, state = form.state.data)
			db.session.add(org)
			db.session.commit()

			flash("Account creation was successful. Please login.", 'success')
			return redirect(url_for('users.login'))

	return render_template('signup.html', title = 'Sign Up', form = form)

@users.route('/logout')
def logout():
	logout_user()

	return redirect(url_for('main.home'))

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message("Password Reset", sender = 'swe.team6@gmail.com', recipients = [user.email])
	msg.body = f'''Follow this link to reset your password: {url_for('users.reset_token', token = token, _external = True)}
				
Didn't make this request? Feel free to ignore this email.
'''
	mail.send(msg)

@users.route('/reset_password', methods = ['GET', 'POST'])
def request_reset():
	if (current_user.is_authenticated):
		return redirect(url_for('main.home'))

	form = RequestResetForm()

	if (form.validate_on_submit()):
		donor = Donor.query.filter_by(email = form.email.data).first()
		org = Organization.query.filter_by(email = form.email.data).first()

		if (donor is not None):
			send_reset_email(donor)
			flash("Please check your email for a link to reset your password.", 'info')
			return redirect(url_for('users.login'))
		elif (org is not None):
			send_reset_email(org)
			flash("Please check your email for a link to reset your password.", 'info')
			return redirect(url_for('users.login'))

	return render_template('request_reset.html', title = 'Reset Password', form = form)

@users.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_token(token):
	if (current_user.is_authenticated):
		return redirect(url_for('main.home'))

	donor = Donor.verify_reset_token(token)
	org = Organization.verify_reset_token(token)

	form = PasswordResetForm()

	if (donor is None and org is not None):
		if (form.validate_on_submit()):
			hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
			org.password = hashed_pw
			db.session.commit()

			flash("Password has been updated. Please login.", 'success')
			return redirect(url_for('users.login'))
	elif (org is None and donor is not None):
		if (form.validate_on_submit()):
			hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
			donor.password = hashed_pw
			db.session.commit()

			flash("Password has been updated. Please login.", 'success')
			return redirect(url_for('users.login'))
	else:
		flash("Invalid or expired token.", 'warning')
		return redirect(url_for('users.request_reset'))

	return render_template('token_reset.html', title = 'Reset Password', form = form)

def save_image(img):
	hex_name = secrets.token_hex(8)
	_, ext = os.path.splitext(img.filename)
	filename = hex_name + ext
	img_path = os.path.join(current_app.root_path, 'static/images/profiles', filename)
	size = (200, 200)
	im = Image.open(img)
	im.thumbnail(size)
	im.save(img_path)

	return filename

@users.route('/org_cp', methods = ['GET', 'POST'])
def org_cp():
	image = url_for('static', filename = 'images/profiles/' + current_user.logo)

	update_account = UpdateOrgAccountForm()
	update_password = UpdatePasswordForm()

	if (update_account.validate_on_submit()):
		if (update_account.logo.data):
			img_file = save_image(update_account.logo.data)
			current_user.logo = img_file

		current_user.first_name = update_account.first_name.data
		current_user.last_name = update_account.last_name.data
		current_user.organization_name = update_account.organization_name.data
		current_user.phone = update_account.phone.data
		current_user.email = update_account.email.data
		current_user.address = update_account.address.data
		current_user.address2 = update_account.address2.data
		current_user.city = update_account.city.data
		current_user.state = update_account.state.data
		current_user.mission = update_account.mission.data
		current_user.impact = update_account.impact.data
		current_user.assistance = update_account.assistance.data
		db.session.commit()

		flash("Account successfully updated.", 'success')
		return redirect(url_for('users.org_cp'))
	elif (request.method == 'GET'):
		update_account.first_name.data = current_user.first_name
		update_account.last_name.data = current_user.last_name
		update_account.organization_name.data = current_user.organization_name
		update_account.phone.data = current_user.phone
		update_account.email.data = current_user.email
		update_account.address.data = current_user.address
		update_account.address2.data = current_user.address2
		update_account.city.data = current_user.city
		update_account.state.data = current_user.state
		update_account.mission.data = current_user.mission
		update_account.impact.data = current_user.impact
		update_account.assistance.data = current_user.impact

	if (update_password.validate_on_submit()):
		if (bcrypt.check_password_hash(current_user.password, update_password.old_password.data)):
			hashed_pw = bcrypt.generate_password_hash(update_password.password.data).decode('utf-8')

			current_user.password = hashed_pw
			db.session.commit()

			flash("Password successfully updated.", 'success')
			return redirect(url_for('users.org_cp'))
		else:
			flash("Unable to update password.", 'danger')
			return redirect(url_for('users.org_cp'))

	return render_template('org_cp.html', title = 'Control Panel', account = update_account, password = update_password, image = image)

@users.route('/donor_cp', methods = ['GET', 'POST'])
def donor_cp():
	image = url_for('static', filename = 'images/profiles/' + current_user.profile_picture)

	update_account = UpdateDonorAccountForm()
	update_password = UpdatePasswordForm()

	if (update_account.validate_on_submit()):
		if (update_account.profile_picture.data):
			img_file = save_image(update_account.profile_picture.data)
			current_user.profile_picture = img_file

		current_user.first_name = update_account.first_name.data
		current_user.last_name = update_account.last_name.data
		current_user.email = update_account.email.data
		current_user.city = update_account.city.data
		current_user.state = update_account.state.data
		current_user.description = update_account.description.data
		db.session.commit()

		flash("Account successfully updated.", 'success')
		return redirect(url_for('users.donor_cp'))
	elif (request.method == 'GET'):
		update_account.first_name.data = current_user.first_name
		update_account.last_name.data = current_user.last_name
		update_account.email.data = current_user.email
		update_account.city.data = current_user.city
		update_account.state.data = current_user.state
		update_account.description.data = current_user.description

	if (update_password.validate_on_submit()):
		if (bcrypt.check_password_hash(current_user.password, update_password.old_password.data)):
			hashed_pw = bcrypt.generate_password_hash(update_password.password.data).decode('utf-8')

			current_user.password = hashed_pw
			db.session.commit()

			flash("Password successfully updated.", 'success')
			return redirect(url_for('users.donor_cp'))
		else:
			flash("Unable to update password.", 'danger')
			return redirect(url_for('users.donor_cp'))

	return render_template('donor_cp.html', title = 'Control Panel', account = update_account, password = update_password, image = image)

@users.route('/load_account')
def load_account():
	org = Organization.query.filter_by(email = current_user.email).first()
	donor = Donor.query.filter_by(email = current_user.email).first()

	if (donor is not None and org is None):
		return redirect(url_for('users.donor_cp'))
	elif (org is not None and donor is None):
		return redirect(url_for('users.org_cp'))
	
	return redirect(url_for('main.home'))