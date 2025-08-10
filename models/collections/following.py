from typing import List, Optional, Dict
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
        self.posts_dict: Dict[str, List[Dict[str, object]]] = {}

    def add_following(self, peer: Peer) -> bool:
        if any(p.USER_ID == peer.USER_ID for p in self.following):
            return False  # already following
        self.following.append(peer)
        
        if peer.USER_ID not in self.posts_dict:
            self.posts_dict[peer.USER_ID] = []
        return True

    def remove_following(self, user_id: str) -> bool:
        peer = self.get_following(user_id)
        if peer:
            self.following.remove(peer)
            
            if user_id in self.posts_dict:
                del self.posts_dict[user_id]
                
            return True
        return False

    def get_following(self, user_id: str) -> Optional[Peer]:
        return next((f for f in self.following if f.USER_ID == user_id), None)

    def all(self) -> List[Peer]:
        return self.following
    
    def add_post(self, user_id: str, timestamp: int, content: str) -> None:
        if user_id not in self.posts_dict:
            self.posts_dict[user_id] = []
        self.posts_dict[user_id].append({
            "timestamp": timestamp,
            "status": False,
            "content": content
        })

    def get_all_users_with_posts(self) -> List[str]:
        return list(self.posts_dict.keys())

    def like_post(self, user_id: str, timestamp: int) -> bool:
        posts = self.posts_dict.get(user_id)
        if not posts:
            return False
        for post in posts:
            if post["timestamp"] == timestamp:
                post["status"] = True
                return True
        return False

    def unlike_post(self, user_id: str, timestamp: int) -> bool:
        posts = self.posts_dict.get(user_id)
        if not posts:
            return False
        for post in posts:
            if post["timestamp"] == timestamp:
                post["status"] = False
                return True
        return False
    
    def get_post(self, user_id: str, timestamp: int) -> Optional[Dict[str, object]]:
        posts = self.posts_dict.get(user_id)
        if not posts:
            return None
        for post in posts:
            if post["timestamp"] == timestamp:
                return post
        return None
