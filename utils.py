import copy

def init_game_state(rows, cols):
    game_state = {}

    # create empty game board
    game_board = []
    for row in range(rows):
        temp_row = []
        for col in range(cols):
            cell = {
                'location': (row, col),
                'holder': None
            }
            temp_row.append(cell)
        game_board.append(temp_row)
    
    # Initialize game state vars
    game_state['board'] = game_board
    game_state['holder-colors'] = {}

    return game_state

def generate_next_frame(game_state):
    cell_updates = []

    game_board = game_state['board']
    game_board_copy = copy.deepcopy(game_board)

    # For each cell in the game board
    for row in range(len(game_board)):
        for col in range(len(game_board[0])):
            cell_copy = game_board_copy[row][col]
            # If the cell has a holder
            if cell_copy['holder'] != None:
                # Find the valid neighbors (within bounds of gameboard)
                valid_neighbors = find_valid_neighbors(cell_copy, len(game_board), len(game_board[0]))
                # for each of these neighbors
                for neighbor_location in valid_neighbors:
                    # extract the cell from the COPY of the game board
                    neighbor_cell = game_board_copy[neighbor_location[0]][neighbor_location[1]]
                    # if the cell has no holder
                    if neighbor_cell['holder'] == None:
                        game_board[neighbor_location[0]][neighbor_location[1]]['holder'] = cell_copy['holder']
                        update = {
                            'location': neighbor_cell['location'],
                            'color': game_state['holder-colors'][cell_copy['holder']]
                        }
                        cell_updates.append(update)
    return cell_updates

def find_valid_neighbors(cell, ROWS, COLS):
    valid_neighbors = []
    rownum = cell['location'][0]
    colnum = cell['location'][1]
    if rownum > 0:
        valid_neighbors.append( (rownum - 1, colnum) )
    if colnum > 0:
        valid_neighbors.append( (rownum, colnum - 1) )
    if rownum < ROWS - 1:
        valid_neighbors.append( (rownum + 1, colnum) )
    if colnum < COLS - 1:
        valid_neighbors.append( (rownum, colnum + 1) )
    return valid_neighbors

# Takes a user action, game_state, and uid.
# Edits the game_state in place to apply the action.
def apply_user_action(game_state, action, uid):
    cell_updates = []

    game_board = game_state['board']

    location = action['location']

    # ignore this var for now
    action = action['action']

    game_board[int(location[0])][int(location[1])]['holder'] = uid
    update = {
                'location': location,
                'color': game_state['holder-colors'][uid]
            }
    cell_updates.append(update)
    return cell_updates