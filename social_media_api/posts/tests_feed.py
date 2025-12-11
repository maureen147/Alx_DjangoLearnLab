from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Post

User = get_user_model()

class FeedTests(APITestCase):
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
        self.user3 = User.objects.create_user(
            username='user3',
            email='user3@example.com',
            password='password123'
        )
        
        # Create posts
        self.post1 = Post.objects.create(
            author=self.user2,
            title='Post from user2',
            content='Content from user2'
        )
        self.post2 = Post.objects.create(
            author=self.user3,
            title='Post from user3',
            content='Content from user3'
        )
        
        # Get token for user1
        response = self.client.post('/api/auth/login/', {
            'username': 'user1',
            'password': 'password123'
        })
        self.token1 = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1}')
    
    def test_feed_without_following(self):
        """Test feed when not following anyone"""
        response = self.client.get('/api/feed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['posts']), 0)
    
    def test_feed_with_following(self):
        """Test feed when following users"""
        # User1 follows user2
        self.user1.following.add(self.user2)
        
        response = self.client.get('/api/feed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['posts']), 1)
        self.assertEqual(response.data['posts'][0]['title'], 'Post from user2')
    
    def test_feed_ordering(self):
        """Test that feed shows most recent posts first"""
        # User1 follows user2
        self.user1.following.add(self.user2)
        
        # Create newer post
        self.post3 = Post.objects.create(
            author=self.user2,
            title='Newer post from user2',
            content='New content'
        )
        
        response = self.client.get('/api/feed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should show newest post first
        self.assertEqual(response.data['posts'][0]['title'], 'Newer post from user2')
        self.assertEqual(response.data['posts'][1]['title'], 'Post from user2')