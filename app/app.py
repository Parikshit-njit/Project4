from typing import List, Dict
import mysql.connector
import simplejson as json
from flask import Flask, Response
from flask import request, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_sqlalchemy import SQLAlchemy
# from models import Addresses
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__,
    instance_relative_config=False,
    template_folder="templates",
    static_folder="static"
            )

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///addresses.db'
app.config['SECRET_KEY'] = "Hello World!"
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

db.create_all()


class AddressForm(FlaskForm):
    fname = StringField("First Name")
    lname = StringField("Last Name")
    address = StringField("Address")
    city = StringField("City")
    state = StringField("State")
    zip_code = StringField("Zip Code")
    submit = SubmitField("Submit")


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Address Project'}
    all_addresses = Addresses.query.order_by(Addresses.id)
    return render_template('index.html', title='Home', user=user, all_addresses = all_addresses)


# @app.route('/view/<int:address_id>', methods=['GET'])
# def record_view(address_id):
#     cursor = mysql.get_db().cursor()
#     cursor.execute('SELECT * FROM addresses WHERE id=%s', address_id)
#     result = cursor.fetchall()
#     return render_template('view.html', title='View Form', city=result[0])
#
#
# @app.route('/edit/<int:address_id>', methods=['GET'])
# def form_edit_get(address_id):
#     cursor = mysql.get_db().cursor()
#     cursor.execute('SELECT * FROM addresses WHERE id=%s', address_id)
#     result = cursor.fetchall()
#     return render_template('edit.html', title='Edit Form', address=result[0])
#
#
# @app.route('/edit/<int:address_id>', methods=['POST'])
# def form_update_post(address_id):
#     cursor = mysql.get_db().cursor()
#     inputData = (request.form.get('Fname'), request.form.get('Lname'), request.form.get('Address'),
#                  request.form.get('City'), request.form.get('State'),
#                  request.form.get('Zip_Code'), address_id)
#     sql_update_query = """UPDATE addresses t SET t.Fname = %s, t.Lname = %s, t.Address = %s, t.City =
#     %s, t.State = %s, t.Zip_Code = %s WHERE t.id = %s """
#     cursor.execute(sql_update_query, inputData)
#     mysql.get_db().commit()
#     return redirect("/", code=302)
#
#
@app.route('/address/new', methods=['GET', 'POST'])
def form_insert_get():
    form = AddressForm()
    addressNew = Addresses(fname=form.fname.data, lname=form.lname.data, address=form.address.data, city=form.city.data, state=form.state.data, zip_code=form.zip_code.data)
    db.session.add(addressNew)
    db.session.commit()
    fname = form.fname
    form.fname.data = ''
    form.lname.data = ''
    form.address.data = ''
    form.city.data = ''
    form.state.data = ''
    form.zip_code.data = ''
    all_addresses = Addresses.query.order_by(Addresses.id)
    return render_template('new.html', title='New Address Form', form=form, fname=fname, all_addresses = all_addresses)
#
#
# @app.route('/address/new', methods=['POST'])
# def form_insert_post():
#     cursor = mysql.get_db().cursor()
#     inputData = (request.form.get('Fname'), request.form.get('Lname'), request.form.get('Address'),
#                  request.form.get('City'), request.form.get('State'),
#                  request.form.get('Zip_Code'))
#     sql_insert_query = """INSERT INTO addresses (Fname,Lname,Address,City,State,Zip_Code) VALUES (%s, %s,%s, %s,%s, %s) """
#     cursor.execute(sql_insert_query, inputData)
#     mysql.get_db().commit()
#     return redirect("/", code=302)
#
#
# @app.route('/delete/<int:address_id>', methods=['POST'])
# def form_delete_post(address_id):
#     cursor = mysql.get_db().cursor()
#     sql_delete_query = """DELETE FROM addresses WHERE id = %s """
#     cursor.execute(sql_delete_query, address_id)
#     mysql.get_db().commit()
#     return redirect("/", code=302)
#
#
# @app.route('/api/v1/addresses', methods=['GET'])
# def api_browse() -> str:
#     cursor = mysql.get_db().cursor()
#     cursor.execute('SELECT * FROM addresses')
#     result = cursor.fetchall()
#     json_result = json.dumps(result);
#     resp = Response(json_result, status=200, mimetype='application/json')
#     return resp
#
#
# @app.route('/api/v1/addresses/<int:address_id>', methods=['GET'])
# def api_retrieve(address_id) -> str:
#     cursor = mysql.get_db().cursor()
#     cursor.execute('SELECT * FROM addresses WHERE id=%s', address_id)
#     result = cursor.fetchall()
#     json_result = json.dumps(result);
#     resp = Response(json_result, status=200, mimetype='application/json')
#     return resp
#
#
# @app.route('/api/v1/addresses/<int:address_id>', methods=['PUT'])
# def api_edit(address_id) -> str:
#     cursor = mysql.get_db().cursor()
#     content = request.json
#     inputData = (content['Fname'], content['Lname'], content['Address'],
#                  content['City'], content['State'],
#                  content['Zip_Code'], address_id)
#     sql_update_query = """UPDATE addresses t SET t.Fname = %s, t.Lname = %s, t.Address = %s, t.City =
#         %s, t.State = %s, t.Zip_Code = %s WHERE t.id = %s """
#     cursor.execute(sql_update_query, inputData)
#     mysql.get_db().commit()
#     resp = Response(status=200, mimetype='application/json')
#     return resp
#
#
# @app.route('/api/v1/addresses', methods=['POST'])
# def api_add() -> str:
#
#     content = request.json
#
#     cursor = mysql.get_db().cursor()
#     inputData = (content['Fname'], content['Lname'], content['Address'],
#                  content['City'], content['State'],
#                  content['Zip_Code'])
#     sql_insert_query = """INSERT INTO addresses (Fname,Lname,Address,City,State,Zip_Code) VALUES (%s, %s,%s, %s,%s, %s) """
#     cursor.execute(sql_insert_query, inputData)
#     mysql.get_db().commit()
#     resp = Response(status=201, mimetype='application/json')
#     return resp
#
#
# @app.route('/api/v1/addresses/<int:address_id>', methods=['DELETE'])
# def api_delete(address_id) -> str:
#     cursor = mysql.get_db().cursor()
#     sql_delete_query = """DELETE FROM addresses WHERE id = %s """
#     cursor.execute(sql_delete_query, address_id)
#     mysql.get_db().commit()
#     resp = Response(status=200, mimetype='application/json')
#     return resp


if __name__ == '__main__':
    app.run(host="0.0.0.0")
