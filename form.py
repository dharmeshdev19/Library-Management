from wtforms import (
	Form, 
	BooleanField, 
	StringField, 
	PasswordField, 
	validators, 
	FloatField, 
	SelectField, 
	FormField, 
	DateField, 
	IntegerField
)

class UserForm(Form):
	username = StringField('Username', [validators.required(), validators.Length(min=1, max=25)])
	password = PasswordField('Password', [
        validators.required(),
    ])

class CategoryForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=25)])

class BookShelfForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=25)])

class BookShelfForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=25)])

class BookEntryForm(Form):
	name = StringField('Name', [validators.required(), validators.Length(min=1, max=25)])
	book_language = StringField('Book Language', [validators.required(), validators.Length(min=1, max=25)])
	author = StringField('Author',)
	publisher = StringField('Publisher')
	# price = FloatField('Price',)
	# category = FormField(CategoryForm, [validators.required()])
	# book_shelf = FormField(BookShelfForm, [validators.required()])
	donated_by = StringField('DonatedBy',)

class BorrowerDetailForm(Form):
	name = StringField('Name', [validators.required(), validators.Length(min=1, max=25)])
	address = StringField('Address', [validators.required(), validators.Length(min=3, max=25)])
	cell_no = IntegerField('Cell No', [validators.required()])
	email = StringField('Email',)
	issue_date = DateField('Issue Date', format='%Y-%m-%d', validators=(validators.Optional(),))
	return_date = DateField('Return Date', format='%Y-%m-%d', validators=(validators.Optional(),))
	return_status = BooleanField('Return Status')