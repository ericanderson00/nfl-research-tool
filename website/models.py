from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #foreign key is a reference to another database which is col that refrences another db
    #'user.id' refrences the class 'User' but sql uses lower case
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') #'list' of all the different notes
    
#foreignKey is lower case when ref class
#relationship is uppercase when ref class
    
