from models import store

"""
Handles the REGISTER command from a client.

Args:
    message: A Message object containing the sender's address and the desired username.

Returns:
    str:
        - A success message if registration is successful.
        - An error message if the username is invalid or already taken.
"""
def run(message):
    username = message.content.strip()
    if not username:
        return "ERROR: Username cannot be empty."

    success = store.register(message.address, username)
    if not success:
        return f"ERROR: Username '{username}' is already taken."

    return f"SUCCESS: Registered as {username}"