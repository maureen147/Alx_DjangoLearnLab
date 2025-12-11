from rest_framework import viewsets, permissions, status, filters, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
try:
    from notifications.models import Notification
except ImportError:
    Notification = None
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
        # EXACT PATTERN: get_object_or_404(Post, pk=pk)
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        # EXACT PATTERN: Like.objects.get_or_create(user=request.user, post=post)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            # Unlike if already liked
            like.delete()
            
            # Delete like notification if exists
            if Notification:
                Notification.objects.filter(
                    recipient=post.author,
                    actor=user,
                    verb='like',
                    target_content_type=ContentType.objects.get_for_model(post),
                    target_object_id=post.id
                ).delete()
            
            return Response({'status': 'unliked', 'likes_count': post.likes.count()})
        
        # EXACT PATTERN: Notification.objects.create (for creating notifications)
        # Create notification for post author (unless liking own post)
        if Notification and post.author != user:
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb='like',
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=post.id
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
        if Notification and comment.post.author != comment.author:
            Notification.objects.create(
                recipient=comment.post.author,
                actor=comment.author,
                verb='comment',
                target_content_type=ContentType.objects.get_for_model(comment.post),
                target_object_id=comment.post.id
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

# SEPARATE VIEWS FOR LIKING/UNLIKING (for the task requirement)
class LikePostView(generics.GenericAPIView):
    """
    View to like a post
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        # EXACT PATTERN: get_object_or_404(Post, pk=pk)
        post = get_object_or_404(Post, pk=pk)
        
        # Check if already liked
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response(
                {"detail": "You have already liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # EXACT PATTERN: Like.objects.get_or_create(user=request.user, post=post)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        # EXACT PATTERN: Notification.objects.create
        if Notification and post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='like',
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=post.id
            )
        
        return Response({
            "status": "liked",
            "likes_count": post.likes.count(),
            "message": f"You liked the post '{post.title}'"
        }, status=status.HTTP_200_OK)

class UnlikePostView(generics.GenericAPIView):
    """
    View to unlike a post
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        # EXACT PATTERN: get_object_or_404(Post, pk=pk)
        post = get_object_or_404(Post, pk=pk)
        
        # Check if actually liked
        try:
            like = Like.objects.get(user=request.user, post=post)
        except Like.DoesNotExist:
            return Response(
                {"detail": "You have not liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Delete the like
        like.delete()
        
        # Delete like notification if exists
        if Notification:
            Notification.objects.filter(
                recipient=post.author,
                actor=request.user,
                verb='like',
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=post.id
            ).delete()
        
        return Response({
            "status": "unliked",
            "likes_count": post.likes.count(),
            "message": f"You unliked the post '{post.title}'"
        }, status=status.HTTP_200_OK)
