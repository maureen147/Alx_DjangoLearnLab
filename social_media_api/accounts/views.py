from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, TokenSerializer

class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Get the token that was created in the serializer
            token = Token.objects.get(user=user)
            
            # Return token and user info
            return Response({
                'message': 'User registered successfully',
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token_key = serializer.validated_data['token']
            
            login(request, user)
            
            # Return token and user info
            return Response({
                'message': 'Login successful',
                'token': token_key,
                'user_id': user.id,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

class TokenInfoView(APIView):
    """View to get information about the current token"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        token = Token.objects.get(user=request.user)
        serializer = TokenSerializer(token)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # Delete the token
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
        except Token.DoesNotExist:
            pass
        
        logout(request)
        return Response({
            "message": "Successfully logged out.",
            "detail": "Token has been deleted."
        }, status=status.HTTP_200_OK)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        try:
            user_to_follow = CustomUser.objects.get(id=user_id)
            if user_to_follow == request.user:
                return Response({"detail": "You cannot follow yourself."}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            if not request.user.following.filter(id=user_id).exists():
                request.user.following.add(user_to_follow)
                return Response({
                    "message": f"You are now following {user_to_follow.username}.",
                    "following_count": request.user.following.count()
                }, status=status.HTTP_200_OK)
            else:
                return Response({"detail": f"You are already following {user_to_follow.username}."}, 
                              status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, 
                          status=status.HTTP_404_NOT_FOUND)

class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id):
        try:
            user_to_unfollow = CustomUser.objects.get(id=user_id)
            if request.user.following.filter(id=user_id).exists():
                request.user.following.remove(user_to_unfollow)
                return Response({
                    "message": f"You have unfollowed {user_to_unfollow.username}.",
                    "following_count": request.user.following.count()
                }, status=status.HTTP_200_OK)
            else:
                return Response({"detail": f"You are not following {user_to_unfollow.username}."}, 
                              status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, 
                          status=status.HTTP_404_NOT_FOUND)