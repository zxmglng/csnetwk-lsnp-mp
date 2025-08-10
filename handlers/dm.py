from models.collections.peers import Peers
from verbose import vprint

def run(data: dict, sender_address: tuple):
    from_id = data.get("FROM", "")
    content = data.get("CONTENT", "")
    
    if not from_id:
        return
    
    peer = Peers().get_peer(from_id)
    
    if vprint("RECV", f"DM from {peer.DISPLAY_NAME} ({from_id}): {content}", sender_ip=sender_address[0], msg_type="DM"):
        print(f"{peer.DISPLAY_NAME}: {content}")
    

