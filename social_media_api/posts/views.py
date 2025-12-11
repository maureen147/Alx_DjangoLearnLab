from rest_framework import viewsets, permissions, status, filters, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
from .models import Post, Comment, Like
from .serializers import (
    PostSerializer, CommentSerializer, 
    LikeSerializer, PostCreateSerializer
)
from .permissions import IsOwnerOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing posts.
    """
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'author__username']
    filterset_fields = ['author']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """Like or unlike a post"""
        post = self.get_object()
        user = request.user
        
        like, created = Like.objects.get_or_create(post=post, user=user)
        
        if not created:
            # Unlike if already liked
            like.delete()
            
            # Delete like notification if exists
            Notification.objects.filter(
                recipient=post.author,
                actor=user,
                verb='like',
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=post.id
            ).delete()
            
            return Response({'status': 'unliked', 'likes_count': post.likes.count()})
        
        # Create notification for post author (unless liking own post)
        if post.author != user:
            Notification.create_notification(
                recipient=post.author,
                actor=user,
                verb='like',
                target=post
            )
        
        return Response({'status': 'liked', 'likes_count': post.likes.count()})
    
    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        """Get all likes for a post"""
        post = self.get_object()
        likes = post.likes.all()
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post', None)
        if post_id is not None:
            queryset = queryset.filter(post_id=post_id)
        return queryset
    
    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        
        # Create notification for post author (unless commenting on own post)
        if comment.post.author != comment.author:
            Notification.create_notification(
                recipient=comment.post.author,
                actor=comment.author,
                verb='comment',
                target=comment.post
            )

# FEED VIEW FOR TASK 3
class FeedView(generics.ListAPIView):
    """
    View to get posts from users that the current user follows
    This view returns posts ordered by creation date, showing the most recent posts at the top.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Get users that the current user follows
        following_users = self.request.user.following.all()
        
        # Get posts from those users, ordered by creation date (most recent first)
        return Post.objects.filter(author__in=following_users).order_by('-created_at')
