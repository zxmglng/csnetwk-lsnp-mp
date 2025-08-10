import time
import uuid
import config
from verbose import vprint
from udp_socket import UDPSocket
from models.collections import ttt_game
from models.collections.ttt_game import check_winner
from views.tictactoe import print_board
from views.message import Message
from models.collections.peers import Peers
from models.collections import my_profile

def run(args: list[str]):
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
        return

    game = ttt_game.get_game(game_id)
    if not game:
        print("Game not found.")
        return

    # Determine my symbol
    my_symbol = "X" if game["player_x"] == profile.USER_ID else "O"

    if game["turn"] != my_symbol:
        print("It's not your turn.")
        return

    if not ttt_game.make_move(game_id, position, my_symbol):
        print("Invalid move.")
        return

    now = int(time.time())
    token_ttl = now + 3600
    token = f"{profile.USER_ID}|{token_ttl}|game"

    # Determine opponent ID and peer
    opponent_id = game["player_o"] if my_symbol == "X" else game["player_x"]
    target_peer = Peers().get_peer(opponent_id)
    if not target_peer:
        print("Opponent not found in peer list.")
        return

    message_dict = {
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

    raw = Message.raw_message(message_dict)

    # Send move
    UDPSocket().send(raw, (target_peer.IP, config.PORT))
    vprint("SEND", f"Tic Tac Toe move to {opponent_id} — position {position}", sender_ip=target_peer.IP, msg_type="TICTACTOE_MOVE")
    print_board(game["board"])

    # Check winner
    winner, winning_line = check_winner(game_id)
    if winner:
        result = "DRAW" if winner == "DRAW" else ("WIN" if my_symbol == winner else "LOSS")
        print(f"Game Over! Result: {result}")
        if winning_line:
            print(f"Winning line: {winning_line}")
