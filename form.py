from wtforms import Form, BooleanField, StringField, PasswordField, validators, FloatField, SelectField, FormField
from models import *

class CategoryForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=25)])

class BookShelfForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=25)])

class BookShelfForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=25)])

class BookEntryForm(Form):
	name = StringField('Name', [validators.required(), validators.Length(min=1, max=25)])
	author = StringField('Author', [validators.required(), validators.Length(min=3, max=25)])
	publisher = StringField('Publisher', [validators.required(), validators.Length(min=3, max=25)])
	price = FloatField('Price', [validators.required()])
	# category = FormField(CategoryForm, [validators.required()])
	# book_shelf = FormField(BookShelfForm, [validators.required()])
	donated_by = StringField('DonatedBy',)