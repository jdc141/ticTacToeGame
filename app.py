from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def landing_page():
    return render_template('landing_page.html')


@app.route('/game')
def game():
    return render_template('game.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == '__main__':
    app.run()
