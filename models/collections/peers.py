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
        existing_peer = self.get_peer(peer.USER_ID)
        if existing_peer:
            existing_peer.DISPLAY_NAME = peer.DISPLAY_NAME
            existing_peer.STATUS = peer.STATUS
            existing_peer.AVATAR_TYPE = peer.AVATAR_TYPE
            existing_peer.AVATAR_ENCODING = peer.AVATAR_ENCODING
            existing_peer.AVATAR_DATA = peer.AVATAR_DATA
            existing_peer.IP = peer.IP
        else:
            self.peers.append(peer)  


    def get_peer(self, user_id: str):
        return next((p for p in self.peers if p.USER_ID == user_id), None)

    def all(self):
        return self.peers