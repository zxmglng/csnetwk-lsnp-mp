from models.collections import ttt_game
from views.tictactoe import print_board
from models.collections.ttt_game import check_winner
from verbose import vprint
from models.collections import my_profile

def handle(message: dict):
    game_id = message.get("GAMEID")
    position = message.get("POSITION")
    symbol = message.get("SYMBOL")

    # Validate position
    try:
        position = int(position)
    except (TypeError, ValueError):
        print(f"Invalid position received: {position}")
        return

    profile = my_profile.get_profile()
    if not profile:
        return

    game = ttt_game.get_game(game_id)
    if not game:
        print(f"Received move for unknown game {game_id}.")
        return

    if ttt_game.make_move(game_id, position, symbol):
        vprint("RECV", f"Tic Tac Toe move from {message.get('FROM')} — position {position}", msg_type="TICTACTOE_MOVE")
        print_board(game["board"])

        winner, winning_line = check_winner(game_id)
        if winner:
            # Determine my symbol for result calculation
            my_symbol = "X" if game["player_x"] == profile.USER_ID else "O"
            result = "DRAW" if winner == "DRAW" else ("WIN" if my_symbol == winner else "LOSS")
            print(f"Game Over! Result: {result}")
            if winning_line:
                print(f"Winning line: {winning_line}")
        else:
            print(f"Your turn ({game['turn']}).")
