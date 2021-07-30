from collections import OrderedDict
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from app import db

class AddressForm(FlaskForm):
    fname = StringField("First Name")
    lname = StringField("Last Name")
    address = StringField("Address")
    city = StringField("City")
    state = StringField("State")
    zip_code = StringField("Zip Code")
    submit = SubmitField("Submit")

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