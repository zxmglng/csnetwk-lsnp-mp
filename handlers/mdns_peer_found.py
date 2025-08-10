from models.collections.peers import Peers
from models.dataclasses.peer import Peer

def run(peer):
    peers_collection = Peers()
    new_peer = Peer(
        USER_ID = peer.peer_id,
        DISPLAY_NAME = peer.display_name,
        STATUS = "Online",
        AVATAR_TYPE = None,
        AVATAR_ENCODING = None,
        AVATAR_DATA = None,
        IP = peer.ip
    )
    peers_collection.add_peer(new_peer)
    print(f"[mDNS Handler] Found new peer: {peer.display_name} ({peer.peer_id}) @ {peer.ip}:{peer.port}")
