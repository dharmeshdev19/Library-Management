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


username = input("Enter username")
password = input("Enter password")

if username and password:
	register(username, password)
else:
	print("Enter username and password!")