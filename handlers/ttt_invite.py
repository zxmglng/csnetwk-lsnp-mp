from models.collections import ttt_game
from views.tictactoe import print_board
from verbose import vprint
from models.collections import my_profile

def handle(message: dict):
    from_user = message.get("FROM")
    game_id = message.get("GAMEID")
    symbol = message.get("SYMBOL")
    to_user = message.get("TO")

    profile = my_profile.get_profile()
    if not profile:
        return

    my_symbol = "O" if symbol == "X" else "X"

    # Create the game entry
    ttt_game.create_game(
        game_id,
        player_x=from_user if symbol == "X" else profile.USER_ID,
        player_o=from_user if symbol == "O" else profile.USER_ID
    )

    vprint("RECV", f"Tic Tac Toe invite from {from_user} — you are {my_symbol}", msg_type="TICTACTOE_INVITE")
    print(f"{from_user} is inviting you to play Tic Tac Toe. You are {my_symbol}.")
    print_board([" "] * 9)
