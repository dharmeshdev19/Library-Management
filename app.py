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
from flask import Flask, make_response, send_from_directory, send_file, Response, jsonify
from openpyxl import load_workbook
import io
import xlwt
from sqlalchemy import or_, and_, select
from flask_babel import Babel
from flask_babel import format_datetime
from flask_util_js import FlaskUtilJs
from sqlalchemy import cast, DATE


app = Flask(__name__)
app.config.from_object(__name__)
sess = Session(app)

db = db_config.database_config(app)[0]
app = db_config.database_config(app)[1]
db = SQLAlchemy(app)
from models import *



@app.route('/', methods=['GET', 'POST'])
def homepage():
    user_id = session.get('id', None)
    if user_id:
        username = User.query.filter_by(id=user_id).first().username.title()
        return render_template("home.html", data={'username': username})
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


@app.route('/book_search/', methods=['POST'])
def book_search():
    book_list = []
    if request.method == 'POST':
        search = request.get_json()
        if search:
            try:
                book_entry_obj = BookEntry.query.filter(BookEntry.book_code==int(search))
                book_list = book_entry_json(book_entry_obj)
            except:
                book_entry_obj = BookEntry.query.filter(or_(
                    BookEntry.name.contains(search),
                ))
                book_list = book_entry_json(book_entry_obj)
        return json.dumps(book_list, cls=new_alchemy_encoder(), check_circular=False)


@app.route('/search_user/', methods=['POST'])
def search_user():
    book_list = []
    if request.method == 'POST':
        borrower_name = request.get_json()
        if borrower_name:
            try:
                borrower_detail_obj = BorrowerDetail.query.filter_by(name=borrower_name)
                borrower_list = borrower_json(borrower_detail_obj)
            except:
                borrower_detail_obj = []
                borrower_list = borrower_json(borrower_detail_obj)
        return json.dumps(borrower_list, cls=new_alchemy_encoder(), check_circular=False)


@app.route('/book_issued_list/', methods=['GET', 'POST'])
def book_issued_list():
    book_list = []
    context = {}
    # username = request.get_json()
    username = 'Dharmesh Deo'
    context['username'] = username
    return render_template("book_issued_list.html", data=context)


@app.route('/book_issue/', methods=['GET', 'POST'])
def book_issue():
    context = {}
    if request.method == 'POST':
        data = request.form.copy()
        search = data.get('search', None)
        if search:
            book_entry_list = book_search(BookEntry, search)
            context['book_entry_list'] = book_entry_list
        else:
            data['issue_date'] = data['issue_date'].split()[0]
            data['return_date'] = data['return_date'].split()[0]
            form = BorrowerDetailForm(data)
            if form.validate():
                name = data.get('name', None)
                address = data.get('address', None)
                mobile_no = data.get('mobile_no', None)
                email = data.get('email', None)
                issue_date = data.get('issue_date', None)
                return_date = data.get('return_date', None)
                book_entry = data.get('book_code')
                borrow_obj = BorrowerDetail(name=name, address=address, mobile_no=int(mobile_no), email=email,
                    issue_date=issue_date, return_date=return_date, return_status=False, book_entry=int(book_entry))
                db.session.add(borrow_obj)
                db.session.commit()
                book_entry = BookEntry.query.filter_by(book_code=int(book_entry)).first()
                book_entry.book_status = BookStatus.query.filter_by(name='Issued').first().id
                db.session.commit()
                return redirect('/')
            else:
                flash_errors(form)
        return render_template("book_issue.html", data=context)
    book_code = request.args.get('book_code')
    book_entry_obj = BookEntry.query.filter_by(book_code=book_code).first()
    issue_date = datetime.date.today()
    return_date = datetime.date.today() + datetime.timedelta(days=10)
    context['issue_date'] = str(issue_date)+' ('+issue_date.strftime('%d %b %y')+')'
    context['return_date'] = str(return_date)+' ('+return_date.strftime('%d %b %y')+')'
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
            sh.write(0, 1, 'Book Name')
            sh.write(0, 2, 'Book Language')
            sh.write(0, 3, 'Book Author')
            sh.write(0, 4, 'Book Publisher')
            sh.write(0, 5, 'Price')
            sh.write(0, 6, 'Category')
            sh.write(0, 7, 'Shelf')
            sh.write(0, 8, 'Book Status in Library')
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
                sh.write(idx+1, 6, str(book.category_name.name))
                sh.write(idx+1, 7, str(book.shelf_name.name))
                sh.write(idx+1, 8, str(book.book_status_name.name))
                sh.write(idx+1, 9, book.donated_by)
                try:
                    bor_detail = BorrowerDetail.query.filter(BorrowerDetail.book_entry==book.book_code).all()
                    if bor_detail:
                        if bor_detail[0].return_date:
                            sh.write(idx+1, 10, str(bor_detail[0].return_date))
                        if bor_detail[0].return_date < datetime.date.today():
                            sh.write(idx+1, 11, str(bor_detail[0].return_date))
                except:
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


# @app.template_filter('issue_status_filter')
# def issue_status_filter(s):
#     return s


@app.route('/book_return/', methods=['GET', 'POST'])
def book_return():
    context = {}
    if request.method == 'POST':
        data = request.form
        search = request.json
        if search:
            book_entry_list = issued_book_search(BookEntry, BookStatus, search)
            book_entry_list = book_entry_json(book_entry_list)
            return json.dumps(book_entry_list, cls=new_alchemy_encoder(), check_circular=False)
        else:
            form = BorrowerDetailForm(data)
            if form.validate():
                json_data = dict(data)
                json_data['return_status'] = True
                book_code = json_data.pop('book_code')
                book_shelf = json_data.pop('book_shelf')
                if book_shelf:
                    book_entry = BorrowerDetail.query.filter_by(book_entry=book_code).update(json_data)
                    db.session.commit()
                
                    book_status_obj = BookStatus.query.filter_by(name='In Library').first()
                    book_entry_obj = BookEntry.query.filter_by(book_code=book_code).first()
                    book_entry_obj.book_status = book_status_obj.id
                    book_entry_obj.book_shelf = int(book_shelf)
                    db.session.commit()
                else:
                    flash('Shelf id not found!', 'danger')
                    return redirect(url_for('book_return', book_code=book_code))
                return redirect('/')
            else:
                flash_errors(form)
        return render_template("book_return.html", data=context)
    book_code = request.args.get('book_code')
    if book_code:
        book_entry_obj = BookEntry.query.filter_by(book_code=book_code).first()
        borrower_detail = BorrowerDetail.query.filter_by(book_entry=book_entry_obj.book_code, return_status=False).first()
        shelf_list = BookShelf.query.all()
        context['shelf_list'] = shelf_list
        context['borrower_detail'] = borrower_detail
        context['book_entry_obj'] = book_entry_obj
    return render_template("book_return.html", data=context)


@app.route('/lost_book/', methods=['GET', 'POST'])
def lost_book():
    data = request.form
    json_data = dict(data)
    book_code = json_data.pop('book_code')
    recover_amount = json_data.get('recover_amount', None)
    note = json_data.get('note', None)
    borrower_detail = json_data.get('borrower_detail', None)
    form = LostBookUserDetailForm(data)
    if form.validate():
        borrow_obj = LostBookUserDetail(recover_amount=recover_amount, note=note, borrower_detail=int(borrower_detail))
        db.session.add(borrow_obj)
        db.session.commit()
        book_status_obj = BookStatus.query.filter_by(name='Lost').first()
        book_entry_obj = BookEntry.query.filter_by(book_code=book_code).first()
        book_entry_obj.book_status = book_status_obj.id
        # book_entry_obj.book_shelf = int(book_shelf) its pending 
        db.session.commit()
        return redirect('/')
    else:
        flash_errors(form)
        return redirect(url_for('book_return', book_code=book_code))


@app.route('/overdued/', methods=['GET'])
def overdued():
    context = {}
    overdued_list = BookEntry.query.join(BorrowerDetail).filter(BorrowerDetail.return_date < datetime.date.today())
    context['overdued_list'] = overdued_list.all()
    return render_template("overdued.html", data=context)


@app.route('/donation_list/', methods=['GET'])
def donation_list():
    context = {}
    donation_list = BookEntry.query.filter(BookEntry.donated_by.isnot(None))
    context['donation_list'] = donation_list
    return render_template("donation_list.html", data=context)

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem' # !! save session in database instead of filesystem
    app.config['TEMPLATES_AUTO_RELOAD'] = True # to auto-reload templates changes.
    sess.init_app(app)
    bootstrap = Bootstrap(app)
    datepicker = datepicker(app)
    fujs = FlaskUtilJs(app)
    app.debug = True
    app.run()
