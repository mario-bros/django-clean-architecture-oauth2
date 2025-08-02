from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from oauth2_provider.contrib.rest_framework import TokenHasScope
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

from application.use_cases.access_protected_resource import AccessProtectedResourceUseCase
from infrastructure.repositories.django_user_repository import DjangoUserRepository
from infrastructure.repositories.memory_resource_repository import InMemoryResourceRepository
from domain.exceptions.exceptions import (
    UserNotAuthenticatedException,
    UserNotActiveException,
    ResourceAccessDeniedException
)


class ProtectedResourceView(APIView):
    """
    Clean Architecture OAuth2 protected resource endpoint.
    
    This endpoint demonstrates Clean Architecture principles:
    - Separation of concerns between layers
    - Dependency inversion (business logic doesn't depend on frameworks)
    - Use case pattern for business logic encapsulation
    - Repository pattern for data access abstraction
    - Domain-driven exception handling
    
    Compare this implementation with the traditional approach in myapp/views.py
    """
    permission_classes = [IsAuthenticated, TokenHasScope]
    required_scopes = ['read']

    def __init__(self):
        super().__init__()
        # Dependency injection - in production, use a DI container
        self.user_repository = DjangoUserRepository()
        self.resource_repository = InMemoryResourceRepository()
        self.access_use_case = AccessProtectedResourceUseCase(
            self.user_repository,
            self.resource_repository
        )

    @extend_schema(
        operation_id='get_protected_resource_clean_arch',
        description='Access protected resources using Clean Architecture pattern with OAuth2',
        parameters=[
            OpenApiParameter(
                name='resource_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Optional: Filter by specific resource ID (1, 2, or 3)',
                required=False
            ),
        ],
        responses={
            200: OpenApiResponse(
                description='Protected resources retrieved successfully',
                response={
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'example': 'This is a protected resource!'
                        },
                        'user': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'username': {'type': 'string', 'example': 'testuser'},
                                'full_name': {'type': 'string', 'example': 'Test User'}
                            }
                        },
                        'resource': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'name': {'type': 'string', 'example': 'User Profile Data'},
                                'description': {'type': 'string', 'example': 'Personal profile information'}
                            }
                        },
                        'access_granted_at': {'type': 'string', 'example': 'now'}
                    }
                }
            ),
            400: OpenApiResponse(description='Invalid resource ID format'),
            401: OpenApiResponse(description='Authentication credentials were not provided'),
            403: OpenApiResponse(description='Insufficient OAuth2 scope permissions or user not active'),
            500: OpenApiResponse(description='Internal server error'),
        },
        tags=['Clean Architecture'],
        summary='Get protected resources (Clean Architecture)'
    )
    def get(self, request):
        """
        Get protected resource data using Clean Architecture pattern.
        
        This method demonstrates:
        1. Controller responsibility: Handle HTTP concerns only
        2. Use case execution: Delegate business logic to use cases
        3. Exception handling: Convert domain exceptions to HTTP responses
        4. Clean separation: No business logic in the controller
        """
        try:
            # Parse request parameters
            resource_id = request.query_params.get('resource_id')
            if resource_id:
                resource_id = int(resource_id)
            
            # Execute use case (this is where business logic happens)
            result = self.access_use_case.execute(
                user_id=request.user.id,
                resource_id=resource_id
            )
            
            return Response(result, status=status.HTTP_200_OK)
            
        except UserNotAuthenticatedException as e:
            return Response(
                {'error': str(e), 'type': 'authentication_error'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        except UserNotActiveException as e:
            return Response(
                {'error': str(e), 'type': 'authorization_error'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        except ResourceAccessDeniedException as e:
            return Response(
                {'error': str(e), 'type': 'access_denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        except ValueError:
            return Response(
                {'error': 'Invalid resource ID format', 'type': 'validation_error'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': 'Internal server error', 'type': 'server_error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
