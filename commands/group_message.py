import time
import uuid
import config
from views.message import Message
from models.collections import my_profile
from models.collections.peers import Peers
from models.collections.groups import Groups

def run(args: list[str]):
    if len(args) < 2:
        groups_collection = Groups()
        group_ids = [group.GROUP_ID for group in groups_collection.all()]
        print("Available groups:", group_ids)
        print("Usage: group_message <group_id> <message content>")
        return

    group_id = args[0]
    content = " ".join(args[1:]).strip()
    
    if not content:
        return
    
    profile = my_profile.get_profile()
    if not profile:
        return

    group = Groups().get_group(group_id)
    if not group:
        return
    
    timestamp = int(time.time())
    token_ttl = timestamp + 3600
    token = f"{profile.USER_ID}|{token_ttl}|group"

    message_dict = {
        "TYPE": "GROUP_MESSAGE",
        "MESSAGE_ID": uuid.uuid4().hex[:8],
        "FROM": profile.USER_ID,
        "GROUP_ID": group_id,
        "CONTENT": content,
        "TIMESTAMP": timestamp,
        "TOKEN": token
    }

    raw = Message.raw_message(message_dict)
    from udp_socket import UDPSocket
    for member in group.MEMBERS:
        if member.USER_ID != profile.USER_ID:
            UDPSocket().send(raw, (member.IP, config.PORT))

    print(f"[GROUP_MESSAGE Sent] to group {group.GROUP_NAME} ({group_id}): {content}")