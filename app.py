import random
import string
from flask_socketio import join_room, leave_room, send, SocketIO, emit

from flask import *

app = Flask(__name__)
app.config["SECRET_KEY"] = b'_5#y2L"F4Q8z\n\xec]/'
socketio = SocketIO(app)
possible_turns = ["X's", "O's"]

urls = {}

board = [0, 0, 0,
         0, 0, 0,
         0, 0, 0]

board_names = ["one", "two", "three", "four", "five", "six", "seven", "eight"]
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
    name = session.get("name")
    if game is None or session.get("name") is None or game not in urls:
        return redirect(url_for("home"))

    return render_template("game.html", code=game, name=name)


@socketio.on("connect")
def handle_connect():
    print("Client Connected!")


@socketio.on("user_join")
def handle_user_join(name):
    print(f"user {name} joined!")

# circle turn... if False, return X, if True, Return 0's
@socketio.on("user_turn")
def handle_user_turn(circleTurn):
    if circleTurn == False:
        user_turn = possible_turns[0]
        emit("user_turn", user_turn, broadcast=True)
    else:
        user_turn = possible_turns[1]
        emit("user_turn", user_turn, broadcast=True)


@socketio.on("user_mark")
def handle_user_mark(mark, circleTurn):
    if circleTurn == False:
        board[int(mark)] += 2
        emit("user_mark", board, broadcast=True)
        print(board)
    else:
        print(board)
        board[int(mark)] += 1
        emit("user_mark", board, broadcast=True)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == '__main__':
    app.run()
