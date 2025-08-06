from logs.logger import logger
from models import store

"""
Handles the FOLLOW command from a client.

Args:
    message: A Message object containing the sender's address and the target username.

Returns:
    tuple:
        - A string confirmation for the sender.
        - A list of (recipient_address, message) tuples for notifying the followed user.
"""
def run(message):
    target_user = message.content.strip()
    follower_address = message.address
    follower_username = store.get_username(follower_address)

    store.follow(follower_address, target_user)

    logger.info(f"{follower_username} followed {target_user}")

    target_address = store.get_address(target_user)
    forwards = []
    if target_address:
        notify_msg = f"{follower_username} just followed you."
        forwards.append((target_address, notify_msg))

    response = f"You are now following {target_user}."

    return response, forwards