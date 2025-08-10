from models.collections.followers import Followers
from models.collections.my_posts import MyPosts  

def run(data: dict, sender_address: tuple):
    unliker_id = data.get("FROM", "")
    timestamp = data.get("TIMESTAMP")

    if not unliker_id or timestamp is None:
        return

    follower = Followers().get_follower(unliker_id)
    if not follower:
        return

    post = MyPosts().get_post(timestamp)
    if not post:
        return

    print(f"{follower.DISPLAY_NAME} unliked your post [{post.content}]")
