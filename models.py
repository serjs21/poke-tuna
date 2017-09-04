from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Song %r>' % self.name


class User(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    phoneid = db.Column(db.String(80))
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    requested_song = db.Column(db.String(80), unique=True)

    def __init__(self, phoneid, x, y, requested_song):
        self.phoneid = phoneid
        self.x = int(x)
        self.y = int(y)
        self.requested_song = requested_song

    def __repr__(self):
        return '<User %r>' % self.name

db.create_all()
