from models.dataclasses.follower import Follower
from models.collections.followers import Followers
from models.collections.peers import Peers


def run(data: dict, sender_address: tuple):
    from_id = data.get("FROM", "")
    timestamp = data.get("TIMESTAMP", None)

    if not from_id:
        return  
    
    ip = sender_address[0]
    
    follower = Follower(
        FOLLOWER_ID=from_id,
        TIMESTAMP=timestamp,
        IP=ip
    )
    
    peer = Peers().get_peer(from_id)
    display_name = peer.DISPLAY_NAME if peer else from_id
    
    Followers().add_follower(follower)
    
    print(f"User {display_name} has followed you")