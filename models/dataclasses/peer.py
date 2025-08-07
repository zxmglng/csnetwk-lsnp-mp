from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timezone
from config import MESSAGE_TERMINATOR

@dataclass
class Peer:
    TYPE: str = "PROFILE"
    USER_ID: str = ""
    DISPLAY_NAME: str = ""
    STATUS: str = ""
    AVATAR_TYPE: Optional[str] = None
    AVATAR_ENCODING: Optional[str] = None
    AVATAR_DATA: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_message_dict(self):
        return {
            "TYPE": self.TYPE,
            "USER_ID": self.USER_ID,
            "DISPLAY_NAME": self.DISPLAY_NAME,
            "STATUS": self.STATUS,
            "AVATAR_TYPE": self.AVATAR_TYPE,
            "AVATAR_ENCODING": self.AVATAR_ENCODING,
            "AVATAR_DATA": self.AVATAR_DATA
        }
