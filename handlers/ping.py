from views.message import Message
import config
from models.collections import my_profile

def run(data: dict, sender_address: tuple):
    from udp_socket import UDPSocket
    
    profile = my_profile.get_profile()
    if not profile:
        return
    
    user_id = data.get("USER_ID", "")
    
    profile_dict = profile.to_message_dict()
    profile_message = Message.raw_message(profile_dict)
    UDPSocket().send(profile_message, (config.BROADCAST_ADDRESS, config.PORT))