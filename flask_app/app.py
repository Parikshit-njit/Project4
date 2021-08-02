from sqlalchemy import create_engine
import repackage
repackage.up()
from flask_app import create_app


engine = create_engine('sqlite:///addresses.db', echo=True)


app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
