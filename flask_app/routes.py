from flask import Blueprint, session, url_for, render_template_string, request, redirect, render_template

routes_api = Blueprint('routes_api', __name__)


@routes_api.before_app_first_request
def prefill_db():
    from flask_app import db
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
    from flask_app import db
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
        from flask_app import db
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
    from flask_app import db
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
    from flask_app import db
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
    from flask_app import db
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
    from flask_app import db
    from flask import Response
    obj = Addresses.query.filter_by(id=address_id).one()
    db.session.delete(obj)
    db.session.commit();
    resp = Response(status=200, mimetype='application/json')
    return resp


@routes_api.route('/set_email', methods=['GET', 'POST'])
def set_email():
    if request.method == 'POST':
        # Save the form data to the session object
        session['email'] = request.form['email_address']
        session['redis_test'] = "session_test_variable"
        return redirect(url_for('routes_api.get_email'))

    return render_template('redis.html')


@routes_api.route('/get_email')
def get_email():
    return render_template_string("""
            {% if session['email'] %}
                <html>
                <body>
<head>
	<title>Learning Javascript</title>
	<link rel="stylesheet" type="text/css" href="style.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
	<script type="text/javascript" src="script.js"></script>
	<link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet">
                <style>
                    * {
	margin: 0;
	padding: 0;
}

body {
	background-color: #EEE;
}

.fly-in-text {
	list-style: none;
	position: absolute;
	left: 50%;
	top: 50%;
	transform: translateX(-50%) translateY(-50%);
}

.fly-in-text li {
	display: inline-block;
	margin-right:50px;
	font-family: Open Sans, Arial;
	font-weight: 300;
	font-size: 4em;
	opacity: 1;
	transition: all 2.5s ease;
}

@media screen and (max-width: 1275px) {
    .fly-in-text li {
		margin-right:30px;
		font-weight: 300;
		font-size: 3em;
	}
}

@media screen and (max-width: 900px) {
    .fly-in-text li {	
    	display: block;
		margin-right:20px;
		font-weight: 300;
		font-size: 3em;
	}
}

@media screen and (max-width: 768px) {
    .fly-in-text li {	
    	display: block;
		margin-right:20px;
		font-weight: 300;
		font-size: 3em;
		text-align: center;
        margin: 0 auto;
}
	}
}

.fly-in-text li:last-child {
	margin-right: 0;
}

.fly-in-text.hidden li {
	opacity: 0;
} 

.fly-in-text.hidden li:nth-child(1) {
	transform: translateX(-200px) translateY(-200px);
}
.fly-in-text.hidden li:nth-child(2) {
	transform: translateX(20px) translateY(100px);
}
.fly-in-text.hidden li:nth-child(3) {
	transform: translateX(-150px) translateY(-80px);
}
.fly-in-text.hidden li:nth-child(4) {
	transform: translateX(10px) translateY(-200px);
}
.fly-in-text.hidden li:nth-child(5) {
	transform: translateX(-300px) translateY(200px);
}
.fly-in-text.hidden li:nth-child(6) {
	transform: translateX(80px) translateY(-20px);
}
.fly-in-text.hidden li:nth-child(4) {
	transform: translateX(30px) translateY(200px);
}
                </style>
</head>
<body>
	<ul class="fly-in-text hidden">
		<li>W</li>
		<li>E</li>
		<li>L</li>
		<li>C</li>
		<li>O</li>
		<li>M</li>
		<li>E</li>
		<li>{{ session['email'] }}</li><br>
		<li style="font-size: 20px">Here's is your session variable: <b>{{ session['redis_test'] }}</b> </li><br><br><br>
		<li style="font-size: 30px">
	<a href="{{ url_for('routes_api.index') }}"> View Addresses </a>
	</li> <br>
	<li style="font-size: 30px">
	<a href="{{ url_for('routes_api.api_browse') }}"> View Addresses in Json Format </a>
	</li> <br>
		<li style="font-size: 30px">
	<a href="{{ url_for('routes_api.form_insert_post') }}"> New Address </a>
	</li> <br>
	<li style="font-size: 30px">
	<a href="{{ url_for('routes_api.delete_email') }}"> Delete Session </a>
	</li> <br>
	</ul>
	<script>
	$(function() {
	setTimeout(function() {
		$('.fly-in-text').removeClass('hidden');
	},500);
})();
	</script>
</body>
</html>
            {% else %}
                <h1>Welcome! Please enter your email <a href="{{ url_for('routes_api.set_email') }}">here.</a></h1>
            {% endif %}
        """)


@routes_api.route('/delete_email')
def delete_email():
    session.pop('email', default=None)
    return '<h1>Session deleted!</h1>'
