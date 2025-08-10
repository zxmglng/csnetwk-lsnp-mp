import time
import config
from views.message import Message
from models.collections import my_profile
from models.collections.peers import Peers


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

    
def auto_ping_loop():
    while True:
        time.sleep(PING_INTERVAL)
        Peers().reset_collection()
        _send_ping()