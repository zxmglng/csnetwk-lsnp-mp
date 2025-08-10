games = {}  # key: GAMEID

def create_game(game_id, player_x, player_o):
    games[game_id] = {
        "board": [" "] * 9,
        "player_x": player_x,
        "player_o": player_o,
        "status": "IN_PROGRESS",
        "turn": "X"  # X always starts
    }


def make_move(game_id, position, symbol):
    game = games.get(game_id)
    if game and game["board"][position] == " ":
        game["board"][position] = symbol
        game["turn"] = "O" if symbol == "X" else "X"
        return True
    return False

def get_game(game_id):
    return games.get(game_id)

def set_result(game_id, result, winning_line=None):
    game = games.get(game_id)
    if game:
        game["winner"] = result
        game["winning_line"] = winning_line

WINNING_LINES = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]

def check_winner(game_id):
    game = games.get(game_id)
    if not game:
        return None, None

    board = game["board"]
    for a, b, c in WINNING_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a], (a, b, c)

    if " " not in board:
        return "DRAW", None

    return None, None

