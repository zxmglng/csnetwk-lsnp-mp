from logs.logger import logger
from models import store

"""
Handles the POST command from a client.

Args:
    message: A Message object containing the sender's address and the post content.

Returns:
    tuple:
        - A string confirmation showing the post and list of followers.
        - A list of (recipient_address, message) tuples for notifying followers.
"""
def run(message):
    author = store.get_username(message.address)
    text = message.content.strip()

    logger.info(f"{author} posted: {text}")
    
    # Get list of followers
    followers = store.get_followers(author)
    forwards = []

    # Notify each follower who is currently online
    for follower in followers:
        address = store.get_address(follower)
        if address:
            forwards.append((address, f"{author} posted: {text}"))

    response = f"{author} POSTED: {text} | Followers: {', '.join(followers) or 'none'}"
    return response, forwards
