from rest_framework import generics, permissions
from rest_framework.response import Response
from django.db.models import Q
from .models import Post
from .serializers import PostSerializer

class UserFeedView(generics.ListAPIView):
    """
    View to get posts from users that the current user follows
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # Get IDs of users that the current user follows
        following_ids = user.following.values_list('id', flat=True)
        
        # Get posts from followed users
        queryset = Post.objects.filter(
            author_id__in=following_ids
        ).select_related('author').prefetch_related('comments', 'likes')
        
        # Optional: Also include user's own posts
        # queryset = queryset | Post.objects.filter(author=user)
        
        return queryset.order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Get paginated data
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        
        # Add feed metadata
        response_data = {
            'feed_info': {
                'total_posts': queryset.count(),
                'following_count': request.user.following.count(),
                'description': f'Posts from {request.user.following.count()} users you follow'
            },
            'posts': serializer.data
        }
        
        return Response(response_data)