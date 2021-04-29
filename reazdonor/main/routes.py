from reazdonor.models import Donor, Organization, Donations
from flask import Blueprint, render_template, url_for, flash, redirect, request
from reazdonor import mail, db
from flask_mail import Message
from reazdonor.main.forms import ContactForm, DonateForm
from flask_login import current_user
import secrets

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
	data = Organization.query.filter_by(assistance = True).all()
	return render_template('home.html', data=data)

@main.route('/about')
def about():
	return render_template('about.html', title = 'About')

@main.route('/how')
def how():
	return render_template('how.html', title = 'How')

@main.route('/how/signup')
def how_signup():
	return render_template('how_signup.html', title = 'How')

@main.route('/how/login')
def how_login():
	return render_template('how_login.html', title = 'How')

@main.route('/how/search')
def how_search():
	return render_template('how_search.html', title = 'How')

@main.route('/how/donate')
def how_donate():
	return render_template('how_donate.html', title = 'How')

@main.route('/contact', methods = ['GET', 'POST', 'DELETE'])
def contact():
	form = ContactForm()

	if (form.validate_on_submit()):
		body = form.message.data
		email = form.email.data
		Name = form.name.data

		msg = Message(
					'Hello',
					sender = "swe.team6@gmail.com",
					recipients = ['swe.team6@gmail.com']
					)
		msg.body = 'Name: ' + Name + '\nEmail: ' + email + '\n\nMessage: ' + body

		mail.send(msg)
		flash("Your message has been recieved. We will get back to you soon.", 'info')
		return redirect(url_for('main.contact'))

	return render_template('contact.html', title = 'Contact', form = form)

@main.route('/team')
def team():
	return render_template('team.html', title = 'Team')

def send_donation_email(donor, org, amount):
	msg_donor = Message("Donation Reciept", sender = 'swe.team6@gmail.com', recipients = [donor.email])
	msg_org = Message("Donation Recieved", sender = 'swe.team6@gmail', recipients = [org.email])

	msg_donor.body = f'''Hey {donor.first_name} {donor.last_name},

Thanks for donating to {org.organization_name}! They appreciate it.

This is your reciept for your transaction of {amount}
'''
	msg_org.body = f'''Good news {org.organization_name},

You just recieved a donation of {amount}! Thank you for using our site.
'''

	mail.send(msg_donor)
	mail.send(msg_org)

@main.route('/donation_complete')
def donation_complete():
	return render_template('donation_complete.html', title = 'Thank you')

@main.route('/donate/<string:org_id>', methods = ['GET', 'POST'])
def donate(org_id):
	form = DonateForm()

	donor = Donor.query.filter_by(email = current_user.email).first()
	org = Organization.query.get(org_id)

	if (donor is None):
			flash("Please create a donor account to make donations", 'danger')

			return redirect(url_for('main.search'))

	if (form.validate_on_submit()):
		cent = str(form.cent_amount.data)
		if (cent == "" or cent == "0"):
			cent = "00"

		str_amount = "$" + str(form.dollar_amount.data) + "." + cent
		donation = Donations(id = secrets.token_hex(8), amount = str_amount, donor_id = donor.id, org_id = org.id)
		db.session.add(donation)
		db.session.commit()

		send_donation_email(donor, org, str_amount)
		return redirect(url_for('main.donation_complete'))

	return render_template('donate.html', title = 'Donate', form = form)

@main.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        search_string = request.form['orgns']
        
        data = Organization.query.filter(Organization.organization_name.like('%' + search_string + '%')).all()
        # all in the search box will return all the tuples
        if len(data) == 0 and search_string == 'all': 
            data = Organization.query.all()
        return render_template('search.html', data = data)
    return render_template('search.html', title = 'Search For Orgs')

@main.route('/organization/<string:org_id>')
def organization(org_id):
	org = Organization.query.get_or_404(org_id)

	return render_template('org_home.html', title = org.organization_name, org = org)
