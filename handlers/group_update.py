from models.collections.groups import Groups
from models.collections.peers import Peers
from models.collections import my_profile
from views.message import Message
import config
from udp_socket import UDPSocket

def run(data: dict, sender_address: tuple):
    """Process incoming GROUP_UPDATE network messages"""

    required_fields = ["FROM", "GROUP_ID", "ADD", "REMOVE", "TIMESTAMP", "TOKEN"]
    if not all(field in data for field in required_fields):
        return
    
    groups = Groups()
    peers = Peers()
    
    group = groups.get_group(data["GROUP_ID"])
    if not group:
        return

    if data["FROM"] != group.FROM:
        return

    added = [uid.strip() for uid in data["ADD"].split(",")] if data["ADD"] else []
    removed = [uid.strip() for uid in data["REMOVE"].split(",")] if data["REMOVE"] else []
    
    actual_adds = []
    for user_id in added:
        peer = peers.get_peer(user_id)
        if peer and peer not in group.MEMBERS:
            group.MEMBERS.append(peer)
            actual_adds.append(user_id)
    
    original_count = len(group.MEMBERS)
    group.MEMBERS = [m for m in group.MEMBERS if m.USER_ID not in removed]
    actual_removes = [uid for uid in removed if original_count != len(group.MEMBERS)]
    
    if not (actual_adds or actual_removes):
        return
    
    groups.update_group(group)
    
    print(f'The group "{group.GROUP_NAME}" member list was updated.')

    if config.DEBUG:
        if actual_adds:
            print(f"[DEBUG] Added: {', '.join(actual_adds)}")
        if actual_removes:
            print(f"[DEBUG] Removed: {', '.join(actual_removes)}")
