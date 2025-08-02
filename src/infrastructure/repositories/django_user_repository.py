from typing import Optional
from application.interfaces.repositories import UserRepository
from domain.entities.user import User
from django.contrib.auth.models import User as DjangoUser


class DjangoUserRepository(UserRepository):
    """Django ORM implementation of UserRepository"""
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        """Find user by ID"""
        try:
            django_user = DjangoUser.objects.get(id=user_id)
            return self._to_domain_entity(django_user)
        except DjangoUser.DoesNotExist:
            return None
    
    def find_by_username(self, username: str) -> Optional[User]:
        """Find user by username"""
        try:
            django_user = DjangoUser.objects.get(username=username)
            return self._to_domain_entity(django_user)
        except DjangoUser.DoesNotExist:
            return None
    
    def _to_domain_entity(self, django_user: DjangoUser) -> User:
        """Convert Django model to domain entity"""
        return User(
            id=django_user.id,
            username=django_user.username,
            email=django_user.email,
            first_name=django_user.first_name,
            last_name=django_user.last_name,
            is_active=django_user.is_active,
            is_staff=django_user.is_staff,
            date_joined=django_user.date_joined,
            last_login=django_user.last_login
        )
