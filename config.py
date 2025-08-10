import socket
import struct
import platform

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't actually send packets, just figures out the outgoing interface IP
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def get_broadcast_address():
    local_ip = get_local_ip()

    # Windows: assume /24 subnet (common in home networks)
    if platform.system() == "Windows":
        parts = local_ip.split(".")
        parts[-1] = "255"
        return ".".join(parts)

CURRENT_IP = get_local_ip()
PORT = 50999
ENCODING = 'utf-8'
MESSAGE_TERMINATOR = '\n\n'
BROADCAST_ADDRESS = get_broadcast_address()
USERNAME = None
VERBOSE = False
