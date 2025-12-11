from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Notification

User = get_user_model()

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'profile_picture']

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserBasicSerializer(read_only=True)
    recipient = UserBasicSerializer(read_only=True)
    message = serializers.SerializerMethodField()
    target_type = serializers.SerializerMethodField()
    target_id = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'actor', 'recipient', 'verb', 'message',
            'target_type', 'target_id', 'is_read',
            'created_at', 'read_at'
        ]
        read_only_fields = ['id', 'created_at', 'read_at']
    
    def get_message(self, obj):
        return obj.get_message()
    
    def get_target_type(self, obj):
        if obj.target_content_type:
            return obj.target_content_type.model
        return None
    
    def get_target_id(self, obj):
        return obj.target_object_id

class NotificationCreateSerializer(serializers.Serializer):
    recipient_id = serializers.IntegerField()
    verb = serializers.CharField()
    target_type = serializers.CharField(required=False)
    target_id = serializers.IntegerField(required=False)

class MarkAsReadSerializer(serializers.Serializer):
    notification_ids = serializers.ListField(
        child=serializers.IntegerField()
    )
    read = serializers.BooleanField(default=True)
