import os
from flask import Flask, render_template, redirect, url_for, session
from dotenv import load_dotenv

load_dotenv()

from controllers.controllers import setup, game

app = Flask(__name__)

app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.register_blueprint(setup)
app.register_blueprint(game)

@app.route("/")
def index():
    access_token = session.get('access_token')
    if access_token:
        return redirect(url_for("game.play"))
    else:
        return render_template("index.html", artists_data=session.get('artists', {}))

def not_found(error):
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.register_error_handler(404, not_found)
    app.run(debug=True)