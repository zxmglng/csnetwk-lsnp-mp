from commands import profile, dm

COMMANDS = {
    "profile": profile.run,
    "dm": dm.run
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