from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserAuthenticationTests(APITestCase):
    def setUp(self):
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'
        self.profile_url = '/api/auth/profile/'
        self.logout_url = '/api/auth/logout/'
        
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'bio': 'Test bio'
        }
    
    def test_user_registration(self):
        """Test user registration creates user and token"""
        response = self.client.post(self.register_url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)
        
        # Verify user was created
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@example.com')
        
        # Verify token was created
        token = Token.objects.get(user=user)
        self.assertEqual(response.data['token'], token.key)
    
    def test_user_login(self):
        """Test user login returns token"""
        # First register a user
        self.client.post(self.register_url, self.user_data, format='json')
        
        # Then login
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Login successful')
    
    def test_token_retrieval(self):
        """Test token is retrieved after login"""
        # Register
        self.client.post(self.register_url, self.user_data, format='json')
        
        # Login
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        
        # Use token to access protected endpoint
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        
        profile_response = self.client.get(self.profile_url)
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
    
    def test_user_logout_deletes_token(self):
        """Test logout deletes the token"""
        # Register and login
        self.client.post(self.register_url, self.user_data, format='json')
        
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        token = login_response.data['token']
        
        # Logout
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        logout_response = self.client.post(self.logout_url)
        
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        
        # Verify token is deleted
        user = User.objects.get(username='testuser')
        with self.assertRaises(Token.DoesNotExist):
            Token.objects.get(user=user)
    
    def test_duplicate_username_registration(self):
        """Test registration with duplicate username fails"""
        # Create first user
        self.client.post(self.register_url, self.user_data, format='json')
        
        # Try to create second user with same username
        duplicate_data = self.user_data.copy()
        duplicate_data['email'] = 'test2@example.com'
        
        response = self.client.post(self.register_url, duplicate_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
    
    def test_password_mismatch(self):
        """Test registration with mismatched passwords fails"""
        data = self.user_data.copy()
        data['password2'] = 'differentpassword'
        
        response = self.client.post(self.register_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)