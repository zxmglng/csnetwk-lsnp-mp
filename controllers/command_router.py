from commands import post, dm, follow, unfollow, register
from models import store

class CommandRouter:
    def __init__(self):
        self.commands = {
            'POST': post.run,
            'DM': dm.run,
            'FOLLOW': follow.run,
            'UNFOLLOW': unfollow.run,
            'REGISTER': register.run
        }

    def route(self, message):
        parts = message.content.strip().split(maxsplit=1)
        command = parts[0].upper()
        message.content = parts[1] if len(parts) > 1 else ""

        if command != "REGISTER" and message.address not in store.users:
            store.register(message.address, f"user{message.address[1]}")

        if command in self.commands:
            result = self.commands[command](message)

            if isinstance(result, tuple):
                return result
            else:
                return (result, [])
    
        return (f"ERROR: Unknown command '{command}'", [])