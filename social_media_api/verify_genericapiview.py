#!/usr/bin/env python3
"""
Verify that FollowUserView and UnfollowUserView use generics.GenericAPIView
"""

with open('accounts/views.py', 'r') as f:
    content = f.read()

print("Checking accounts/views.py for GenericAPIView usage...")
print("=" * 60)

# Check 1: Import statement
print("\n1. Checking import of 'generics':")
if 'from rest_framework import' in content and 'generics' in content:
    print("   ✅ 'generics' is imported")
else:
    print("   ❌ 'generics' is not imported")

# Check 2: FollowUserView uses GenericAPIView
print("\n2. Checking FollowUserView:")
if 'class FollowUserView(generics.GenericAPIView):' in content:
    print("   ✅ FollowUserView inherits from generics.GenericAPIView")
else:
    print("   ❌ FollowUserView does not inherit from generics.GenericAPIView")
    
    # Show what it actually inherits from
    import re
    match = re.search(r'class FollowUserView\((.*?)\):', content)
    if match:
        print(f"   Actually inherits from: {match.group(1)}")

# Check 3: UnfollowUserView uses GenericAPIView
print("\n3. Checking UnfollowUserView:")
if 'class UnfollowUserView(generics.GenericAPIView):' in content:
    print("   ✅ UnfollowUserView inherits from generics.GenericAPIView")
else:
    print("   ❌ UnfollowUserView does not inherit from generics.GenericAPIView")
    
    # Show what it actually inherits from
    match = re.search(r'class UnfollowUserView\((.*?)\):', content)
    if match:
        print(f"   Actually inherits from: {match.group(1)}")

# Check 4: Both have post methods
print("\n4. Checking both views have post() methods:")
has_follow_post = 'def post(self, request, user_id):' in content and 'class FollowUserView' in content
has_unfollow_post = 'def post(self, request, user_id):' in content and 'class UnfollowUserView' in content

print(f"   FollowUserView has post() method: {'✅ Yes' if has_follow_post else '❌ No'}")
print(f"   UnfollowUserView has post() method: {'✅ Yes' if has_unfollow_post else '❌ No'}")

print("\n" + "=" * 60)
if ('class FollowUserView(generics.GenericAPIView):' in content and 
    'class UnfollowUserView(generics.GenericAPIView):' in content):
    print("✅ SUCCESS: Both follow/unfollow views use generics.GenericAPIView!")
else:
    print("❌ ISSUE: Views need to inherit from generics.GenericAPIView")
