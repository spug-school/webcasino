import flask
import queue
import threading
from time import sleep

from flask import jsonify

from games.twentyone import TwentyOne
import json

app = flask.Flask(__name__, template_folder='frontend')
app.static_folder = 'frontend'
flask_queue = queue.Queue()
game = TwentyOne()
game_thread = threading.Thread(target=game.run, daemon=True)

if not game_thread.is_alive():
    try:
        game_thread.start()
        if not game.queue.empty():
            print(game.queue.get())
    except KeyboardInterrupt:
        game_thread.join()

@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'GET':
        return flask.render_template('index.html')


@app.route('/data/', methods=['GET','POST'])
def data():
    try:
        print(flask.request.headers)
        for i in flask.request.data:
            print(i)
    except Exception as e:
        print(e)
    try:
        json_report = json.dumps(game.get_data())
        response = flask.make_response(json_report)
        response.mimetype = 'application/json'
    except Exception as e:
        print(e)
        response = flask.make_response(str(e))
        response.mimetype = 'text/plain'
        response.headers = {'status': 'error', 'message': str(e)}
        return response
    return response



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='127.0.0.1', port=5000)