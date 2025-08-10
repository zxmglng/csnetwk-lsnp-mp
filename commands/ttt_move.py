import time
from udp_socket import UDPSocket
import config
from models.collections import ttt_game
from models.collections.ttt_game import check_winner
from views.tictactoe import print_board

def run(args):
    if len(args) < 2:
        print("Usage: ttt_move <GAMEID> <POSITION>")
        return

    game_id = args[0]
    position = int(args[1])
    game = ttt_game.get_game(game_id)
    if not game:
        print("Game not found.")
        return

    # Determine my symbol
    my_symbol = "X" if game["player_x"] == config.USERNAME else "O"

    if game["turn"] != my_symbol:
        print("It's not your turn.")
        return

    if not ttt_game.make_move(game_id, position, my_symbol):
        print("Invalid move.")
        return

    message = (
        f"TYPE: TICTACTOE_MOVE\n"
        f"FROM: {config.USERNAME}@{config.CURRENT_IP}\n"
        f"TO: {game['player_o']}@{config.CURRENT_IP if my_symbol=='X' else game['player_x']}\n"
        f"GAMEID: {game_id}\n"
        f"MESSAGE_ID: msg{int(time.time())}\n"
        f"POSITION: {position}\n"
        f"SYMBOL: {my_symbol}\n"
        f"TURN: {position}\n"
        f"TOKEN: {config.USERNAME}@{config.CURRENT_IP}|{int(time.time())+3600}|game"
    )

    UDPSocket().send(message, (game["player_o"].split("@")[1] if my_symbol=="X" else game["player_x"].split("@")[1], config.PORT))
    print_board(game["board"])

    winner, winning_line = check_winner(game_id)
    if winner:
        result = "DRAW" if winner == "DRAW" else ("WIN" if symbol == winner else "LOSS")
        print(f"Game Over! Result: {result}")
        if winning_line:
            print(f"Winning line: {winning_line}")
        return
