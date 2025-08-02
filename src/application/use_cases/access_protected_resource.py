from application.interfaces.repositories import UserRepository, ResourceRepository
from domain.entities.user import User, ProtectedResource
from domain.exceptions.exceptions import (
    UserNotAuthenticatedException,
    UserNotActiveException,
    ResourceAccessDeniedException
)


class AccessProtectedResourceUseCase:
    """Use case for accessing protected resources"""
    
    def __init__(self, user_repository: UserRepository, resource_repository: ResourceRepository):
        self.user_repository = user_repository
        self.resource_repository = resource_repository
    
    def execute(self, user_id: int, resource_id: int = None) -> dict:
        """
        Access protected resource
        
        Args:
            user_id: ID of the user requesting access
            resource_id: Optional specific resource ID
            
        Returns:
            dict: Protected resource data
            
        Raises:
            UserNotAuthenticatedException: When user doesn't exist
            UserNotActiveException: When user is not active
            ResourceAccessDeniedException: When user cannot access resource
        """
        # Find user
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotAuthenticatedException("User not found")
        
        # Check if user can access protected resources (business rule)
        if not user.can_access_protected_resource():
            raise UserNotActiveException("User account is not active")
        
        # If specific resource requested, check access
        if resource_id:
            resource = self.resource_repository.find_by_id(resource_id)
            if not resource:
                raise ResourceAccessDeniedException("Resource not found")
            
            if not resource.is_accessible_by_user(user):
                raise ResourceAccessDeniedException("Access denied to this resource")
            
            return {
                "message": f"Access granted to resource: {resource.name}",
                "resource": {
                    "id": resource.id,
                    "name": resource.name,
                    "description": resource.description
                },
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "full_name": user.full_name
                }
            }
        
        # General protected resource access
        return {
            "message": "This is a protected resource!",
            "user": {
                "id": user.id,
                "username": user.username,
                "full_name": user.full_name
            },
            "access_granted_at": "now"  # In real app, use proper datetime
        }
