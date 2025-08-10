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
        self.followers: List[Peer] = []

    def reset_collection(self):
        self.followers = []
    
    def add_peer(self, follower: Peer) -> bool:
        """Add or update a follower. Returns True if added, False if updated."""
        for i, p in enumerate(self.followers):
            if p.USER_ID == follower.USER_ID:
                self.followers[i] = follower
                return False  # updated
        self.followers.append(follower)
        return True  # added

    def remove_follower(self, user_id: str) -> bool:
        for i, p in enumerate(self.followers):
            if p.USER_ID == user_id:
                del self.followers[i]
                return True
        return False

    def get_follower(self, user_id: str) -> Optional[Peer]:
        return next((p for p in self.followers if p.USER_ID == user_id), None)

    def all(self) -> List[Peer]:
        return self.followers
