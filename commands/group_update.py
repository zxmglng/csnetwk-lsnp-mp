import time
import config
from views.message import Message
from models.collections import my_profile
from models.collections.peers import Peers
from models.collections.groups import Groups

def run(args: list[str]):
    groups_collection = Groups()
    peers_collection = Peers()

    if len(args) < 3:
        print("Usage:")
        print("  group_update <group_id> add <user_ids_comma_separated>")
        print("  group_update <group_id> remove <user_ids_comma_separated>")
        return

    group_id = args[0]
    group = groups_collection.get_group(group_id)
    if not group:
        print(f"Group {group_id} not found.")
        return

    profile = my_profile.get_profile()
    if not profile or group.FROM != profile.USER_ID:
        print("Error: Only the group creator can modify membership.")
        return

    add_user_ids = []
    remove_user_ids = []

    i = 1
    while i < len(args):
        part = args[i].lower()
        if part == "add" and i + 1 < len(args):
            add_user_ids.extend(uid.strip() for uid in args[i + 1].split(",") if uid.strip())
            i += 2
        elif part == "remove" and i + 1 < len(args):
            remove_user_ids.extend(uid.strip() for uid in args[i + 1].split(",") if uid.strip())
            i += 2
        else:
            i += 1

    actually_added = []
    actually_removed = []

    for user_id in add_user_ids:
        if not any(m.USER_ID == user_id for m in group.MEMBERS):
            peer = peers_collection.get_peer(user_id)
            if peer:
                group.MEMBERS.append(peer)
                actually_added.append(user_id)

    group.MEMBERS = [m for m in group.MEMBERS if m.USER_ID not in remove_user_ids]
    actually_removed.extend(remove_user_ids)

    timestamp = int(time.time())
    token_ttl = timestamp + 3600
    token = f"{profile.USER_ID}|{token_ttl}|group"

    message_dict = {
        "TYPE": "GROUP_UPDATE",
        "FROM": profile.USER_ID,
        "GROUP_ID": group.GROUP_ID,
        "ADD": ",".join(actually_added),
        "REMOVE": ",".join(actually_removed),
        "TIMESTAMP": timestamp,
        "TOKEN": token
    }

    raw = Message.raw_message(message_dict)

    from udp_socket import UDPSocket
    for member in group.MEMBERS:
        UDPSocket().send(raw, (member.IP, config.PORT))

    print(f"Updated group '{group.GROUP_NAME}':")
    if actually_added:
        print(f"  Added: {', '.join(actually_added)}")
    if actually_removed:
        print(f"  Removed: {', '.join(actually_removed)}")
