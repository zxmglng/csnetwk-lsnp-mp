from verbose import vprint
from models.collections.followers import Followers
from models.collections.my_posts import MyPosts  

def run(data: dict, sender_address: tuple):
    liker_id = data.get("FROM", "")
    timestamp = data.get("TIMESTAMP")

    if not liker_id or timestamp is None:
        return

    follower = Followers().get_follower(liker_id)
    if not follower:
        return

    post = MyPosts().get_post(timestamp)
    if not post:
        return

    if vprint("RECV", f"{follower.DISPLAY_NAME} likes your post [{post.content}]", sender_ip=sender_address[0], msg_type="LIKE"):
        print(f"{follower.DISPLAY_NAME} likes your post [{post.content}]")
