from views.message import Message
from handlers import profile, ping, dm, follow, unfollow, group_create, group_message

class HandleMessage:
    def __init__(self):
        self.type_router = {
            "PROFILE": profile.run,  
            "PING": ping.run,
            "DM": dm.run,
            "FOLLOW": follow.run,
            "UNFOLLOW": unfollow.run,
            "GROUP_CREATE": group_create.run,
            "GROUP_MESSAGE": group_message.run,
        }

    def run(self, message: str, sender_address: tuple):
        data = Message.parsed_message(message)
        msg_type = data.get("TYPE")

        handler = self.type_router.get(msg_type)
        if handler:
            handler(data, sender_address)
        else:
            print(f"[Warning] Unknown TYPE: {msg_type}")