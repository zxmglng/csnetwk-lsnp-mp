import time
import uuid
import config
from views.message import Message
from models.collections import my_profile
from models.collections.peers import Peers
from models.collections.groups import Groups
from models.dataclasses.group import Group

def run(args: list[str]):
    if len(args) < 2:
        peers = Peers().all()
        peer_ids = [peer.USER_ID for peer in peers]
        print("Available peers:", peer_ids)
        print("Usage: group_create <group_name> <member_user_ids_comma_separated>")
        return
    
    group_name = args[0]
    user_ids_str = args[1]  
    user_ids = [uid.strip() for uid in user_ids_str.split(",") if uid.strip()]
    
    groups_collection = Groups()
    group_id = f"{group_name}_{uuid.uuid4().hex[:5]}"
    
    profile = my_profile.get_profile()
    if not profile:
        return
        
    peers_collection = Peers()
    members = [profile]
    
    for user_id in user_ids:
        peer = peers_collection.get_peer(user_id)
        if peer:
            members.append(peer)
    
    if not members:
        return  
    
    new_group = Group(GROUP_ID=group_id, GROUP_NAME=group_name, MEMBERS=members)

    if groups_collection.add_group(new_group):
        print(f"[GROUP CREATED] {group_name} with ID {group_id} and members: {[p.USER_ID for p in members]}")
        
        timestamp = int(time.time())
        token_ttl = timestamp + 3600
        token = f"{profile.USER_ID}|{token_ttl}|group"
    
        members_str = ",".join(peer.USER_ID for peer in members)

        message_dict = {
            "TYPE": "GROUP_CREATE",
            "FROM": profile.USER_ID,
            "GROUP_ID": group_id,
            "GROUP_NAME": group_name,
            "MEMBERS": members_str,
            "TIMESTAMP": timestamp,
            "TOKEN": token
        }
        
        raw = Message.raw_message(message_dict)

        from udp_socket import UDPSocket
        for peer in members:
            UDPSocket().send(raw, (peer.IP, config.PORT))
        
        print("You’ve been added to", group_name)
