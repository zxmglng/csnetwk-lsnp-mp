import time
import uuid
import config
from verbose import vprint
from views.message import Message
from models.collections import my_profile
from models.collections.peers import Peers
from models.collections.following import Following

def run(args: list[str]):
    if len(args) < 1:
        peers = Peers().all()
        peer_ids = [peer.USER_ID for peer in peers]
        print("Available peers:", peer_ids)
        print("Usage: follow <target_user_id>")
        return    
    
    target_user_id = args[0]
    
    profile = my_profile.get_profile()
    if not profile:
        return
    
    target_peer = Peers().get_peer(target_user_id)
    if not target_peer:
        return
    
    timestamp = int(time.time())
    token_ttl = timestamp + 3600
    token = f"{profile.USER_ID}|{token_ttl}|follow"
    
    message_dict = {
        "TYPE": "FOLLOW",
        "MESSAGE_ID": uuid.uuid4().hex[:8],
        "FROM": profile.USER_ID,
        "TO": target_user_id,
        "TIMESTAMP": timestamp,
        "TOKEN": token
    }
    
    raw = Message.raw_message(message_dict)
    
    from udp_socket import UDPSocket
    UDPSocket().send(raw, (target_peer.IP, config.PORT))
    
    Following().add_following(target_peer)

    vprint("SEND", f"FOLLOW to {target_user_id}", sender_ip=target_peer.IP, msg_type="FOLLOW")
    print(f"[FOLLOW Sent] to {target_user_id}")