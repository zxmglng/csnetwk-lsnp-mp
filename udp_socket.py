import socket
import threading
import config
from handle_message import HandleMessage

class UDPSocket:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UDPSocket, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((config.CURRENT_IP, config.PORT))

        self.encoding = config.ENCODING
        self.running = True
        
        self.handler = HandleMessage()

    def send(self, message: str, address: tuple):
        full_message = message + config.MESSAGE_TERMINATOR
        self.socket.sendto(full_message.encode(self.encoding), address)

    def receive_loop(self):
        def listen():
            while self.running:
                try:
                    data, addr = self.socket.recvfrom(65535)
                    message = data.decode(self.encoding)
                    
                    if addr[0] != config.CURRENT_IP:
                        self.handler.run(message, addr)
                    
                except Exception as e:
                    print(f"Error in receive_loop: {e}")
                    continue

        thread = threading.Thread(target=listen, daemon=True)
        thread.start()

    def close(self):
        self.running = False
        self.socket.close()
