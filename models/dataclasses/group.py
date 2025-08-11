from dataclasses import dataclass, field
from typing import List, Optional
from models.dataclasses.peer import Peer

@dataclass
class Group:
    GROUP_ID: str
    GROUP_NAME: str
    MEMBERS: List[Peer] = field(default_factory=list)

    def add_member(self, peer: Peer) -> bool:
        if any(m.USER_ID == peer.USER_ID for m in self.MEMBERS):
            return False  
        self.MEMBERS.append(peer)
        return True

    def remove_member(self, user_id: str) -> bool:
        member = self.get_member(user_id)
        if member:
            self.MEMBERS.remove(member)
            return True
        return False

    def get_member(self, user_id: str) -> Optional[Peer]:
        return next((m for m in self.MEMBERS if m.USER_ID == user_id), None)

    def all(self) -> List[Peer]:
        return self.MEMBERS

    def update_members(self, add: List[str], remove: List[str]) -> tuple[List[str], List[str]]:
        """Update members by adding and removing specified user IDs.
        
        Returns a tuple of lists: (added, removed).
        """
        added = []
        removed = []

        for user_id in add:
            peer = Peer(user_id)  
            if self.add_member(peer):
                added.append(user_id)

        for user_id in remove:
            if self.remove_member(user_id):
                removed.append(user_id)

        return added, removed
