from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasScope
from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.types import OpenApiTypes


class ProtectedResourceView(APIView):
    """
    Original OAuth2 protected resource endpoint.
    
    This is the simple, traditional Django view before Clean Architecture refactoring.
    Compare this with the Clean Architecture version in src/presentation/views/
    """
    permission_classes = [IsAuthenticated, TokenHasScope]
    required_scopes = ['read']

    @extend_schema(
        operation_id='get_protected_resource_original',
        description='Get protected resource using traditional Django approach',
        responses={
            200: OpenApiResponse(
                description='Protected resource accessed successfully',
                response={
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'example': 'This is a protected resource!'
                        }
                    }
                }
            ),
            401: OpenApiResponse(
                description='Authentication credentials were not provided'
            ),
            403: OpenApiResponse(
                description='Insufficient OAuth2 scope permissions'
            ),
        },
        tags=['Original Implementation'],
        summary='Get protected resource (Original)'
    )
    def get(self, request):
        """Original implementation without Clean Architecture."""
        return Response({"message": "This is a protected resource!"})
