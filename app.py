#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import json
import os
from models import db
from models import Song
from models import User
from models import app
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
#
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# db.init_app(app)
#
#
# class Song(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=True)
#
#     def __init__(self, name):
#         self.name = name
#
#     def __repr__(self):
#         return '<Song %r>' % self.name
#
# db.create_all()


# def init_db():
#     # import all modules here that might define models so that
#     # they will be registered properly on the metadata.  Otherwise
#     # you will have to import them first before calling init_db()
#     # import yourapplication.models
#     Base.metadata.create_all(bind=engine)
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

# app = Flask(__name__)
# app.config.from_object('config')

# db = SQLAlchemy(app)
# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/api/v1.0/add_song', methods=['POST'])
def add_song():
    data = json.loads(request.data)
    song = Song(data['name'])
    db.session.add(song)
    db.session.commit()
    return 'Song %s was added\n' % data['name']


@app.route('/api/v1.0/check_song', methods=['POST'])
def check_song():
    name = json.loads(request.data)['name']
    if Song.query.filter_by(name=name).first():
        return 'Song %s exists\n' % name
    else:
        return 'Song %s doesn\'t exist\n' % name


@app.route('/api/v1.0/update_user', methods=['POST'])
def update_user():
    data = json.loads(request.data)
    rs = None
    if data.has_key('requested_song'):
        rs = data['requested_song']
    if not User.query.filter_by(phoneid=data['phoneid']).first():
        user = User(data['phoneid'], data['lat'], data['long'], rs)
        db.session.add(user)
        db.session.commit()
    else:
        User.query.filter_by(phoneid=data['phoneid']).long = data['long']
        User.query.filter_by(phoneid=data['phoneid']).lat = data['lat']
        User.query.filter_by(phoneid=data['phoneid']).requested_song = rs
        db.session.commit()
    return 'User updated\n'


@app.route('/api/v1.0/usercount', methods=['POST'])
def get_users():
    users = User.query.all()
    data = json.loads(request.data)
    counter = 0
    rs = None
    if data.has_key('requested_song'):
        rs = data['requested_song']
    for u in users:
        if (u.lat - float(data['lat'])) ** 2 + (u.long - float(data['long'])) ** 2 <= float(data['range'])   ** 2:
            if rs:
                if u.requested_song == rs:
                    counter += 1
            else:
                counter += 1
    return json.dumps({'count': counter})


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
# if __name__ == '__main__':
#     app.run()
#
# # Or specify port manually:
# '''
if __name__ == '__main__':
    # db = init()
    # global db
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)
# '''
