from models.collections.peers import Peers
from models.collections.groups import Groups
from models.collections import my_profile
from views.message import Message
import time
import uuid
import config

def run(data: dict, sender_address: tuple):
    group_id = data.get("GROUP_ID", "")
    content = data.get("CONTENT", "")
    
    if not group_id or not content:
        print("Error: Missing 'GROUP_ID' or 'CONTENT' in the data.")
        return
    
    profile = my_profile.get_profile()
    if not profile:
        print("Error: Profile not found.")
        return

    group = Groups().get_group(group_id)
    if not group:
        print(f"Group {group_id} not found.")
        return
    
    timestamp = int(time.time())
    token_ttl = timestamp + 3600
    token = f"{profile.USER_ID}|{token_ttl}|group"

    message_dict = {
        "TYPE": "GROUP_MESSAGE",
        "FROM": profile.USER_ID,
        "GROUP_ID": group_id,
        "CONTENT": content,
        "TIMESTAMP": timestamp,
        "MESSAGE_ID": uuid.uuid4().hex[:8],
        "TOKEN": token
    }

    raw = Message.raw_message(message_dict)
    from udp_socket import UDPSocket
    for member in group.MEMBERS:
        if member.USER_ID != profile.USER_ID:
            UDPSocket().send(raw, (member.IP, config.PORT))

    print(f"{profile.USER_ID} sent \"{content}\"")
