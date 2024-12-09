from asyncio import timeout

import flask
import queue
import threading
from time import sleep

from flask import jsonify

from games.twentyone import TwentyOne
import json

app = flask.Flask(__name__, template_folder='frontend', static_folder='frontend')
flask_queue = queue.Queue()
game = TwentyOne()
game_thread = threading.Thread(target=game.run, daemon=True)
url_list = []
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
        return flask.render_template('index.html', image_urls=url_list)

@app.route('/games/', methods=['POST'])
def games():
    pass


@app.route('/data/', methods=['GET','POST'])
def data():
    try:
        data_to_json = json.loads(flask.request.data)
        if data_to_json['input'] == "Yes":
            print(f"received message: {data_to_json['input']}")
            game.queue.put(1)
        elif data_to_json['input'] == "No":
            print(f"received message: {data_to_json['input']}")
            game.queue.put(0)
        while game.to_send.empty():
            sleep(0.5)

    except Exception as e:
        print(e)
    try:
        while game.to_send.empty():
            sleep(0.1)
        game_data = game.to_send.get()

        for card in game_data["data"]["dealer_hand"]:
            img_file = f'img/{card["suit"]}_{card["rank"]}.png'
            image_url = flask.url_for('static', filename=f'{img_file}')
            url_list.append(image_url)

        for card in game_data["data"]["player_hand"]:
            img_file = f'img/{card["suit"]}_{card["rank"]}.png'
            image_url = flask.url_for('static', filename=f'{img_file}')
            url_list.append(image_url)

        json_report = json.dumps(game_data)
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
    app.run(debug=True, threaded=True, use_reloader=True, host='127.0.0.1', port=5000)