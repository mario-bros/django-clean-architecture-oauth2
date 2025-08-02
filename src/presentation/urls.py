from django.urls import path
from src.presentation.views.protected_resource_view import ProtectedResourceView

urlpatterns = [
    path('api/v2/protected-resource/', ProtectedResourceView.as_view(), name='protected_resource_v2'),
]
