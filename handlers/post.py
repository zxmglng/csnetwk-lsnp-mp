from models.collections.following import Following

def run(data: dict, sender_address: tuple):
    user_id = data.get("USER_ID", "")
    content = data.get("CONTENT", "").strip()
    
    peer = Following().get_following(user_id)
    if not peer:
        return  
    
    print(f"{peer.DISPLAY_NAME} sent: \"{content}\"")