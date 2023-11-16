from flask import Flask, render_template, session, request, jsonify
from flask_socketio import SocketIO, emit
import uuid
import time

import utils

app = Flask(__name__)
socketio = SocketIO(app)

app.secret_key = 'yoijdsfnjokdwsvfnweoffeq9uh'

ROWS = 100
COLS = 100
tick_time = 0.2 # tick time in seconds

game_states = {}
unapplied_actions = {}

@app.route('/')
def index():
    return render_template('index.html', row_count=ROWS, column_count=COLS)

@socketio.on('client_action')
def update_game(data):
    if session['uid'] in unapplied_actions:
        unapplied_actions[session['uid']].append(data)
        return jsonify({'message': 'Update received successfully.'})
    else:
        return jsonify({'message': 'Update received but player not yet initialized.'})

def send_update(uid):
    while True:
        start_time = time.time()

        cell_updates = [] # updates we need to send the clients

        updated_cells = utils.generate_next_frame(game_states[uid])
        cell_updates += updated_cells

        # single action from user
        if len(unapplied_actions[uid]) > 0:
            cell_updates += utils.apply_user_action(game_states[uid], unapplied_actions[uid][0], uid)
            unapplied_actions[uid] = unapplied_actions[uid][1:]

        # send updates if there are any
        if len(cell_updates) > 0:
            socketio.emit('update', {'cell_updates': cell_updates})

        # If tick finished faster than the tick time, wait
        compute_time = time.time() - start_time
        sleep_duration = max(0, tick_time - compute_time)
        time.sleep(sleep_duration)
        if compute_time > tick_time:
            print("Goal Tick Time:", tick_time, "Actual:", compute_time)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

    # Generate uid
    session['uid'] = uuid.uuid4()

    # Generate global game state vars
    unapplied_actions[session['uid']] = []
    game_states[session['uid']] = utils.init_game_state(ROWS, COLS)
    
    # initialize the holder color
    # TODO: make game state indexed in lobby num, not session uid
    game_states[session['uid']]['holder-colors'][session['uid']] = '#000000'

    # Start game update loop
    socketio.start_background_task(target=send_update, uid=session['uid'])

if __name__ == '__main__':
    socketio.run(app, debug=True, port=8001, host='0.0.0.0', allow_unsafe_werkzeug=True)