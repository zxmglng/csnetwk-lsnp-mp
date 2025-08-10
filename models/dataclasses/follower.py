from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Follower:
    FOLLOWER_ID: str = ""
    TIMESTAMP: Optional[str] = None  # Optional field
    IP: Optional[str] = None