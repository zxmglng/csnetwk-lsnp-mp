import time
import uuid
import config
from views.message import Message
from models.collections import my_profile
from models.collections.followers import Followers

def run(args: list[str]):
    if len(args) < 1:
        print("Usage: post <message content>")
        return
    
    content = " ".join(args).strip()
    if not content:
        return
    
    profile = my_profile.get_profile()
    if not profile:
        print("No profile found.")
        return
    
    timestamp = int(time.time())
    ttl = 3600  
    expire_time = timestamp + ttl
    token = f"{profile.USER_ID}|{expire_time}|broadcast"
    message_id = uuid.uuid4().hex[:8]
    
    message_dict = {
        "TYPE": "POST",
        "USER_ID": profile.USER_ID,
        "CONTENT": content,
        "TTL": ttl,
        "MESSAGE_ID": message_id,
        "TOKEN": token,
        "TIMESTAMP": timestamp
    }
    
    raw = Message.raw_message(message_dict)
    
    from udp_socket import UDPSocket
    followers = Followers().all()
    
    if not followers:
        return
    
    for follower in followers:
        UDPSocket().send(raw, (follower.IP, config.PORT))
    
    print(f"[POST Sent] to {len(followers)} followers: \"{content}\"")
