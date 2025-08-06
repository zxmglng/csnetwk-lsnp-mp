from logs.logger import logger
from models import store

"""
Handles the DM (Direct Message) command from a client.
Args:
    message: A Message object containing the sender's address and the raw message content.

Returns:
    tuple:
        - A string confirmation for the sender or an error message.
        - A list of (recipient_address, message) tuples for forwarding the DM.
"""
def run(message):
    try:
        parts = message.content.strip().split(maxsplit=1)
        to_user = parts[0]
        text = parts[1] if len(parts) > 1 else ""

        from_user = store.get_username(message.address)
        to_address = store.get_address(to_user)

        if not to_address:
            return f"User {to_user} not found.", []

        logger.info(f"{from_user} sent DM to {to_user}: {text}")
        return f"DM to {to_user} from {from_user}: {text}", [(to_address, f"DM from {from_user}: {text}")]
    except Exception as e:
        logger.error(f"DM command failed: {e}")
        return "Usage: DM <username> <message>", []
