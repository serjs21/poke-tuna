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
    id = db.Column(db.String(80))
    phoneid = db.Column(db.String(80),  primary_key=True, unique=True)
    long = db.Column(db.Float)
    lat = db.Column(db.Float)
    requested_song = db.Column(db.String(80), unique=True)

    def __init__(self, phoneid, lat, long, requested_song):
        self.phoneid = phoneid
        self.lat = float(lat)
        self.long = float(long)
        self.requested_song = requested_song

    def __repr__(self):
        return '<User %r>' % self.phoneid

db.drop_all()
db.create_all()
