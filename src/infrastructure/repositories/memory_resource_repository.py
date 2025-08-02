from typing import Optional
from application.interfaces.repositories import ResourceRepository
from domain.entities.user import ProtectedResource


class InMemoryResourceRepository(ResourceRepository):
    """In-memory implementation of ResourceRepository for demo purposes"""
    
    def __init__(self):
        self._resources = [
            ProtectedResource(
                id=1,
                name="User Profile Data",
                description="Personal profile information",
                owner_id=1,
                is_public=False
            ),
            ProtectedResource(
                id=2,
                name="Public Documentation",
                description="API documentation and guides",
                owner_id=1,
                is_public=True
            ),
            ProtectedResource(
                id=3,
                name="Admin Panel",
                description="Administrative controls",
                owner_id=1,
                is_public=False
            )
        ]
    
    def find_by_id(self, resource_id: int) -> Optional[ProtectedResource]:
        """Find resource by ID"""
        for resource in self._resources:
            if resource.id == resource_id:
                return resource
        return None
    
    def find_by_owner(self, owner_id: int) -> list[ProtectedResource]:
        """Find resources by owner"""
        return [r for r in self._resources if r.owner_id == owner_id]
    
    def create(self, resource: ProtectedResource) -> ProtectedResource:
        """Create new resource"""
        # Generate new ID
        max_id = max([r.id for r in self._resources]) if self._resources else 0
        resource.id = max_id + 1
        self._resources.append(resource)
        return resource
