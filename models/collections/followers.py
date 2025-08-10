from typing import List, Optional
from models.dataclasses.peer import Peer  

class Followers:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Followers, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.followers: List[Peer] = []  # store Peer instances
    
    def add_follower(self, peer: Peer) -> bool:
        for i, f in enumerate(self.followers):
            if f.USER_ID == peer.USER_ID:
                self.followers[i] = peer
                return False  # Updated existing follower
        self.followers.append(peer)
        return True  # Added new follower

    def remove_follower(self, user_id: str) -> bool:
        peer = self.get_follower(user_id)
        if peer:
            self.followers.remove(peer)
            return True
        return False

    def get_follower(self, user_id: str) -> Optional[Peer]:
        return next((f for f in self.followers if f.USER_ID == user_id), None)

    def all(self) -> List[Peer]:
        return self.followers
