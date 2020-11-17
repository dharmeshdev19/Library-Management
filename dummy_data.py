from models import Category, BookShelf, BookStatus
from app import *

#Create category
names = ['Novel', 'Classic', 'Action and Adventure', 'Crime and Detective', 'Drama']
for name in names:
	category = Category(name=name,)
	db.session.add(category)
	db.session.commit()


#Create shelf
names = [
	'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10',
	'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10',
	'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10',
	'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10'
]
for name in names:
	shelf = BookShelf(name=name,)
	db.session.add(shelf)
	db.session.commit()

#Create status
names = ['In Library', 'Issued', 'Lost']
for name in names:
	status = BookStatus(name=name)
	db.session.add(status)
	db.session.commit()