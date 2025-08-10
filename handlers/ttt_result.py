from models.collections import ttt_game
from views.tictactoe import print_board
from verbose import vprint

def handle(data: dict):
    game_id = data.get("GAMEID")
    result = data.get("RESULT")
    winning_line = data.get("WINNING_LINE")

    if not game_id or not result:
        print("Invalid game result message received.")
        return

    game = ttt_game.get_game(game_id)
    if not game:
        print(f"Unknown game result received for game ID: {game_id}")
        return

    ttt_game.set_result(game_id, result, winning_line)

    vprint("RECV", f"Tic Tac Toe result for game {game_id}: {result}", msg_type="TICTACTOE_RESULT")
    print_board(game["board"])
    print(f"Game Over! Result: {result}")

    if winning_line:
        print(f"Winning line: {winning_line}")
