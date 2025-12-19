from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.URLField(blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, blank=True)
    
    def __str__(self):
        return self.username
