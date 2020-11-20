from flask import Flask, flash, request, render_template, redirect, url_for, session, json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.session import Session
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
import yaml
from utils import *
from form import *

app = Flask(__name__)
app.config.from_object(__name__)
sess = Session(app)

# !! write database connection code in seperate file / function.
db = yaml.load(open('db.yaml'))
database = db.get('database', None)
mysql_host = db.get('mysql_host', None)
mysql_user = db.get('mysql_user', None)
mysql_password = db.get('mysql_password', None)
mysql_db_name = db.get('mysql_db_name', None)
port = db.get('port', None)
app.config['SQLALCHEMY_DATABASE_URI'] = database+'://'+mysql_user+':'+mysql_password+'@'+mysql_host+':'+port+'/'+mysql_db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
            # !! very poor validation code, please add proper standard way of validating post data.
            username = data.get('username', None)
            password = data.get('password', None)
            user = User.query.filter_by(username=username).first() # !! never perform query on direct data from user.
            try:
                if not user or not check_password_hash(user.password, password):
                    flash('Invalid username and password!')
                    return render_template("login.html")
                else:
                    session['id'] = user.id
                return redirect('http://127.0.0.1:5000/') # !! not proper redirection coding, please correct it as per standards
            except:
                flash('User not found!', 'danger')
                return render_template("login.html")
        else:
            return render_template("login.html")
    else:
        flash('you already login', 'danger')
        return redirect('http://127.0.0.1:5000/') # !! not proper redirection coding, please correct it as per standards
            
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
            context['book_entry_obj'] = book_entry_obj.paginate(page, 10, False)
    page = request.args.get('page')
    data = session.get('data')
    if page and data:
        search = session.get('data').get('search')
        category = session.get('data').get('category')
        book_status = session.get('data').get('book_status')
        book_entry_obj = filter_data(search, category, book_status)
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
    app.config['SESSION_TYPE'] = 'filesystem' # !! save session in database instead of filesystem
    sess.init_app(app)
    bootstrap = Bootstrap(app)
    datepicker = datepicker(app)
    app.debug = True
    app.run()
