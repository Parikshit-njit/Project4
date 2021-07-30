from collections import OrderedDict

from app import db

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