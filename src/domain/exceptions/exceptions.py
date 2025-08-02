class DomainException(Exception):
    """Base domain exception"""
    pass


class UserException(DomainException):
    """User-related domain exceptions"""
    pass


class UserNotAuthenticatedException(UserException):
    """Raised when user is not authenticated"""
    pass


class UserNotActiveException(UserException):
    """Raised when user is not active"""
    pass


class ResourceException(DomainException):
    """Resource-related domain exceptions"""
    pass


class ResourceAccessDeniedException(ResourceException):
    """Raised when user cannot access resource"""
    pass


class ResourceNotFoundException(ResourceException):
    """Raised when resource is not found"""
    pass
