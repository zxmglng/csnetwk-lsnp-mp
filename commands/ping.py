import time
import config
from views.message import Message
from models.collections import my_profile

PING_INTERVAL = 300

def _send_ping():
    from udp_socket import UDPSocket
    profile = my_profile.get_profile()
    if not profile:
        return

    message_dict = {
        "TYPE": "PING",
        "USER_ID": profile.USER_ID,
    }

    raw = Message.raw_message(message_dict)
    UDPSocket().send(raw, (config.BROADCAST_ADDRESS, config.PORT))

    profile_dict = profile.to_message_dict()
    profile_message = Message.raw_message(profile_dict)
    UDPSocket().send(profile_message, (config.BROADCAST_ADDRESS, config.PORT))
    
def auto_ping_loop():
    while True:
        time.sleep(PING_INTERVAL)
        _send_ping()