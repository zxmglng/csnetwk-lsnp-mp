import time
import uuid
import config
from verbose import vprint
from views.message import Message
from models.collections import my_profile
from models.collections.groups import Groups
from views.message import Message
from udp_socket import UDPSocket

def run(args: list[str]):
    """Send a message to a group"""
    if len(args) < 2:
        print("Usage: group_message <group_id> <message>")
        return

    group_id = args[0]
    content = " ".join(args[1:])
    profile = my_profile.get_profile()
    
    if not profile or not content:
        return

    group = Groups().get_group(group_id)
    if not group or not any(m.USER_ID == profile.USER_ID for m in group.MEMBERS):
        print("Error: Not a group member")
        return

    message_dict = {
        "TYPE": "GROUP_MESSAGE",
        "FROM": profile.USER_ID,
        "GROUP_ID": group_id,
        "CONTENT": content,
        "TIMESTAMP": int(time.time()),
        "MESSAGE_ID": uuid.uuid4().hex[:8],
        "TOKEN": f"{profile.USER_ID}|{int(time.time()) + 3600}|group"
    }

    raw = Message.raw_message(message_dict)
    for member in group.MEMBERS:
        if member.USER_ID != profile.USER_ID:
            UDPSocket().send(raw, (member.IP, config.PORT))

    if vprint("SEND", f"GROUP_MESSAGE sent to {member.USER_ID} ({member.IP}) in group {group_id}: {content}", sender_ip=member.IP, msg_type="GROUP_MESSAGE"):
        print(f"You sent to group {group_id}: {content}")
