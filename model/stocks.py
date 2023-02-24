from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


class Stock(db.Model):
    __tablename__ = 'stocks'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _ticker = db.Column(db.String(255), unique=False, nullable=False)
    _rating = db.Column(db.String(255), unique=False, nullable=False)


    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, ticker, rating="neutral"):
        self._name = name    # variables with self prefix become part of the object, 
        self._ticker = ticker
        self._rating = rating

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    # a getter method, extracts email from object
    @property
    def ticker(self):
        return self._ticker
    
    # a setter function, allows name to be updated after initial object creation
    @ticker.setter
    def ticker(self, ticker):
        self._ticker = ticker

    @property
    def rating(self):
        return self._rating
    
    # a setter function, allows name to be updated after initial object creation
    @rating.setter
    def rating(self, rating):
        self._rating = rating

    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "ticker": self.ticker,
            "rating": self.rating,
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", ticker="", rating=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(ticker) > 0:
            self.ticker = ticker
        if len(rating) > 0:
            self.rating = rating
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    
    ## Created a database that stores stocks above


"""Database Creation and Testing """


# Builds working data for testing
def initStocks():
    """Create database and tables"""
    db.create_all()
    """Tester data for table"""
    s1 = Stock(name='APPLE<', ticker='APPL', rating='STONG SELL')
    s2 = Stock(name='NVIDIA', ticker='NVDA', rating='STRONG BUY')
    s3 = Stock(name='EXXON MOBILE', ticker='XOM', rating='NEUTRAL')

    stocks = [s1, s2, s3,]

    """Builds sample user/note(s) data"""
    for stock in stocks:
        try:
            '''add user/post data to table'''
            stock.create()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {stock.id}")
            