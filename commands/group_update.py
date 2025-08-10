import time
import uuid
import config
from views.message import Message
from models.collections import my_profile
from models.collections.peers import Peers
from models.collections.groups import Groups
from models.dataclasses.group import Group

def run(args: list[str]):
    groups_collection = Groups()
    peers_collection = Peers()

    if len(args) < 3:
        group_ids = [group.GROUP_ID for group in groups_collection.all()]
        print("Available group IDs:", group_ids)

        peer_ids = [peer.USER_ID for peer in peers_collection.all()]
        print("Available peers:", peer_ids)

        print("Usage:")
        print("group_update <group_id> add <user_ids_comma_separated>")
        print("group_update <group_id> remove <user_ids_comma_separated>")
        print("group_update <group_id> add <user_ids_comma_separated> remove <user_ids_comma_separated>")
        return

    group_id = args[0]
    group = groups_collection.get_group(group_id)
    if not group:
        print(f"Group {group_id} not found.")
        return

    add_user_ids = []
    remove_user_ids = []

    i = 1
    while i < len(args):
        part = args[i].lower()
        if part == "add" and i + 1 < len(args):
            add_user_ids = [uid.strip() for uid in args[i + 1].split(",") if uid.strip()]
            i += 2
        elif part == "remove" and i + 1 < len(args):
            remove_user_ids = [uid.strip() for uid in args[i + 1].split(",") if uid.strip()]
            i += 2
        else:
            i += 1

    profile = my_profile.get_profile()
    if not profile:
        return

    actually_added = []
    actually_removed = []

    for user_id in add_user_ids:
        if any(m.USER_ID == user_id for m in group.MEMBERS):
            continue
        peer = peers_collection.get_peer(user_id)
        if peer:
            group.MEMBERS.append(peer)
            actually_added.append(user_id)

    new_members = []
    for m in group.MEMBERS:
        if m.USER_ID in remove_user_ids:
            actually_removed.append(m.USER_ID)
        else:
            new_members.append(m)
    group.MEMBERS = new_members

    print(f"Members now: {[m.USER_ID for m in group.MEMBERS]}")

    timestamp = int(time.time())
    token_ttl = timestamp + 3600
    token = f"{profile.USER_ID}|{token_ttl}|group"

    members_str = ",".join(m.USER_ID for m in group.MEMBERS)
    add_str = ",".join(actually_added)
    remove_str = ",".join(actually_removed)

    message_dict = {
        "TYPE": "GROUP_UPDATE",
        "FROM": profile.USER_ID,
        "GROUP_ID": group.GROUP_ID,
        "ADD": add_str,
        "REMOVE": remove_str,
        "TIMESTAMP": timestamp,
        "TOKEN": token
    }

    raw = Message.raw_message(message_dict)

    from udp_socket import UDPSocket
    for member in group.MEMBERS:
        UDPSocket().send(raw, (member.IP, config.PORT))
        
    for user_id in actually_removed:
        peer = peers_collection.get_peer(user_id)
        if peer:
            UDPSocket().send(raw, (peer.IP, config.PORT))

    print(f"[GROUP_UPDATE Sent] to members: {members_str}")
