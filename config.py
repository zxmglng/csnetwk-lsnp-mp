import socket

PORT = 50999
ENCODING = 'utf-8'
MESSAGE_TERMINATOR = '\n\n'
BROADCAST_ADDRESS = '<broadcast>'
CURRENT_IP = socket.gethostbyname(socket.gethostname())
USERNAME = None
VERBOSE = False