from typing import List, Optional
from models.dataclasses.group import Group

class Groups:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Groups, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.groups: List[Group] = []

    def add_group(self, group: Group) -> bool:
        if any(g.GROUP_ID == group.GROUP_ID for g in self.groups):
            return False  
        self.groups.append(group)
        return True

    def remove_group(self, group_id: str) -> bool:
        group = self.get_group(group_id)
        if group:
            self.groups.remove(group)
            return True
        return False

    def get_group(self, group_id: str) -> Optional[Group]:
        return next((g for g in self.groups if g.GROUP_ID == group_id), None)

    def all(self) -> List[Group]:
        return self.groups
