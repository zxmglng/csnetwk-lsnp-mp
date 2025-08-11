from models.collections.peers import Peers
from models.collections.groups import Groups
from models.dataclasses.group import Group
from models.collections import my_profile
from verbose import vprint

def run(data: dict, sender_address: tuple):
    group_id = data.get("GROUP_ID", "")
    group_name = data.get("GROUP_NAME", "")
    members_str = data.get("MEMBERS", "")
    
    if not group_id or not group_name or not members_str:
        return  
    
    user_ids = [uid.strip() for uid in members_str.split(",") if uid.strip()]
    peers_collection = Peers()

    profile = my_profile.get_profile()
    if not profile:
        return
    
    members = [profile]
    for user_id in user_ids:
        peer = peers_collection.get_peer(user_id)
        if peer:
            members.append(peer)
    
    print(members)
    if not members:
        return  
    
    groups_collection = Groups()
    existing_group = groups_collection.get_group(group_id)
    if existing_group:
        return  
        
    new_group = Group(GROUP_ID=group_id, GROUP_NAME=group_name, MEMBERS=members)
    groups_collection.add_group(new_group)
    
    if vprint("RECV", f'Added to group "{group_name}" (ID: {group_id}) with members: {[p.USER_ID for p in members]}', sender_ip=sender_address[0], msg_type="GROUP_CREATE"):
        print(f'You\'ve been added to "{group_name}"')
 