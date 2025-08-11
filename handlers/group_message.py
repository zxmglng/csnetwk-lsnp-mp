from models.collections import my_profile
from models.collections.groups import Groups
from views.message import Message
import config
import time
import uuid

def run(data: dict, sender_address: tuple):
    """Handle incoming group message relay"""
    try:

        from udp_socket import UDPSocket
        
        group_id = data.get("GROUP_ID")
        content = data.get("CONTENT")
        from_id = data.get("FROM")
        
        if not all([group_id, content, from_id]):
            return

        group = Groups().get_group(group_id)
        if not group or not any(m.USER_ID == from_id for m in group.MEMBERS):
            return

        message_dict = {
            "TYPE": "GROUP_MESSAGE",
            "FROM": from_id,
            "GROUP_ID": group_id,
            "CONTENT": content,
            "TIMESTAMP": int(time.time()),
            "MESSAGE_ID": uuid.uuid4().hex[:8],
            "TOKEN": f"{from_id}|{int(time.time()) + 3600}|group"
        }

        raw = Message.raw_message(message_dict)
        for member in group.MEMBERS:
            if member.USER_ID != from_id:
                UDPSocket().send(raw, (member.IP, config.PORT))

        print(f"[Group {group_id}] {from_id}: {content}")

    except Exception as e:
        print(f"Group message handler error: {str(e)}")
