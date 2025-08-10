from typing import List
from models.dataclasses.peer import Peer

class Peers:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Peers, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.peers: List[Peer] = []

    def reset_collection(self):
        self.peers = []
    
    def add_peer(self, peer: Peer):
        for i, p in enumerate(self.peers):
            if p.USER_ID == peer.USER_ID:
                self.peers[i] = peer  
                return False  

        self.peers.append(peer)  
        return True  


    def get_peer(self, user_id: str):
        return next((p for p in self.peers if p.USER_ID == user_id), None)

    def all(self):
        return self.peers