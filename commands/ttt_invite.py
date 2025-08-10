import time
import uuid
import config
from verbose import vprint
from models.collections import ttt_game, my_profile
from models.collections.peers import Peers
from views.message import Message
from udp_socket import UDPSocket
from views.tictactoe import print_board

def run(args):
    if not args:
        peers = Peers().all()
        peer_ids = [p.USER_ID for p in peers]
        print("Available peers:", peer_ids)
        print("Usage: ttt_invite <target_user_id>")
        return

    target_user_id = args[0]
    profile = my_profile.get_profile()
    if not profile:
        print("No profile found.")
        return

    target_peer = Peers().get_peer(target_user_id)
    if not target_peer:
        print(f"Peer {target_user_id} not found.")
        return

    symbol = "X"  # Inviter always plays X
    now = int(time.time())
    token_ttl = now + 3600  # token valid for 1 hour

    game_id = f"g{len(ttt_game.games) % 256}"
    ttt_game.create_game(game_id, profile.USER_ID, target_user_id)

    token = f"{profile.USER_ID}|{token_ttl}|game"
    message = {
        "TYPE": "TICTACTOE_INVITE",
        "FROM": profile.USER_ID,
        "TO": target_user_id,
        "GAMEID": game_id,
        "MESSAGE_ID": uuid.uuid4().hex[:8],
        "SYMBOL": symbol,
        "TIMESTAMP": now,
        "TOKEN": token
    }

    raw_msg = Message.raw_message(message)

    UDPSocket().send(raw_msg, (target_peer.IP, config.PORT))
    if vprint("SEND", f"Tic Tac Toe invite to {target_user_id} — you are {symbol}", sender_ip=target_peer.IP, msg_type="TICTACTOE_INVITE"):
        print(f"[Invite sent] to {target_user_id} — you are {symbol}. GAMEID: {game_id}")

    print_board([" "] * 9)
