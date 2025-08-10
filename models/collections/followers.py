from typing import List, Optional
from models.dataclasses.follower import Follower

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
        self.followers: List[Follower] = []

    def reset_collection(self):
        self.followers = []
    
    def add_follower(self, follower: Follower) -> bool:
        for i, f in enumerate(self.followers):
            if f.FOLLOWER_ID == follower.FOLLOWER_ID:
                self.followers[i] = follower
                return False  # Updated existing follower
        self.followers.append(follower)
        return True  # Added new follower

    def remove_follower(self, follower_id: str) -> bool:
        follower = self.get_follower(follower_id)
        if follower:
            self.followers.remove(follower)
            return True
        return False

    def get_follower(self, follower_id: str) -> Optional[Follower]:
        return next((f for f in self.followers if f.FOLLOWER_ID == follower_id), None)

    def all(self) -> List[Follower]:
        return self.followers
