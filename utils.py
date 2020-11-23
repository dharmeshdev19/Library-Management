from wtforms_alchemy import ModelForm, ModelFormField
from sqlalchemy import or_, and_, select
from flask import flash

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

def flash_errors(form):
    for field, errors in form.errors.items():
        flash(u"Error in the %s field - %s" % (
            field,
            errors
        ))