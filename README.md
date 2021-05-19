# ReazDonor

![Website Logo](reazdonor/static/images/logo.png)

## Introduction
ReazDonor is a web application that allows donors to discover and donate to organizations.

Features include:
* Donor and organization accounts
* Browse organizations
* View organizations that need immediate assistance
* Donate to organizations
* View transaction history

## Installation and Execution
**Note:** this project uses Python 3. In order for the code to execute properly, make sure Python 3 is installed.

Due to the high cost of running web servers, this project is not currently being hosted and must be installed natively to access.

1. Clone repository: `git clone https://github.com/JustinJNEAL/ReazDonor.git`
2. Install dependencies: `python3 -m pip install -r requirements.txt`
3. Edit `reazconfig.json`
	1. Create secret key
		1. Activate Python3 interpreter: `python3`
		2. Run the following code:
		```python3
		import secrets
		key = secrets.token_hex(16)
		print(key)
		```
		3. Copy the output of the `key` variable
		4. Paste value within `""` of `"SECRET_KEY"`
	2. Email features
		1. Type email within `""` of `"MAIL_USERNAME"`
		2. Type email password within `""` of `"MAIL_PASSWORD"`
		3. *If using an email other than GMail, then `config.py` must be edited for your specific mail server*
4. Edit `config.py`
	1. In line `with open('reazconfig.json') as config_file:` replace `reazconfig.json` with the absolute file path
5. Run program: `python3 run.py`
6. Fire up your favorite web browser and paste the output IP. Enjoy!


## Contributors
* [Md Reazul Islam](http://github.com/mdreazul)
* [Justin Neal](http://github.com/JustinJNEAL)
* [Dawit Dagnachew](http://github.com/DawitDa)
* [Asha Vassell]()
* [Kayla Walker](http://github.com/kayverly)
