from models.collections import ttt_game
from views.tictactoe import print_board

def handle(message):
    game_id = message["GAMEID"]
    result = message["RESULT"]
    winning_line = message.get("WINNING_LINE")

    game = ttt_game.get_game(game_id)
    if not game:
        print("Unknown game result received.")
        return

    ttt_game.set_result(game_id, result, winning_line)
    print_board(game["board"])
    print(f"Game over: {result}")
