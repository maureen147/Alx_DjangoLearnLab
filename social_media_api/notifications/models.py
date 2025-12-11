from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

User = get_user_model()

class Notification(models.Model):
    # Notification types
    FOLLOW = 'follow'
    LIKE = 'like'
    COMMENT = 'comment'
    MENTION = 'mention'
    
    NOTIFICATION_TYPES = [
        (FOLLOW, 'New Follower'),
        (LIKE, 'Post Liked'),
        (COMMENT, 'New Comment'),
        (MENTION, 'Mentioned in Post/Comment'),
    ]
    
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='actor_notifications'
    )
    verb = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    
    # Generic foreign key for the target object (post, comment, etc.)
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    
    # Read status
    is_read = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.actor.username} {self.get_verb_display()} - {self.recipient.username}"
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
    
    def mark_as_unread(self):
        if self.is_read:
            self.is_read = False
            self.read_at = None
            self.save()
    
    @classmethod
    def create_notification(cls, recipient, actor, verb, target=None):
        """Helper method to create a notification"""
        notification = cls(
            recipient=recipient,
            actor=actor,
            verb=verb,
        )
        
        if target:
            notification.target_content_type = ContentType.objects.get_for_model(target)
            notification.target_object_id = target.id
        
        notification.save()
        return notification
    
    def get_message(self):
        """Get a human-readable notification message"""
        messages = {
            'follow': f"{self.actor.username} started following you",
            'like': f"{self.actor.username} liked your post",
            'comment': f"{self.actor.username} commented on your post",
            'mention': f"{self.actor.username} mentioned you",
        }
        return messages.get(self.verb, "You have a new notification")
