from wtforms_alchemy import ModelForm, ModelFormField
from sqlalchemy import or_, and_, select
from flask import flash, json
from sqlalchemy.ext.declarative import DeclarativeMeta
from models import *

def filter_data(BookEntry, search, category, book_status):
    try:
        book_entry_obj = BookEntry.query.filter(BookEntry.book_code==int(search))
    except:
        book_entry_obj = BookEntry.query.filter(or_(
            BookEntry.name.contains(search),
            BookEntry.author.contains(search),
            BookEntry.publisher.contains(search)
        ))
    if category:
        book_entry_obj = book_entry_obj.filter(BookEntry.category==int(category))

    if book_status:
        book_entry_obj = book_entry_obj.filter(BookEntry.book_status==int(book_status))
    return book_entry_obj

def book_search(BookEntry, search):
    try:
        book_entry_obj = BookEntry.query.filter(BookEntry.book_code==int(search))
    except:
        book_entry_obj = BookEntry.query.filter(or_(
            BookEntry.name.contains(search),
        ))
    return book_entry_obj

def issued_book_search(BookEntry, search):
    try:
        book_entry_obj = BookEntry.query.filter(BookEntry.book_code==int(search))
    except:
        book_entry_obj = BookEntry.query.filter(or_(
            BookEntry.name.contains(search),
        ))
    book_status_obj = BookStatus.query.filter(BookStatus.name=='Issued')
    book_entry_obj = book_entry_obj.filter(BookEntry.book_status==book_status_obj.all()[0].id)
    return book_entry_obj

def flash_errors(form):
    for field, errors in form.errors.items():
        flash(u"Error in the %s field - %s" % (
            field,
            errors
        ))

def book_entry_json(book_entry_obj):
    book_list = []
    for book_entry in book_entry_obj:
        book_list.append({
            'book_code': book_entry.book_code,
            'name': book_entry.name,
            'book_language': book_entry.book_language,
            'author': book_entry.author,
            'publisher': book_entry.publisher,
            'price': book_entry.price,
            'category': book_entry.category,
            'category_name': book_entry.category_name.name,
            'book_shelf': book_entry.book_shelf,
            'shelf_name': book_entry.shelf_name.name,
            'book_status': book_entry.book_status,
            'book_status_name': book_entry.book_status_name.name,
            'donated_by': book_entry.donated_by
            })
    return book_list

def borrower_json(borrower_obj):
    borrower_list = []
    for borrower in borrower_obj:
        borrower_list.append({
            'name': borrower.name,
            'address': borrower.address,
            'cell_no': borrower.cell_no,
            'email': borrower.email,
            'issue_date': borrower.issue_date,
            'return_date': borrower.return_date,
            'return_status': borrower.return_status,
            'book_entry': borrower.book_entry
            })
    return borrower_list

def new_alchemy_encoder():
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)

                # an SQLAlchemy class
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                    fields[field] = obj.__getattribute__(field)
                # a json-encodable dict
                return fields

            return json.JSONEncoder.default(self, obj)

    return AlchemyEncoder