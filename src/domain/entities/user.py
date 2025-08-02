from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class User:
    """Core User domain entity"""
    id: Optional[int]
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    is_staff: bool
    date_joined: Optional[datetime] = None
    last_login: Optional[datetime] = None
    
    @property
    def full_name(self) -> str:
        """Business rule for full name formatting"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def can_access_protected_resource(self) -> bool:
        """Business rule for resource access"""
        return self.is_active and not self.is_banned()
    
    def is_banned(self) -> bool:
        """Business rule to check if user is banned"""
        # Implement your business logic here
        return False


@dataclass
class ProtectedResource:
    """Core Protected Resource entity"""
    id: Optional[int]
    name: str
    description: str
    owner_id: int
    is_public: bool = False
    created_at: Optional[datetime] = None
    
    def is_accessible_by_user(self, user: User) -> bool:
        """Business rule for resource accessibility"""
        if self.is_public:
            return True
        return user.id == self.owner_id or user.is_staff
