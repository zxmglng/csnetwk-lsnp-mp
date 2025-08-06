import socket
from models.message import Message
from controllers.command_router import CommandRouter
from logs.logger import logger

class UDPServer:
    def __init__(self, host='localhost', port=50999):
        self.router = CommandRouter()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((host, port))
        logger.info(f"UDP Server running on {host}:{port}")

    def run(self):
        while True:
            try:
                data, address = self.socket.recvfrom(1024)
                content = data.decode('utf-8').strip()
                
                if not content:
                    continue

                message = Message(address, content)
                logger.info(f"Received: {message}")

                response, forwards = self.router.route(message)

                # Respond to sender
                self.socket.sendto(response.encode('utf-8'), address)
                logger.info(f"Sent response to {address}: {response}")

                # Forward messages to other clients
                for target_address, msg in forwards:
                    self.socket.sendto(msg.encode('utf-8'), target_address)
                    logger.info(f"Forwarded to {target_address}: {msg}")

            except Exception as e:
                logger.error(f"Error handling message: {e}")

if __name__ == "__main__":
    UDPServer().run()