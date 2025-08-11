import time
from views.message import Message
from models.collections import my_profile
from models.collections.following import Following
import config
from udp_socket import UDPSocket
from verbose import vprint

def run(args: list[str]):
    following_collection = Following()

    if len(args) != 2:
        print("Usage: unlike <user_id> <post_timestamp>")
        print("\nUsers with posts and their timestamps and contents:")

        for user_id in following_collection.get_all_users_with_posts():
            posts = following_collection.posts_dict.get(user_id, [])
            if not posts:
                continue
            print(f"User: {user_id}")
            for post in posts:
                ts = post["timestamp"]
                content = post.get("content", "")
                print(f"  Timestamp: {ts}, Content: \"{content}\"")
        return

    user_id = args[0]
    post_timestamp_str = args[1]

    try:
        post_timestamp = int(post_timestamp_str)
    except ValueError:
        return

    profile = my_profile.get_profile()
    if not profile:
        return

    unliked = following_collection.unlike_post(user_id, post_timestamp)
    if not unliked:
        return

    timestamp_now = int(time.time())
    token_ttl = timestamp_now + 3600
    token = f"{profile.USER_ID}|{token_ttl}|broadcast"

    to_peer = following_collection.get_following(user_id)
    if not to_peer:
        return

    message_dict = {
        "TYPE": "UNLIKE",
        "FROM": profile.USER_ID,
        "TO": to_peer.USER_ID,
        "POST_TIMESTAMP": post_timestamp,
        "ACTION": "UNLIKE",
        "TIMESTAMP": timestamp_now,
        "TOKEN": token
    }

    raw = Message.raw_message(message_dict)
    UDPSocket().send(raw, (to_peer.IP, config.PORT))

    if vprint("SEND", f"UNLIKE message sent to {to_peer.USER_ID} ({to_peer.IP}) for post at timestamp {post_timestamp}", sender_ip=to_peer.IP, msg_type="UNLIKE"):
        print(f"Sent UNLIKE for post from {user_id} at timestamp {post_timestamp} to {to_peer.USER_ID}")
