#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to verify all required imports are present in the serializers.py file
"""

import os

# Check if serializers.py exists
serializers_path = 'accounts/serializers.py'
if not os.path.exists(serializers_path):
    print("File not found:", serializers_path)
    print("\nCreating the correct serializers.py file...")
    
    # Create the directory if it doesn't exist
    os.makedirs('accounts', exist_ok=True)
    
    # Create the correct serializers.py content
    serializers_content = '''from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'bio']
    
    def validate(self, attrs):
        # Check if passwords match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Check if username already exists
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "A user with that username already exists."})
        
        # Check if email already exists
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "A user with that email already exists."})
        
        return attrs
    
    def create(self, validated_data):
        # Remove password2 from validated data
        validated_data.pop('password2')
        
        # Create user using create_user method (handles password hashing)
        user = User.objects.create_user(**validated_data)
        
        # Create token for the user
        Token.objects.create(user=user)
        
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            # Try to authenticate the user
            user = authenticate(username=username, password=password)
            
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                
                # Get or create token for the user
                token, created = Token.objects.get_or_create(user=user)
                
                # Add user and token to validated data
                attrs['user'] = user
                attrs['token'] = token.key
                return attrs
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio', 
                  'profile_picture', 'followers', 'followers_count', 'following_count',
                  'date_joined', 'last_login']
        read_only_fields = ['id', 'date_joined', 'last_login', 'followers_count', 'following_count']
        extra_kwargs = {
            'followers': {'read_only': True}
        }
    
    def get_followers_count(self, obj):
        return obj.followers.count()
    
    def get_following_count(self, obj):
        return obj.following.count()
'''
    
    with open(serializers_path, 'w') as f:
        f.write(serializers_content)
    
    print("Created", serializers_path, "with all required imports")

# Now read the file
with open(serializers_path, 'r') as f:
    content = f.read()

# Check for required imports
required_imports = [
    "from rest_framework.authtoken.models import Token",
    "Token.objects.create",
    "get_user_model().objects.create_user"
]

print("\nChecking accounts/serializers.py for required imports...\n")

all_present = True
for required in required_imports:
    if required in content:
        print("OK: Found:", required)
    else:
        print("MISSING:", required)
        all_present = False

# Also check for the create method using get_user_model
if 'get_user_model()' in content:
    print("OK: Found: get_user_model() function")
else:
    print("MISSING: get_user_model() function")
    all_present = False

# Check for User.objects.create_user
if 'User.objects.create_user' in content:
    print("OK: Found: User.objects.create_user")
else:
    print("MISSING: User.objects.create_user")
    all_present = False

print("\n" + "="*50)
if all_present:
    print("SUCCESS: All required imports and patterns are present!")
    print("\nYour serializers.py now includes:")
    print("1. Token import from rest_framework.authtoken.models")
    print("2. Token creation in registration")
    print("3. Proper user creation with create_user()")
    print("4. Token retrieval in login")
else:
    print("WARNING: Some required imports/patterns are missing.")
