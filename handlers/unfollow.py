from models.collections.followers import Followers
from models.collections.peers import Peers

def run(data: dict, sender_address: tuple):
    from_id = data.get("FROM", "")

    if not from_id:
        return  
    
    peer = Peers().get_peer(from_id)

    Followers().remove_follower(from_id)
    print(f"User {peer.DISPLAY_NAME} has unfollowed you")
