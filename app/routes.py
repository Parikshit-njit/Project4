from flask import Blueprint


routes_api = Blueprint('routes_api', __name__)


@routes_api.before_app_first_request
def prefill_db():
    from app import db
    from models import Addresses
    db.session.query(Addresses).delete()
    db.session.commit()
    try:
        for csv_row in open("../db/addresses.csv", "r"):
            line = csv_row.strip().split(",")
            print(line)
            fname = line[0]
            lname = line[1]
            address = line[2]
            city = line[3]
            state = line[4]
            zip_code = line[5]
            newAddress = Addresses(fname=fname, lname=lname, address=address, city=city, state=state, zip_code=zip_code)
            db.session.add(newAddress)
            db.session.commit()
    except:
        print("HANG ON!!!")
    finally:
        print("In finally...")


@routes_api.route('/', methods=['GET'])
def index():
    from models import Addresses
    from flask import render_template
    user = {'username': 'Address Project'}
    all_addresses = Addresses.query.order_by(Addresses.id)
    return render_template('index.html', title='Home', user=user, all_addresses = all_addresses)


@routes_api.route('/view/<int:address_id>', methods=['GET'])
def record_view(address_id):
    from models import Addresses
    from flask import render_template
    print(Addresses.query.get(address_id).fname)
    return render_template('view.html', title='View Form', city=Addresses.query.get(address_id))


@routes_api.route('/edit/<int:address_id>', methods=['GET'])
def form_edit_get(address_id):
    from models import Addresses
    from flask import render_template
    obj = Addresses.query.filter_by(id=address_id).one()
    return render_template('edit.html', title='Edit Form', address=obj)
#
#


@routes_api.route('/edit/<int:address_id>', methods=['POST'])
def form_update_post(address_id):
    from app import db
    from models import Addresses
    from flask import request, redirect
    obj = Addresses.query.filter_by(id=address_id).one()
    obj.fname = request.form.get('fname')
    obj.lname = request.form.get('lname')
    obj.address = request.form.get('address')
    obj.city = request.form.get('city')
    obj.state = request.form.get('state')
    obj.zip_code = request.form.get('zip_code')
    db.session.flush()
    db.session.commit()
    return redirect("/", code=302)
#
#


@routes_api.route('/address/new', methods=['POST'])
def form_insert_get():
        from models import Addresses
        from forms import AddressForm
        from app import db
        from flask import render_template
        form = AddressForm()
        addressNew = Addresses(fname=form.fname.data, lname=form.lname.data, address=form.address.data,
                               city=form.city.data, state=form.state.data, zip_code=form.zip_code.data)
        fname = form.fname
        db.session.add(addressNew)
        db.session.commit()
        form.fname.data = ''
        form.lname.data = ''
        form.address.data = ''
        form.city.data = ''
        form.state.data = ''
        form.zip_code.data = ''
        all_addresses = Addresses.query.order_by(Addresses.id)
        return render_template('new.html', title='New Address Form', form=form, fname=fname, all_addresses = all_addresses)


@routes_api.route('/address/new', methods=['GET'])
def form_insert_post():
    from flask import render_template
    from forms import AddressForm
    from models import Addresses
    form = AddressForm()
    all_addresses = Addresses.query.order_by(Addresses.id)
    return render_template('new.html', title='New Address Form', form=form, all_addresses=all_addresses)
    return redirect("/", code=302)


@routes_api.route('/delete/<int:address_id>', methods=['POST'])
def form_delete_post(address_id):
    from models import Addresses
    from app import db
    from flask import redirect
    obj = Addresses.query.filter_by(id=address_id).one()
    db.session.delete(obj)
    db.session.commit();
    return redirect("/", code=302)


@routes_api.route('/api/v1/addresses', methods=['GET'])
def api_browse() -> str:
    from models import Addresses
    from flask import jsonify
    resp = Addresses.query.all()
    json_arr = []
    for temp in resp:
        json_arr.append(temp.toDict())
    return jsonify(json_arr)


@routes_api.route('/api/v1/addresses/<int:address_id>', methods=['GET'])
def api_retrieve(address_id) -> str:
    from models import Addresses
    from flask import jsonify
    resp = Addresses.query.filter_by(id=address_id).one()
    return jsonify(resp.toDict())


@routes_api.route('/api/v1/addresses/<int:address_id>', methods=['PUT'])
def api_edit(address_id) -> str:
    from app import db
    from models import Addresses
    from flask import request, Response
    content = request.json
    obj = Addresses.query.filter_by(id=address_id).one()
    obj.fname = content['fname']
    obj.lname = content['lname']
    obj.address = content['address']
    obj.city = content['city']
    obj.state = content['state']
    obj.zip_code = content['zip_code']
    db.session.commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@routes_api.route('/api/v1/addresses', methods=['POST'])
def api_add() -> str:
    from models import Addresses
    from app import db
    from flask import request, Response
    content = request.json

    newAddress = Addresses(fname = content['fname'], lname = content['lname'], address = content['address'],
                 city = content['city'], state = content['state'],
                 zip_code = content['zip_code'])
    db.session.add(newAddress)
    db.session.commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@routes_api.route('/api/v1/addresses/<int:address_id>', methods=['DELETE'])
def api_delete(address_id) -> str:
    from models import Addresses
    from app import db
    from flask import Response
    obj = Addresses.query.filter_by(id=address_id).one()
    db.session.delete(obj)
    db.session.commit();
    resp = Response(status=200, mimetype='application/json')
    return resp
