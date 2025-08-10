from models.collections.following import Following

def run(data: dict, sender_address: tuple):
    user_id = data.get("USER_ID", "")
    content = data.get("CONTENT", "").strip()
    timestamp = data.get("TIMESTAMP", "")
    
    peer = Following().get_following(user_id)
    if not peer:
        return  
    
    Following().add_post(user_id, timestamp, content)
    print(f"{peer.DISPLAY_NAME} sent: \"{content}\"")