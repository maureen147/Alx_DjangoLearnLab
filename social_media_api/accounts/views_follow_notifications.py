from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from notifications.models import Notification
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, TokenSerializer

# ... (keep all other views the same until follow views) ...

# FOLLOW FUNCTIONALITY WITH NOTIFICATIONS
class FollowUserView(generics.GenericAPIView):
    """
    View to follow a user
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        try:
            user_to_follow = CustomUser.objects.get(id=user_id)
            
            if user_to_follow == request.user:
                return Response(
                    {"detail": "You cannot follow yourself."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if already following
            if request.user.following.filter(id=user_id).exists():
                return Response(
                    {"detail": f"You are already following {user_to_follow.username}."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Follow the user
            request.user.following.add(user_to_follow)
            
            # Create notification for the followed user
            Notification.create_notification(
                recipient=user_to_follow,
                actor=request.user,
                verb='follow'
            )
            
            return Response({
                "message": f"You are now following {user_to_follow.username}.",
                "following_count": request.user.following.count(),
                "followers_count": user_to_follow.followers.count()
            }, status=status.HTTP_200_OK)
            
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "User not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )

class UnfollowUserView(generics.GenericAPIView):
    """
    View to unfollow a user
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        try:
            user_to_unfollow = CustomUser.objects.get(id=user_id)
            
            # Check if actually following
            if not request.user.following.filter(id=user_id).exists():
                return Response(
                    {"detail": f"You are not following {user_to_unfollow.username}."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Unfollow the user
            request.user.following.remove(user_to_unfollow)
            
            # Delete follow notification if exists
            Notification.objects.filter(
                recipient=user_to_unfollow,
                actor=request.user,
                verb='follow'
            ).delete()
            
            return Response({
                "message": f"You have unfollowed {user_to_unfollow.username}.",
                "following_count": request.user.following.count(),
                "followers_count": user_to_unfollow.followers.count()
            }, status=status.HTTP_200_OK)
            
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "User not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )

# ... (keep the rest of the file the same) ...
