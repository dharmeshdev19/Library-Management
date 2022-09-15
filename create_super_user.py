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

def check_username():
	username = input("\nEnter username\n")
	if username:
		return username
	else:
		check_username()

def check_password():
	password = input("\nEnter password\n")
	if password:
		return password
	else:
		check_password()


if __name__ == "__main__":
	username = check_username()
	password = check_password()
	print (username, password)
	register(username, password)
# !! write the function in recursive manner, make sure you add proper validation when taking input from user, if the user does not provide any input data, you should prompt it to ask again from input data.