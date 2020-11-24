from flask import Flask, flash, request, render_template, redirect, url_for, session, json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.session import Session
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from utils import *
from form import *
import db_config
import datetime
from flask import Flask, make_response, send_from_directory, send_file, Response
from openpyxl import load_workbook
import io
import xlwt

app = Flask(__name__)
app.config.from_object(__name__)
sess = Session(app)

db = db_config.database_config(app)[0]
app = db_config.database_config(app)[1]
db = SQLAlchemy(app)
from models import *

# app = Flask(__name__)

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
            # !! very poor validation code, please add proper standard way of validating post data.
            username = data.get('username', None)
            password = data.get('password', None)
            
            form = UserForm(data)
            if form.validate():
                user = User.query.filter_by(username=username).first() # !! never perform query on direct data from user.
                try:
                    if not user or not check_password_hash(user.password, password):
                        flash('Invalid username and password!')
                        return render_template("login.html")
                    else:
                        session['id'] = user.id
                    return redirect('/') 
                except:
                    flash('User not found!', 'danger')
                    return render_template("login.html")
            else:
                flash_errors(form)
                return render_template("login.html")
        else:
            return render_template("login.html")
    else:
        flash('you already login', 'danger')
        return redirect('/') 

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
            book_language = data.get('book_language', None)
            author = data.get('author', None)
            publisher = data.get('publisher', None)
            price = data.get('price', None)
            if not price:
                price = 0
            category = data.get('category', None)
            if not category:
                flash('category required field!', 'danger')
            book_shelf_number = data.get('book_shelf_number', None)
            if not book_shelf_number:
                flash('book shelf required field!', 'danger')
            donated_by = data.get('donated_by', None)
            form = BookEntryForm(data)
            if form.validate():
                book_entry = BookEntry(name=name, book_language=book_language, author=author, publisher=publisher, price=price,
                    category=int(category), book_shelf=int(book_shelf_number), book_status=1, donated_by=donated_by)
                db.session.add(book_entry)
                db.session.commit()
                context['book_data'] = book_entry
                return render_template("book_entry_detail.html", data=context)
            else:
                flash_errors(form)
                return render_template("book_entry.html", data=context)
        else:
            return render_template("book_entry.html", data=context)
    else:
        flash('you need to login!', 'danger')
        return redirect(url_for('login'))

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
        if search:
            page = 1
            session['data'] = data
            book_entry_obj = filter_data(BookEntry, search, category, book_status)
            context['book_entry_obj'] = book_entry_obj.paginate(page, 5, False)
    page = request.args.get('page')
    data = session.get('data')
    if page and data:
        search = session.get('data').get('search')
        category = session.get('data').get('category')
        book_status = session.get('data').get('book_status')
        book_entry_obj = filter_data(BookEntry, search, category, book_status)
        context['book_entry_obj'] = book_entry_obj.paginate(int(page), 5, False)
    return render_template("search.html", data=context)

@app.route('/book_edit/', methods=['GET', 'POST'])
def book_edit():
    if session.get('id'):
        context = {}
        category_list = Category.query.all()
        shelf_list = BookShelf.query.all()
        context['shelf_list'] = shelf_list
        context['category_list'] = category_list
        book_code = request.args.get('book_code')
        if request.method == 'POST':
            data = request.form
            json_data = dict(data)
            book_code = json_data.pop('book_code')
            book_entry = BookEntry.query.filter_by(book_code=book_code).update(json_data)
            db.session.commit()
            book_entry = BookEntry.query.filter_by(book_code=book_code).first()
            context['book_data'] = book_entry
            return render_template("book_update.html", data=context)
        else:
            book_entry_obj = BookEntry.query.filter_by(book_code=book_code).first()
            shelf_name = BookShelf.query.filter_by(id=book_entry_obj.book_shelf).first().name
            category_name = Category.query.filter_by(id=book_entry_obj.category).first().name
            context['category_name'] = category_name
            context['shelf_name'] = shelf_name
            context['book_data'] = book_entry_obj
            return render_template("book_edit.html", data=context)
    else:
        flash('you need to login!', 'danger')
        return redirect(url_for('login'))

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

@app.route('/book_search/', methods=['GET', 'POST'])
def book_search():
    context = {}
    if request.method == 'POST':
        data = request.form
        search = data.get('search', None)
        if search:
            book_entry_list = book_search(BookEntry, search)
            context['book_entry_list'] = book_entry_list
    return render_template("book_issue.html", data=context)

@app.route('/book_issue/', methods=['GET', 'POST'])
def book_issue():
    context = {}
    if request.method == 'POST':
        data = request.form
        search = data.get('search', None)
        if search:
            book_entry_list = book_search(BookEntry, search)
            context['book_entry_list'] = book_entry_list
        else:
            form = BorrowerDetailForm(data)
            if form.validate():
                name = data.get('name', None)
                address = data.get('address', None)
                cell_no = data.get('cell_no', None)
                email = data.get('email', None)
                issue_date = data.get('issue_date', None)
                return_date = data.get('return_date', None)
                book_entry = data.get('book_code')
                borrow_obj = BorrowerDetail(name=name, address=address, cell_no=int(cell_no), email=email,
                    issue_date=issue_date, return_date=return_date, return_status=False, book_entry=int(book_entry))
                db.session.add(borrow_obj)
                db.session.commit()
                return redirect('/')
            else:
                flash_errors(form)
        return render_template("book_issue.html", data=context)
    book_code = request.args.get('book_code')
    book_entry_obj = BookEntry.query.filter_by(book_code=book_code).first()
    issue_date = datetime.date.today()
    return_date = datetime.date.today() + datetime.timedelta(days=10)
    context['issue_date'] = issue_date
    context['return_date'] = return_date
    context['book_entry_obj'] = book_entry_obj
    return render_template("book_issue.html", data=context)

@app.route('/download_book_list/', methods=['GET'])
def download_book_list():
    data = session.get('data')
    if data:
        search = session.get('data').get('search')
        category = session.get('data').get('category')
        book_status = session.get('data').get('book_status')
        book_list = filter_data(BookEntry, search, category, book_status)
        if book_list:
            #output in bytes
            output = io.BytesIO()
            #create WorkBook object
            workbook = xlwt.Workbook()

                #add a sheet
            sh = workbook.add_sheet('Book List')
            #add headers
            sh.write(0, 0, 'Book Code')
            sh.write(0, 1, 'Name')
            sh.write(0, 2, 'Book Language')
            sh.write(0, 3, 'Author')
            sh.write(0, 4, 'Publisher')
            sh.write(0, 5, 'Price')
            sh.write(0, 6, 'Category')
            sh.write(0, 7, 'Shelf')
            sh.write(0, 8, 'Status')
            sh.write(0, 9, 'Donated By')
            sh.write(0, 10, 'Return Date')
            sh.write(0, 11, 'Overdue')
            
            idx = 0
            for book in book_list.all():
                sh.write(idx+1, 0, str(book.book_code))
                sh.write(idx+1, 1, book.name)
                sh.write(idx+1, 2, book.book_language)
                sh.write(idx+1, 3, book.author)
                sh.write(idx+1, 4, book.publisher)
                sh.write(idx+1, 5, str(book.price))
                sh.write(idx+1, 6, str(book.category_name))
                sh.write(idx+1, 7, str(book.shelf_name))
                sh.write(idx+1, 8, str(book.book_status))
                sh.write(idx+1, 9, book.donated_by)
                sh.write(idx+1, 10, '')
                sh.write(idx+1, 11, '')
                idx += 1
            workbook.save(output)
            output.seek(0)
            return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=book_list.xls"})
        else:
            flash('book not found!', 'danger')
            return render_template("search.html")
    else:
        flash('book not found!', 'danger')
        return render_template("search.html")

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
    app.config['SESSION_TYPE'] = 'filesystem' # !! save session in database instead of filesystem
    app.config['TEMPLATES_AUTO_RELOAD'] = True # to auto-reload templates changes.
    sess.init_app(app)
    bootstrap = Bootstrap(app)
    datepicker = datepicker(app)
    app.debug = True
    app.run()
