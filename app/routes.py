from flask import Blueprint

routes_api = Blueprint('routes_api', __name__)


@routes_api.before_app_first_request
def prefill_db():
    from app import db, Addresses, app
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