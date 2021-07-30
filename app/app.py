from flask import Flask, session, url_for, render_template_string
from flask import request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import redis
from flask_session import Session
from routes import routes_api

engine = create_engine('sqlite:///addresses.db', echo=True)


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
    session.pop('email', default=None)
    return '<h1>Session deleted!</h1>'


db.create_all()


if __name__ == '__main__':
    app.run(host="0.0.0.0")
