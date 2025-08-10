from models.collections.peers import Peers

def run(data: dict, sender_address: tuple):
    from_id = data.get("FROM", "")
    content = data.get("CONTENT", "")
    
    if not from_id:
        return
    
    peer = Peers().get_peer(from_id)
    print(f"{peer.DISPLAY_NAME}: {content}")
