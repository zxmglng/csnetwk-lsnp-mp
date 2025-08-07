from commands.profile import run as handle_profile

def run(data: dict, sender_address: tuple):
    user_id = data.get("USER_ID", "")
    print(f"[PING Received] from {user_id}")