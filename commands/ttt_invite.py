import time
from udp_socket import UDPSocket
import config
from models.collections import ttt_game
from models.collections.peers import Peers

def run(args):
    if len(args) < 2:
        peers = Peers().all()
        peer_ids = [peer.USER_ID for peer in peers]
        print("Available peers:", peer_ids)
        print("Usage: ttt_invite <target_user_id> <X|O>")
        return

    to_user = args[0]
    symbol = args[1].upper()
    if symbol not in ["X", "O"]:
        print("Symbol must be X or O")
        return

    game_id = f"g{len(ttt_game.games) % 256}"
    ttt_game.create_game(game_id,
                        player_x=config.USERNAME if symbol == "X" else to_user,
                        player_o=config.USERNAME if symbol == "O" else to_user)

    message = (
        f"TYPE: TICTACTOE_INVITE\n"
        f"FROM: {config.USERNAME}@{config.CURRENT_IP}\n"
        f"TO: {to_user}\n"
        f"GAMEID: {game_id}\n"
        f"MESSAGE_ID: msg{int(time.time())}\n"
        f"SYMBOL: {symbol}\n"
        f"TIMESTAMP: {int(time.time())}\n"
        f"TOKEN: {config.USERNAME}@{config.CURRENT_IP}|{int(time.time())+3600}|game"
    )

    UDPSocket().send(message, (to_user.split("@")[1], config.PORT))
    print(f"Invite sent to {to_user} — you are {symbol}")
