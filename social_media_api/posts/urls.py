from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'comments', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    # Add feed endpoint for Task 3
    path('feed/', views.FeedView.as_view(), name='user-feed'),
    # Separate like/unlike endpoints (for the task requirement)
    path('posts/<int:pk>/like/', views.LikePostView.as_view(), name='post-like'),
    path('posts/<int:pk>/unlike/', views.UnlikePostView.as_view(), name='post-unlike'),
]
