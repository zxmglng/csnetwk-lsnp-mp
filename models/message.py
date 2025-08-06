"""
Represents a message sent by a client.

Attributes:
    address (tuple): The sender's (host, port) socket address.
    content (str): The message content.
"""
class Message:
    def __init__(self, address, content):
        self.address = address
        self.content = content
        
    def __str__(self):
        return f"[{self.address}] {self.content}"