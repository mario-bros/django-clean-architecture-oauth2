import unittest
from unittest.mock import Mock
from application.use_cases.access_protected_resource import AccessProtectedResourceUseCase
from domain.entities.user import User, ProtectedResource
from domain.exceptions.exceptions import UserNotAuthenticatedException, UserNotActiveException


class TestAccessProtectedResourceUseCase(unittest.TestCase):
    """Test Clean Architecture use case"""
    
    def setUp(self):
        self.mock_user_repo = Mock()
        self.mock_resource_repo = Mock()
        self.use_case = AccessProtectedResourceUseCase(
            self.mock_user_repo, 
            self.mock_resource_repo
        )
    
    def test_successful_access(self):
        """Test successful access to protected resource"""
        # Arrange
        user = User(
            id=1, username="testuser", email="test@example.com",
            first_name="Test", last_name="User", is_active=True, is_staff=False
        )
        self.mock_user_repo.find_by_id.return_value = user
        
        # Act
        result = self.use_case.execute(user_id=1)
        
        # Assert
        self.assertIn("message", result)
        self.assertIn("user", result)
        self.assertEqual(result["user"]["username"], "testuser")
    
    def test_user_not_found(self):
        """Test access with non-existent user"""
        # Arrange
        self.mock_user_repo.find_by_id.return_value = None
        
        # Act & Assert
        with self.assertRaises(UserNotAuthenticatedException):
            self.use_case.execute(user_id=999)
    
    def test_inactive_user(self):
        """Test access with inactive user"""
        # Arrange
        user = User(
            id=1, username="testuser", email="test@example.com",
            first_name="Test", last_name="User", is_active=False, is_staff=False
        )
        self.mock_user_repo.find_by_id.return_value = user
        
        # Act & Assert
        with self.assertRaises(UserNotActiveException):
            self.use_case.execute(user_id=1)


if __name__ == '__main__':
    unittest.main()
