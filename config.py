import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # connect to a public IP (does not send packets), to determine outgoing interface IP
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

CURRENT_IP = get_local_ip()
PORT = 50999
ENCODING = 'utf-8'
MESSAGE_TERMINATOR = '\n\n'
BROADCAST_ADDRESS = '192.168.1.255'
USERNAME = None
VERBOSE = False