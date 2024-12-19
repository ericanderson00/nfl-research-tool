from . import db # . = __init__.py
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey

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
    
class PlayerInfo(db.Model):
    __tablename__ = 'players'
    playerID = db.Column(db.Integer, primary_key=True)
    playerName = db.Column(db.String(50), nullable=False, index=True)
    pos = db.Column(db.String(4))
    team = db.Column(db.String(30))
    
    gameLogs = db.relationship('GameLog', backref='playerinfo')
    
class GameLog(db.Model):
    __tablename__ = 'game_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playerID = db.Column(db.Integer, db.ForeignKey('players.playerID'))
    # playerName = db.Column(db.String(50), nullable=False, index=True)
    playerOpp = db.Column(db.String(10))
    week = db.Column(db.Integer)
    year = db.Column(db.Integer)
    
    receptions = db.Column(db.Integer, default=0)
    recYds = db.Column(db.Integer, default=0)
    recTD = db.Column(db.Integer, default=0)
    recAvg = db.Column(db.Float, default=0) #add later
    recLong = db.Column(db.Integer, default=0) #add later
    targets =db.Column(db.Integer, default=0) #add later
    
    rushYards = db.Column(db.Integer, default=0) 
    rushTD = db.Column(db.Integer, default=0)
    rushAvg = db.Column(db.Float, default=0)#add later
    carries = db.Column(db.Integer, default=0) #add later
    longRush = db.Column(db.Float, default=0)#add later
    
    
    passYards = db.Column(db.Integer, default=0)
    passTD = db.Column(db.Integer, default=0)
    interceptions = db.Column(db.Integer, default=0)
    passComp = db.Column(db.Integer, default=0) #add later
    passAttempts = db.Column(db.Integer, default=0) #add later
    passAvg = db.Column(db.Float, default=0) #add later
    
    
    
    
    fanPoints = db.Column(db.Float)     