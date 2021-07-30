from contextlib import redirect_stderr
from typing import List, Dict
import mysql.connector
import simplejson as json
from flask import Flask, Response, jsonify, session, url_for, render_template_string
from flask import request, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_sqlalchemy import SQLAlchemy
# from models import Addresses
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from collections import OrderedDict
from sqlalchemy.ext.serializer import loads, dumps
import redis
from flask_session import Session
from routes import routes_api

engine = create_engine('sqlite:///addresses.db', echo=True)

# Session = sessionmaker(bind=engine)
# session = Session()

app = Flask(__name__,
    instance_relative_config=False,
    template_folder="templates",
    static_folder="static"
            )

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///addresses.db'
app.config['SECRET_KEY'] = "Hello World!"

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')

# Create and initialize the Flask-Session object AFTER `app` has been configured
server_session = Session(app)

db = SQLAlchemy(app)
app.register_blueprint(routes_api)

@app.route('/set_email', methods=['GET', 'POST'])
def set_email():
    if request.method == 'POST':
        # Save the form data to the session object
        session['email'] = request.form['email_address']
        return redirect(url_for('get_email'))

    return """
        <form method="post">
            <label for="email">Enter your email address:</label>
            <input type="email" id="email" name="email_address" required />
            <button type="submit">Submit</button
        </form>
        """


@app.route('/get_email')
def get_email():
    return render_template_string("""
            {% if session['email'] %}
                <h1>Welcome {{ session['email'] }}!</h1>
            {% else %}
                <h1>Welcome! Please enter your email <a href="{{ url_for('set_email') }}">here.</a></h1>
            {% endif %}
        """)


@app.route('/delete_email')
def delete_email():
    # Clear the email stored in the session object
    session.pop('email', default=None)
    return '<h1>Session deleted!</h1>'


class Addresses(db.Model):
    """Data model for user addresses."""
    __table_args__ = (
        db.UniqueConstraint('fname', 'lname', 'address', 'state', 'city', 'zip_code'),
    )
    __tablename__ = 'addresses'
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    fname = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=True
    )

    lname = db.Column(
        db.String(80),
        index=False,
        unique=False,
        nullable=True
    )
    address = db.Column(
        db.String(80),
        index=False,
        unique=False,
        nullable=True
    )
    city = db.Column(
        db.String(80),
        index=False,
        unique=False,
        nullable=True
    )
    state = db.Column(
        db.String(80),
        index=False,
        unique=False,
        nullable=True
    )
    zip_code = db.Column(
        db.String(80),
        index=False,
        unique=False,
        nullable=True
    )

    def toDict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = str(getattr(self, key))
        return result

    def __repr__(self):
        return '<Addresses {}>'.format(self.id)

db.create_all()



class AddressForm(FlaskForm):
    fname = StringField("First Name")
    lname = StringField("Last Name")
    address = StringField("Address")
    city = StringField("City")
    state = StringField("State")
    zip_code = StringField("Zip Code")
    submit = SubmitField("Submit")


if __name__ == '__main__':
    app.run(host="0.0.0.0")
