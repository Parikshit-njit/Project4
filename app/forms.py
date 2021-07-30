from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class AddressForm(FlaskForm):
    fname = StringField("First Name")
    lname = StringField("Last Name")
    address = StringField("Address")
    city = StringField("City")
    state = StringField("State")
    zip_code = StringField("Zip Code")
    submit = SubmitField("Submit")

