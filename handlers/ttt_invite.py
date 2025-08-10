from models.collections import ttt_game
from views.tictactoe import print_board

def handle(message):
    from_user = message["FROM"]
    game_id = message["GAMEID"]
    symbol = message["SYMBOL"]

    my_symbol = "O" if symbol == "X" else "X"
    ttt_game.create_game(game_id,
                        player_x=from_user if symbol == "X" else message["TO"],
                        player_o=from_user if symbol == "O" else message["TO"],
                        turn=symbol)

    print(f"{from_user} is inviting you to play tic-tac-toe. You are {my_symbol}.")
    print_board([" "] * 9)
