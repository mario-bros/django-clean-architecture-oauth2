from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.user import User, ProtectedResource


class UserRepository(ABC):
    """Abstract repository interface for User operations"""
    
    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        """Find user by ID"""
        pass
    
    @abstractmethod
    def find_by_username(self, username: str) -> Optional[User]:
        """Find user by username"""
        pass


class ResourceRepository(ABC):
    """Abstract repository interface for Resource operations"""
    
    @abstractmethod
    def find_by_id(self, resource_id: int) -> Optional[ProtectedResource]:
        """Find resource by ID"""
        pass
    
    @abstractmethod
    def find_by_owner(self, owner_id: int) -> list[ProtectedResource]:
        """Find resources by owner"""
        pass
    
    @abstractmethod
    def create(self, resource: ProtectedResource) -> ProtectedResource:
        """Create new resource"""
        pass
