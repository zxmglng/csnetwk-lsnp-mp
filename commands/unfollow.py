from logs.logger import logger
from models import store

"""
Handles the UNFOLLOW command from a client.

Args:
    message: A Message object containing the sender's address and the username to unfollow.

Returns:
    tuple:
        - A string confirmation for the sender.
        - A list of (recipient_address, message) tuples for notifying the unfollowed user.
"""
def run(message):
    target_user = message.content.strip()
    store.unfollow(message.address, target_user)
    
    follower = store.get_username(message.address)
    unfollowed_address = store.get_address(target_user)

    logger.info(f"{follower} unfollowed {target_user}")

    forwards = []
    if unfollowed_address:
        forwards.append((unfollowed_address, f"{follower} has unfollowed you."))

    return f"You have unfollowed {target_user}.", forwards