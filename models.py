from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Category(db.Model):
    """docstring for Category"""
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name


class BookShelf(db.Model):
    """docstring for BookShelf"""
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name


class BookStatus(db.Model):
    """docstring for BookStatus"""
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name


class BookEntry(db.Model):
    """docstring for BookEntry"""
    book_code = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1000, increment=1), primary_key = True)
    name = db.Column(db.String(500), nullable=False)
    book_language = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=True)
    publisher = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Float, nullable=True)
    category = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)
    category_name = db.relationship("Category", foreign_keys=category)
    book_shelf = db.Column(db.Integer, db.ForeignKey('book_shelf.id'),
        nullable=False)
    shelf_name = db.relationship("BookShelf", foreign_keys=book_shelf)
    book_status = db.Column(db.Integer, db.ForeignKey('book_status.id'),
        nullable=False)
    book_status_name = db.relationship("BookStatus", foreign_keys=book_status)
    donated_by = db.Column(db.String(100), nullable=True)

class BorrowerDetail(db.Model):
    """docstring for BorrowerDetail"""
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    cell_no = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    issue_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    return_status = db.Column(db.Boolean, default=False, nullable=False)
    book_entry = db.Column(db.Integer, db.ForeignKey('book_entry.book_code'),
        nullable=False)