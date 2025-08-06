import socket
import threading
from logs.logger import logger

class UDPClient:
    def __init__(self, server_host='localhost', server_port=50999):
        self.server_address = (server_host, server_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.socket.bind(('localhost', 0))  
        self.running = True

        self.listener_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.listener_thread.start()

    def send(self, message):
        logger.info(f"Sending: {message}")
        self.socket.sendto(message.encode('utf-8'), self.server_address)

    def receive_messages(self):
        while self.running:
            try:
                data, _ = self.socket.recvfrom(1024)
                msg = data.decode('utf-8')
                print(f"\n[RECEIVED] {msg}\n> ", end='', flush=True)
                logger.info(f"Received: {msg}")
            except Exception as e:
                logger.error(f"Receive error: {e}")
                break

    def stop(self):
        self.running = False
        self.socket.close()

if __name__ == "__main__":
    client = UDPClient()

    print("Available commands:")
    print(" - REGISTER <username>")
    print(" - POST <message>")
    print(" - DM <username> <message>")
    print(" - FOLLOW <username>")
    print(" - UNFOLLOW <username>")
    print(" - exit/quit\n")

    try:
        while True:
            msg = input("> ")
            if msg.lower() in ['exit', 'quit']:
                break
            client.send(msg)
    except KeyboardInterrupt:
        pass
    finally:
        client.stop()