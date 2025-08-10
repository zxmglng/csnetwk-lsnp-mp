from typing import List, Optional
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Post:
    timestamp: int  
    content: str
    status: bool = False


class MyPosts:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MyPosts, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.posts: List[Post] = []

    def add_post(self, content: str, timestamp: Optional[int] = None) -> None:
        if timestamp is None:
            import time
            timestamp = int(time.time())
        self.posts.append(Post(timestamp, content))

    def all(self) -> List[Post]:
        return self.posts

    def get_post(self, timestamp: int) -> Optional[Post]:
        return next((p for p in self.posts if p.timestamp == timestamp), None)