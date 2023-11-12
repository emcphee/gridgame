from flask import Flask, render_template, session, request, jsonify
from utils import init_game_state
import uuid
from flask_socketio import SocketIO, emit
import time
import utils

app = Flask(__name__)
socketio = SocketIO(app)

app.secret_key = 'yoijdsfnjokdwsvfnweoffeq9uh'

ROWS = 100
COLS = 100

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
        time.sleep(0.1) # update delay

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

@socketio.on('connect')
def handle_connect():
    print('Client connected')

    # Generate uid
    session['uid'] = uuid.uuid4()

    # Generate global game state vars
    unapplied_actions[session['uid']] = []
    game_states[session['uid']] = init_game_state(ROWS, COLS)
    
    # initialize the holder color
    # TODO: make game state indexed in lobby num, not session uid
    game_states[session['uid']]['holder-colors'][session['uid']] = '#FF0000'

    # Start game update loop
    socketio.start_background_task(target=send_update, uid=session['uid'])

if __name__ == '__main__':
    socketio.run(app, debug=True)