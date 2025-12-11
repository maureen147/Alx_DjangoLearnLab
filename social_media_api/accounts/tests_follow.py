from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

User = get_user_model()

class FollowSystemTests(APITestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password123'
        )
        self.user2 = User.objects.create_user(
            username='user2', 
            email='user2@example.com',
            password='password123'
        )
        
        # Get token for user1
        response = self.client.post('/api/auth/login/', {
            'username': 'user1',
            'password': 'password123'
        })
        self.token1 = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
    
    def test_follow_user(self):
        """Test following another user"""
        response = self.client.post(f'/api/auth/users/{self.user2.id}/follow/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'You are now following user2.')
        
        # Verify follow relationship
        self.assertTrue(self.user1.following.filter(id=self.user2.id).exists())
        self.assertEqual(self.user1.following.count(), 1)
        self.assertEqual(self.user2.followers.count(), 1)
    
    def test_cannot_follow_self(self):
        """Test that user cannot follow themselves"""
        response = self.client.post(f'/api/auth/users/{self.user1.id}/follow/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cannot follow yourself', response.data['detail'])
    
    def test_unfollow_user(self):
        """Test unfollowing a user"""
        # First follow
        self.user1.following.add(self.user2)
        
        # Then unfollow
        response = self.client.post(f'/api/auth/users/{self.user2.id}/unfollow/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'You have unfollowed user2.')
        
        # Verify unfollow
        self.assertFalse(self.user1.following.filter(id=self.user2.id).exists())
        self.assertEqual(self.user1.following.count(), 0)
    
    def test_get_followers_list(self):
        """Test getting list of followers"""
        # Make user2 follow user1
        self.user2.following.add(self.user1)
        
        response = self.client.get(f'/api/auth/users/{self.user1.id}/followers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'user2')
    
    def test_get_following_list(self):
        """Test getting list of users followed"""
        # Make user1 follow user2
        self.user1.following.add(self.user2)
        
        response = self.client.get(f'/api/auth/users/{self.user1.id}/following/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'user2')