from typing import List, Optional
from models.dataclasses.peer import Peer  

class Following:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Following, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.following: List[Peer] = []  # store Peer instances
    
    def add_following(self, peer: Peer) -> bool:
        if any(p.USER_ID == peer.USER_ID for p in self.following):
            return False  # already following
        self.following.append(peer)
        return True

    def remove_following(self, user_id: str) -> bool:
        peer = self.get_following(user_id)
        if peer:
            self.following.remove(peer)
            return True
        return False

    def get_following(self, user_id: str) -> Optional[Peer]:
        return next((f for f in self.following if f.USER_ID == user_id), None)

    def all(self) -> List[Peer]:
        return self.following
