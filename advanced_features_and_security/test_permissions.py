#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.LibraryProject.settings')
django.setup()

from django.contrib.auth.models import User, Group
from bookshelf.models import Book, Author

def test_permissions():
    print("Testing Permissions and Groups Setup...")
    
    # Check if groups exist
    groups = Group.objects.all()
    print("Available Groups:", [group.name for group in groups])
    
    # Check Book model permissions
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType
    
    content_type = ContentType.objects.get_for_model(Book)
    permissions = Permission.objects.filter(content_type=content_type)
    print("Book Model Permissions:")
    for perm in permissions:
        print(f"  - {perm.codename}: {perm.name}")
    
    # Verify the exact permission names required
    required_permissions = ['can_view', 'can_create', 'can_edit', 'can_delete']
    existing_permissions = [perm.codename for perm in permissions]
    
    print("\nRequired Permissions Check:")
    for perm in required_permissions:
        if perm in existing_permissions:
            print(f"  ✅ {perm} - FOUND")
        else:
            print(f"  ❌ {perm} - MISSING")
    
    print("\n✅ Permissions and Groups setup completed successfully!")

if __name__ == '__main__':
    test_permissions()
