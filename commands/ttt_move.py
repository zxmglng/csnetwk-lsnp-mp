import time
import uuid
import config
from verbose import vprint
from udp_socket import UDPSocket
from models.collections import ttt_game, my_profile
from models.collections.peers import Peers
from views.message import Message
from views.tictactoe import print_board
from models.collections.ttt_game import check_winner

def run(args):
    if len(args) < 2:
        print("Usage: ttt_move <GAMEID> <POSITION>")
        return

    game_id = args[0]
    try:
        position = int(args[1])
    except ValueError:
        print("Position must be an integer.")
        return

    profile = my_profile.get_profile()
    if not profile:
        print("Profile not found.")
        return

    game = ttt_game.get_game(game_id)
    if not game:
        print("Game not found.")
        return

    my_symbol = "X" if game["player_x"] == profile.USER_ID else "O"

    if game["turn"] != my_symbol:
        print("It's not your turn.")
        return

    if not ttt_game.make_move(game_id, position, my_symbol):
        print("Invalid move.")
        return

    now = int(time.time())
    token = f"{profile.USER_ID}|{now + 3600}|game"

    opponent_id = game["player_o"] if my_symbol == "X" else game["player_x"]
    target_peer = Peers().get_peer(opponent_id)
    if not target_peer:
        print("Opponent not found.")
        return

    message = {
        "TYPE": "TICTACTOE_MOVE",
        "FROM": profile.USER_ID,
        "TO": opponent_id,
        "GAMEID": game_id,
        "MESSAGE_ID": uuid.uuid4().hex[:8],
        "POSITION": position,
        "SYMBOL": my_symbol,
        "TURN": my_symbol,
        "TIMESTAMP": now,
        "TOKEN": token
    }

    raw_msg = Message.raw_message(message)
    UDPSocket().send(raw_msg, (target_peer.IP, config.PORT))
    vprint("SEND", f"Tic Tac Toe move to {opponent_id} — position {position}", sender_ip=target_peer.IP, msg_type="TICTACTOE_MOVE")

    print_board(game["board"])

    winner, winning_line = check_winner(game_id)
    if winner:
        result = "DRAW" if winner == "DRAW" else ("WIN" if my_symbol == winner else "LOSS")
        print(f"Game Over! Result: {result}")
        if winning_line:
            print(f"Winning line: {winning_line}")
