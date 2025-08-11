from models.collections import my_profile
from models.collections.groups import Groups
from views.message import Message
from udp_socket import UDPSocket
import config
import time
import uuid

def run(data: dict, sender_address: tuple):
    """Handle incoming group messages and relay them to group members"""
    
    group_id = data.get("GROUP_ID")
    from_id = data.get("FROM")
    content = data.get("CONTENT")
    
    if not all([group_id, from_id, content]):
        print("Error: Missing required message fields (GROUP_ID, FROM, CONTENT)")
        return

    groups = Groups()
    group = groups.get_group(group_id)
    if not group:
        print(f"Error: Group {group_id} not found")
        return

    # Verify sender is a group member
    sender_in_group = any(member.USER_ID == from_id for member in group.MEMBERS)
    if not sender_in_group:
        print(f"Error: User {from_id} is not a member of group {group_id}")
        return
        
    print(f"[Group {group_id}] {from_id}: {content}")


    message_dict = {
        "TYPE": "GROUP_MESSAGE",
        "FROM": from_id,
        "GROUP_ID": group_id,
        "CONTENT": content,
        "TIMESTAMP": int(time.time()),
        "MESSAGE_ID": uuid.uuid4().hex[:8],
        "TOKEN": f"{from_id}|{int(time.time()) + 3600}|group"
    }

    raw_message = Message.raw_message(message_dict)
    for member in group.MEMBERS:
        if member.USER_ID != from_id:  
            try:
                UDPSocket().send(raw_message, (member.IP, config.PORT))
            except Exception as e:
                print(f"Error sending to {member.USER_ID}: {str(e)}")
