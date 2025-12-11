from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like

User = get_user_model()

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'profile_picture']

class CommentSerializer(serializers.ModelSerializer):
    author = UserBasicSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='author',
        write_only=True
    )
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_id', 'content', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'author']
    
    def create(self, validated_data):
        # Set the author to the current user if not provided
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super().create(validated_data)

class PostSerializer(serializers.ModelSerializer):
    author = UserBasicSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='author',
        write_only=True
    )
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'author_id', 'title', 'content',
                  'created_at', 'updated_at', 'comments', 'comments_count',
                  'likes_count', 'is_liked']
        read_only_fields = ['id', 'created_at', 'updated_at', 'author',
                           'comments_count', 'likes_count', 'is_liked']
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
    
    def create(self, validated_data):
        # Set the author to the current user if not provided
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super().create(validated_data)

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content']

class LikeSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']
        read_only_fields = ['id', 'created_at']