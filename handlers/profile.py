from models.dataclasses.peer import Peer
from models.collections.peers import Peers
from verbose import vprint

def run(data: dict, sender_address: tuple):
    peer = Peer(
        USER_ID = data.get("USER_ID", ""),
        DISPLAY_NAME = data.get("DISPLAY_NAME", ""),
        STATUS = data.get("STATUS", ""),
        AVATAR_TYPE = data.get("AVATAR_TYPE"),
        AVATAR_ENCODING = data.get("AVATAR_ENCODING"),
        AVATAR_DATA = data.get("AVATAR_DATA"),
        IP = sender_address[0]
    )

    Peers().add_peer(peer)

    if vprint("RECV", f"{peer.DISPLAY_NAME} {peer.STATUS}", sender_ip=sender_address[0], msg_type="PROFILE"):
        print(f"{peer.DISPLAY_NAME} {peer.STATUS}")