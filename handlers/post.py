from models.collections.following import Following
from verbose import vprint

def run(data: dict, sender_address: tuple):
    user_id = data.get("USER_ID", "")
    content = data.get("CONTENT", "").strip()
    timestamp = data.get("TIMESTAMP", "")
    
    peer = Following().get_following(user_id)
    if not peer:
        return  
    
    Following().add_post(user_id, timestamp, content)

    if vprint("RECV", f"{peer.DISPLAY_NAME} sent: \"{content}\"", sender_ip=sender_address[0], msg_type="FOLLOW"):
        print(f"{peer.DISPLAY_NAME} sent: \"{content}\"")