from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)


class Addresses(db.Model):
    """Data model for user addresses."""

    __tablename__ = 'addresses'
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    fname = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=True
    )

    lname = db.Column(
        db.String(80),
        index=False,
        unique=True,
        nullable=True
    )
    address = db.Column(
        db.String(80),
        index=False,
        unique=True,
        nullable=True
    )
    city = db.Column(
        db.String(80),
        index=False,
        unique=True,
        nullable=True
    )
    state = db.Column(
        db.String(80),
        index=False,
        unique=True,
        nullable=True
    )
    zip_code = db.Column(
        db.String(80),
        index=False,
        unique=True,
        nullable=True
    )

    def __repr__(self):
        return '<Addresses {}>'.format(self.id)