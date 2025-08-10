import config
from models.dataclasses.peer import Peer
from views.message import Message
from models.collections import my_profile  

def run(args = None):
    from udp_socket import UDPSocket  
    display_name = input("Enter DISPLAY_NAME: ")
    status = input("Enter STATUS: ")

    profile = Peer(
        USER_ID = f"{config.USERNAME}@{config.CURRENT_IP}",
        DISPLAY_NAME = display_name,
        STATUS = status,
        IP = config.CURRENT_IP
    )
    
    my_profile.set_profile(profile)

    raw = Message.raw_message(profile.to_message_dict())
    
    UDPSocket().send(raw, (config.BROADCAST_ADDRESS, config.PORT))
    
    