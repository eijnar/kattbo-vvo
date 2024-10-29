from dataclasses import dataclass
from typing import List

from core.database.models.user import User


@dataclass
class UserContext:
    user: User
    permissions: List[str]
    
    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions