from app import *

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
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)
    book_shelf = db.Column(db.Integer, db.ForeignKey('book_shelf.id'),
        nullable=False)
    book_status = db.Column(db.Integer, db.ForeignKey('book_status.id'),
        nullable=False)
    donated_by = db.Column(db.String(100), nullable=True)


