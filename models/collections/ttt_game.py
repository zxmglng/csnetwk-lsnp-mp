games = {}  # key: game_id

WIN_LINES = [
    (0,1,2), (3,4,5), (6,7,8),  # rows
    (0,3,6), (1,4,7), (2,5,8),  # columns
    (0,4,8), (2,4,6)            # diagonals
]

def create_game(game_id, player_x, player_o):
    games[game_id] = {
        "board": [" "] * 9,
        "player_x": player_x,
        "player_o": player_o,
        "status": "IN_PROGRESS",
        "turn": "X"
    }

def make_move(game_id, pos, symbol):
    game = games.get(game_id)
    if not game or pos not in range(9) or game["board"][pos] != " ":
        return False
    game["board"][pos] = symbol
    game["turn"] = "O" if symbol == "X" else "X"
    return True

def get_game(game_id):
    return games.get(game_id)

def set_result(game_id, result, winning_line=None):
    game = games.get(game_id)
    if game:
        game["status"] = "FINISHED"
        game["winner"] = result
        game["winning_line"] = winning_line

def check_winner(game_id):
    game = games.get(game_id)
    if not game:
        return None, None
    board = game["board"]
    for a,b,c in WIN_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a], (a,b,c)
    if " " not in board:
        return "DRAW", None
    return None, None
