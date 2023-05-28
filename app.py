import random
import string
from flask_socketio import join_room, leave_room, send, SocketIO

from flask import *

app = Flask(__name__)
app.config["SECRET_KEY"] = b'_5#y2L"F4Q8z\n\xec]/'
socketio = SocketIO(app)

urls = {}


def generate_unique_url():
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        if code not in urls:
            break

    return code


@app.route('/', methods=["GET", "POST"])
def home():
    session.clear()
    if request.method == 'POST':
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template('home.html', error="Please enter a name", code=code, name=name)

        if join != False and not code:
            return render_template('home.html', error="Please enter a game code", code=code, name=name)

        game = code
        if create != False:
            game = generate_unique_url()
            urls[game] = {"members": 0}
        elif code not in urls:
            return render_template('home.html', error="game does not exist", code=code, name=name)

        session["game"] = game
        session["name"] = name
        return redirect(url_for("game"))

    return render_template('home.html')


@app.route('/game')
def game():
    game = session.get("game")
    if game is None or session.get("name") is None or game not in urls:
        return redirect(url_for("home"))

    return render_template('game.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == '__main__':
    app.run()
