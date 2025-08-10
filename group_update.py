import time
import uuid
import config
from views.message import Message
from models.collections import my_profile
from models.collections.peers import Peers
from models.collections.groups import Groups

def run(args: list[str]):
    groups_collection = Groups()
    peers_collection = Peers()

    if len(args) < 3:
        groups = groups_collection.all()
        print("Available groups and their members:")
        for group in groups:
            member_ids = [member.USER_ID for member in group.MEMBERS]
            print(f"Group ID: {group.GROUP_ID}, Members: {member_ids}")

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
    
    if "add" in args:
        add_index = args.index("add")
        if add_index + 1 < len(args):
            add_user_ids = args[add_index + 1].split(",")
    
    if "remove" in args:
        remove_index = args.index("remove")
        if remove_index + 1 < len(args):
            remove_user_ids = args[remove_index + 1].split(",")

    profile = my_profile.get_profile()
    if not profile or profile.USER_ID != group.FROM:
        print("You are not authorized to update this group.")
        return

    # Update group members
    for user_id in add_user_ids:
        peer = peers_collection.get_peer(user_id.strip())
        if peer and peer not in group.MEMBERS:
            group.MEMBERS.append(peer)

    for user_id in remove_user_ids:
        peer = peers_collection.get_peer(user_id.strip())
        if peer in group.MEMBERS:
            group.MEMBERS.remove(peer)

    # Save updated group
    groups_collection.update_group(group)

    timestamp = int(time.time())
    token_ttl = timestamp + 3600
    token = f"{profile.USER_ID}|{token_ttl}|group"

    message_dict = {
        "TYPE": "GROUP_UPDATE",
        "FROM": profile.USER_ID,
        "GROUP_ID": group_id,
        "ADD": ",".join(add_user_ids),
        "REMOVE": ",".join(remove_user_ids),
        "TIMESTAMP": timestamp,
        "TOKEN": token
    }

    raw = Message.raw_message(message_dict)
    for member in group.MEMBERS:
        if member.USER_ID != profile.USER_ID:
            from udp_socket import UDPSocket
            UDPSocket().send(raw, (member.IP, config.PORT))

    print(f'The group "{group.GROUP_NAME}" member list was updated.')
