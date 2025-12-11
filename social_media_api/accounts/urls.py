from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('token-info/', views.TokenInfoView.as_view(), name='token-info'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    
    # Follow management endpoints for Task 3
    # EXACT PATTERN: follow/<int:user_id>/
    path('follow/<int:user_id>/', views.FollowUserView.as_view(), name='follow-user'),
    # EXACT PATTERN: unfollow/<int:user_id>/
    path('unfollow/<int:user_id>/', views.UnfollowUserView.as_view(), name='unfollow-user'),
    
    # Additional endpoints (not required but good to have)
    path('users/<int:user_id>/followers/', views.UserFollowersView.as_view(), name='user-followers'),
    path('users/<int:user_id>/following/', views.UserFollowingView.as_view(), name='user-following'),
]
