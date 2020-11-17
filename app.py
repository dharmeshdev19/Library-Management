from flask import Flask, flash, request, render_template, redirect, url_for, session, json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.session import Session
from flask_bootstrap import Bootstrap
import yaml
from flask_datepicker import datepicker
import datetime
# from utils import *
from form import *
import flask_whooshalchemy
import flask.ext.whooshalchemy

from flask import Blueprint
# from flask_paginate import Pagination, get_page_parameter
from flask_paginate import Pagination, get_page_args
from sqlalchemy import or_, and_, select


app = Flask(__name__)
app.config.from_object(__name__)
sess = Session(app)

db = yaml.load(open('db.yaml'))
database = db.get('database', None)
mysql_host = db.get('mysql_host', None)
mysql_user = db.get('mysql_user', None)
mysql_password = db.get('mysql_password', None)
mysql_db_name = db.get('mysql_db_name', None)
port = db.get('port', None)
app.config['SQLALCHEMY_DATABASE_URI'] = database+'://'+mysql_user+':'+mysql_password+'@'+mysql_host+':'+port+'/'+mysql_db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['WHOOSH_BASE'] = 'whoosh'
app.config['WHOOSH_BASE'] = 'path/to/whoosh/base'

db = SQLAlchemy(app)
from models import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def homepage():
    user_id = session.get('id', None)
    if user_id:
        return render_template("home.html")
    else:
        flash('you need to login!', 'danger')
        return redirect(url_for('login'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if not session.get('id'):
        if request.method == 'POST':
            data = request.form
            username = data.get('username', None)
            password = data.get('password', None)
            user = User.query.filter_by(username=username).first()
            try:
                if not user or not check_password_hash(user.password, password):
                    flash('Invalid username and password!')
                    return render_template("login.html")
                else:
                    session['id'] = user.id
                return redirect('http://127.0.0.1:5000/')
            except:
                flash('User not found!', 'danger')
                return render_template("login.html")
        else:
            return render_template("login.html")
    else:
        flash('you already login', 'danger')
        return redirect('http://127.0.0.1:5000/')
            
@app.route('/logout/', methods=['GET'])
def logout():
    session.clear()
    flash('you logout successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/book_entry/', methods=['GET', 'POST'])
def book_entry():
    context={}
    if session.get('id'):
        category_list = Category.query.all()
        shelf_list = BookShelf.query.all()
        context['category_list'] = category_list
        context['shelf_list'] = shelf_list
        if request.method == 'POST':
            data = request.form
            name = data.get('name', None)
            author = data.get('author', None)
            publisher = data.get('publisher', None)
            price = data.get('price', None)
            category = data.get('category', None)
            book_shelf_number = data.get('book_shelf_number', None)
            donated_by = data.get('donated_by', None)
            form = BookEntryForm(data)
            if form.validate():
                book_entry = BookEntry(name=name, author=author, publisher=publisher, price=price,
                    category=int(category), book_shelf=int(book_shelf_number), book_status=1, donated_by=donated_by)
                db.session.add(book_entry)
                db.session.commit()
                context['book_data'] = book_entry
                return render_template("book_entry_detail.html", data=context)
            else:
                flash("missing required fields", 'danger')
                return render_template("book_entry.html", data=context)
        else:
            return render_template("book_entry.html", data=context)
    else:
        flash('you need to login!', 'danger')
        return redirect(url_for('login'))

def get_users(book_entry_obj, offset=0, per_page=2):
    return book_entry_obj[offset: offset + per_page]

@app.route('/search/', methods=['GET', 'POST'])
def search():
    context={}
    category_list = Category.query.all()
    book_status_list = BookStatus.query.all()
    context['category_list'] = category_list
    context['book_status_list'] = book_status_list
    if request.method == 'POST':
        data = request.form
        search = data.get('search', None)
        category = data.get('category', None)
        book_status = data.get('book_status', None)
        issued_date = data.get('issued_date', None)
        return_date = data.get('return_date', None)
        if search:
            print(search)
            page = 1
            session['data'] = data
            try:
                book_entry_obj = BookEntry.query.filter(BookEntry.book_code==int(search))
            except:
                book_entry_obj = BookEntry.query.filter(or_(
                    BookEntry.book_code.contains(search),
                    BookEntry.name.contains(search),
                    BookEntry.author.contains(search),
                    BookEntry.publisher.contains(search)
                ))
            # if category:
            #     for each in book_entry_obj.all():
            #         if each.category != int(category):
            #             print(book_entry_obj.all())
            #             book_entry_obj.all().remove(each)
            #             print(book_entry_obj.all())

            # if book_status == '2':
            #     issued_date , return_date
            #     for each in book_entry_obj.all():
            #         if each.book_status != int(book_status):
            #             book_entry_obj.all().remove(each)
            # elif book_status:
            #     for each in book_entry_obj.all():
            #         if each.book_status != int(book_status):
            #             book_entry_obj.all().remove(each)
            context['book_entry_obj'] = book_entry_obj.paginate(page, 10, False)
    page = request.args.get('page')
    data = session.get('data')
    if page and data:
        search = session.get('data').get('search')
        category = session.get('data').get('category')
        book_status = session.get('data').get('book_status')
        try:
            book_entry_obj = BookEntry.query.filter(BookEntry.book_code==int(search))
        except:
            book_entry_obj = BookEntry.query.filter(or_(
                BookEntry.name.contains(search),
                BookEntry.author.contains(search),
                BookEntry.publisher.contains(search)
            ))
        # if category:
        #     for each in book_entry_obj_list:
        #         if each.category != int(category):
        #             book_entry_obj_list.remove(each)

        # if book_status == '2':
        #     issued_date , return_date
        #     for each in book_entry_obj_list:
        #         if each.book_status != int(book_status):
        #             book_entry_obj_list.remove(each)
        # elif book_status:
        #     for each in book_entry_obj_list:
        #         if each.book_status != int(book_status):
        #             book_entry_obj.remove(each)
        context['book_entry_obj'] = book_entry_obj.paginate(int(page), 10, False)
    return render_template("search.html", data=context)

# @app.route('/book_entry_detail/', methods=['GET', 'POST'])
# def book_entry_detail():
#     if session.get('id'):
#         if request.method == 'POST':
            
#             return render_template("book_entry_detail.html")
#         else:
#             return render_template("book_entry_detail.html")
#     else:
#         flash('you need to login!', 'danger')
#         return redirect(url_for('login'))

@app.route('/book_issue/', methods=['GET'])
def book_issue():
    return render_template("book_issue.html")

@app.route('/book_return/', methods=['GET'])
def book_return():
    return render_template("book_return.html")

@app.route('/overdued/', methods=['GET'])
def overdued():
    return render_template("overdued.html")

@app.route('/donation_list/', methods=['GET'])
def donation_list():
    return render_template("donation_list.html")

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)
    bootstrap = Bootstrap(app)
    datepicker = datepicker(app)
    app.debug = True
    app.run()
