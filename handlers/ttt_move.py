from models.collections import ttt_game, my_profile
from models.collections.ttt_game import check_winner
from views.tictactoe import print_board
from verbose import vprint

def handle(message):
    game_id = message.get("GAMEID")
    position = message.get("POSITION")
    symbol = message.get("SYMBOL")

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
        print(f"Move received for unknown game {game_id}.")
        return

    if ttt_game.make_move(game_id, position, symbol):
        vprint("RECV", f"Move from {message.get('FROM')} — position {position}", msg_type="TICTACTOE_MOVE")
        print_board(game["board"])

        winner, line = check_winner(game_id)
        if winner:
            my_symbol = "X" if game["player_x"] == profile.USER_ID else "O"
            if winner == "DRAW":
                result = "DRAW"
            else:
                result = "WIN" if my_symbol == winner else "LOSS"
            print(f"Game Over! Result: {result}")
            if line:
                print(f"Winning line: {line}")
        else:
            print(f"Your turn ({game['turn']}).")
