from models.collections import ttt_game
from views.tictactoe import print_board
from models.collections.ttt_game import check_winner

def handle(message):
    game_id = message["GAMEID"]
    position = int(message["POSITION"])
    symbol = message["SYMBOL"]

    game = ttt_game.get_game(game_id)
    if not game:
        print(f"Received move for unknown game {game_id}.")
        return

    if ttt_game.make_move(game_id, position, symbol):
        print_board(game["board"])
        winner, winning_line = check_winner(game_id)
        if winner:
            result = "DRAW" if winner == "DRAW" else ("WIN" if symbol == winner else "LOSS")
            print(f"Game Over! Result: {result}")
            if winning_line:
                print(f"Winning line: {winning_line}")
            return
        print(f"Your turn ({game['turn']}).")
