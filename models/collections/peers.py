import asyncio
from typing import List
from datetime import datetime, timedelta, timezone
from models.dataclasses.peer import Peer

class Peers:
    _instance = None
    TTL = timedelta(minutes=5)
    
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

    def remove_expried_peers(self):
        now = datetime.now(timezone.utc)
        self.peers = [p for p in self.peers if now - p.created_at < self.TTL]

    async def start_auto_cleanup(self, interval_seconds: int = 10):
        while True:
            self.remove_expried_peers()
            await asyncio.sleep(interval_seconds)        
            