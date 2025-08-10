from typing import Optional, Tuple

games: dict[str, dict] = {}  # key: GAMEID

def create_game(game_id: str, player_x: str, player_o: str) -> None:
    """Initialize a new Tic Tac Toe game."""
    games[game_id] = {
        "board": [" "] * 9,
        "player_x": player_x,
        "player_o": player_o,
        "status": "IN_PROGRESS",
        "turn": "X"  # X always starts
    }

def make_move(game_id: str, position: int, symbol: str) -> bool:
    """Place a move on the board if valid."""
    game = games.get(game_id)
    if not game:
        return False
    if position < 0 or position >= 9:
        return False
    if game["board"][position] != " ":
        return False

    game["board"][position] = symbol
    game["turn"] = "O" if symbol == "X" else "X"
    return True

def get_game(game_id: str) -> Optional[dict]:
    """Retrieve the game state."""
    return games.get(game_id)

def set_result(game_id: str, result: str, winning_line: Optional[Tuple[int, int, int]] = None) -> None:
    """Mark a game as finished with the result and optional winning line."""
    game = games.get(game_id)
    if game:
        game["status"] = "FINISHED"
        game["winner"] = result
        game["winning_line"] = winning_line

WINNING_LINES: list[Tuple[int, int, int]] = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]

def check_winner(game_id: str) -> Tuple[Optional[str], Optional[Tuple[int, int, int]]]:
    """Check if there is a winner or if the game is a draw."""
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
