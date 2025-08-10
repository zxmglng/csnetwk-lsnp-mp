from models.collections import ttt_game, my_profile
from views.tictactoe import print_board
from verbose import vprint

def handle(data: dict, sender_address: tuple):
    from_user = data.get("FROM")
    game_id = data.get("GAMEID")
    symbol = data.get("SYMBOL")

    profile = my_profile.get_profile()
    if not profile:
        return
    my_symbol = "O" if symbol == "X" else "X"
    # Create new game with correct player assignment
    ttt_game.create_game(
        game_id,
        player_x=from_user if symbol == "X" else profile.USER_ID,
        player_o=from_user if symbol == "O" else profile.USER_ID
    )
    if vprint("RECV", f"Tic Tac Toe invite from {from_user} — you are {my_symbol}", sender_ip=sender_address[0], msg_type="TICTACTOE_INVITE"):
        print(f"{from_user} invites you to play Tic Tac Toe. You are {my_symbol}. GAMEID: {game_id}")
    print_board([" "] * 9)