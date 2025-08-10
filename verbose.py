import datetime
import config

def vprint(direction, msg, sender_ip=None, msg_type=None):
    #Verbose print with timestamp, message type color coding, and optional sender info.
    if not getattr(config, "VERBOSE", False):
        return True
    
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    
    # Direction-based colors (SEND, RECV, DROP, etc.)
    dir_colors = {
        "SEND": "\033[94m",   # Blue
        "RECV": "\033[92m",   # Green
    }
    
    # Message-type-based colors
    type_colors = {
        "FOLLOW": "\033[93m",    # Yellow
        "UNFOLLOW": "\033[91m",  # Red
        "DM": "\033[96m",        # Cyan
        "PING": "\033[95m",      # Magenta
    }
    
    RESET = "\033[0m"
    
    # Pick message type color if available, otherwise use direction color
    color = type_colors.get(msg_type, dir_colors.get(direction, ""))
    
    prefix = f"{color}{direction:>5} {ts}{RESET}"
    ip_info = f"[{sender_ip}]" if sender_ip else ""
    type_info = f"({msg_type})" if msg_type else ""
    
    print(f"{prefix} {ip_info} {type_info} {msg}")
    return False