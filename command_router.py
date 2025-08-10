from commands import profile, dm, follow, unfollow, group_create

COMMANDS = {
    "profile": profile.run,
    "dm": dm.run,
    "follow": follow.run,
    "unfollow": unfollow.run,
    "group_create": group_create.run
}

def send(command: str, args: list[str]):
    cmd = command.lower()
    
    if cmd in COMMANDS:
        try:
            COMMANDS[cmd](args)
        except Exception as e:
            print(f"Error executing '{cmd}': {e}")
    else:
        print(f"Unknown command: {cmd}")