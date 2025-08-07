from typing import Optional
from models.dataclasses.peer import Peer

_current_profile: Optional[Peer] = None

def set_profile(profile: Peer):
    global _current_profile
    _current_profile = profile
    
def get_profile() -> Optional[Peer]:
    return _current_profile

def is_profile_set() -> bool:
    return _current_profile is not None