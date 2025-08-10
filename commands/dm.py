import time
import uuid
import config
from views.message import Message
from models.collections import my_profile
from models.collections.peers import Peers

def run(args: list[str]):
    
    if len(args) < 2:
        return
    
    target_user_id = args[0]
    content = " ".join(args[1:])
    
    profile = my_profile.get_profile()
    if not profile:
        return
    
    target_peer = Peers().get_peer(target_user_id)
    if not target_peer:
        return
    
    timestamp = int(time.time())
    token_ttl = timestamp + 3600
    token = f"{profile.USER_ID}|{token_ttl}|chat"
    
    message_dict = {
        "TYPE": "DM",
        "FROM": profile.USER_ID,
        "TO": target_user_id,
        "CONTENT": content,
        "TIMESTAMP": timestamp,
        "MESSAGE_ID": uuid.uuid4().hex[:8],
        "TOKEN": token
    }
    
    raw = Message.raw_message(message_dict)
    
    from udp_socket import UDPSocket
    UDPSocket().send(raw, (target_peer.IP, config.PORT))
    
    print(f"[DM Sent] to {target_user_id}: {content}")
    