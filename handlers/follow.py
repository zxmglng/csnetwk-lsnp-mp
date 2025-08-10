from verbose import vprint
from models.collections.followers import Followers
from models.collections.peers import Peers


def run(data: dict, sender_address: tuple):
    from_id = data.get("FROM", "")
    if not from_id:
        return  
    
    peer = Peers().get_peer(from_id)
    Followers().add_follower(peer)
    
    if vprint("RECV", f"FOLLOW from {peer.DISPLAY_NAME} ({from_id})", sender_ip=sender_address[0], msg_type="FOLLOW"):
        print(f"User {peer.DISPLAY_NAME} has followed you")
    