from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import *

def register(username, password):
	try:
		password = generate_password_hash(password, method='sha256')
		user = User(username=username, password=password)
		db.session.add(user)
		db.session.commit()
		print("user created successfully")
	except:
		print("something wrong, please contact admin!")


username = input("Enter username") # the input is asked on same line, make sure it ask input data on next line
password = input("Enter password") # the input is asked on same line, make sure it ask input data on next line

if username and password:
	register(username, password)
else:
	print("Enter username and password!")

# !! write the function in recursive manner, make sure you add proper validation when taking input from user, if the user does not provide any input data, you should prompt it to ask again from input data.