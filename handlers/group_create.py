from models.collections.peers import Peers
from models.collections.groups import Groups
from models.dataclasses.group import Group

def run(data: dict, sender_address: tuple):
    group_id = data.get("GROUP_ID", "")
    group_name = data.get("GROUP_NAME", "")
    members_str = data.get("MEMBERS", "")
    
    if not group_id or not group_name or not members_str:
        return  
    
    user_ids = [uid.strip() for uid in members_str.split(",") if uid.strip()]
    
    peers_collection = Peers()
    members = []
    for user_id in user_ids:
        peer = peers_collection.get_peer(user_id)
        if peer:
            members.append(peer)
    
    if not members:
        return  
    
    groups_collection = Groups()
    existing_group = groups_collection.get_group(group_id)
    if existing_group:
        return  
    
    new_group = Group(GROUP_ID=group_id, GROUP_NAME=group_name, MEMBERS=members)
    groups_collection.add_group(new_group)
    
    print(f'You\'ve been added to "{group_name}"')
 