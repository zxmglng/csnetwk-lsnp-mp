from models.collections import my_profile, peers

def run(data: dict, sender_address: tuple):
    
    from_id = data.get("FROM", "")
    content = data.get("CONTENT", "")
    
    print(f"[DM] from {from_id}: {content}")