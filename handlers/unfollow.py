from models.collections.followers import Followers
from models.collections.peers import Peers
from verbose import vprint

def run(data: dict, sender_address: tuple):
    from_id = data.get("FROM", "")

    if not from_id:
        return  
    
    peer = Peers().get_peer(from_id)
    
    Followers().remove_follower(from_id)

    vprint("RECV", f"UNFOLLOW from {peer.DISPLAY_NAME} ({from_id})", sender_ip=sender_address[0], msg_type="UNFOLLOW")
    print(f"User {peer.DISPLAY_NAME} has unfollowed you")
