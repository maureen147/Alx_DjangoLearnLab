from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )
    
    def __str__(self):
        return self.username
    
    def follow(self, user):
        """Follow another user"""
        if user != self:
            self.following.add(user)
    
    def unfollow(self, user):
        """Unfollow a user"""
        if user != self:
            self.following.remove(user)
    
    def is_following(self, user):
        """Check if following a user"""
        return self.following.filter(id=user.id).exists()
    
    def get_followers_count(self):
        """Get number of followers"""
        return self.followers.count()
    
    def get_following_count(self):
        """Get number of users following"""
        return self.following.count()