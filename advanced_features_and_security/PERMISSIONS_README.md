# Permissions and Groups Management

## Overview
This Django application implements a comprehensive permissions and groups system to control access to book management functionality.

## Groups Setup

### 1. Viewers Group
- **Permissions**: `can_view_book`
- **Access**: Can view books but cannot modify them

### 2. Editors Group  
- **Permissions**: `can_view_book`, `can_create_book`, `can_edit_book`
- **Access**: Can view, create, and edit books but cannot delete them

### 3. Admins Group
- **Permissions**: `can_view_book`, `can_create_book`, `can_edit_book`, `can_delete_book`
- **Access**: Full access to all book operations

## Custom Permissions

The Book model has been extended with these custom permissions:
- `can_view_book` - Permission to view books
- `can_create_book` - Permission to create new books
- `can_edit_book` - Permission to edit existing books  
- `can_delete_book` - Permission to delete books

## Views Protection

The following views are protected with permission checks:

- `list_books()` - Requires `can_view_book` permission
- `add_book()` - Requires `can_create_book` permission  
- `edit_book()` - Requires `can_edit_book` permission
- `delete_book()` - Requires `can_delete_book` permission
- `admin_view()` - Requires all book permissions

## Setup Instructions

1. **Run migrations** to create the new permissions:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
Create groups and assign permissions:

bash
python manage.py setup_groups
Assign users to groups through Django admin:

Go to /admin/auth/user/

Select users and assign them to appropriate groups

Test permissions by logging in as different users and accessing:

/relationship/dashboard/ - Shows user's permissions

/relationship/books/ - Book listing (requires view permission)

/relationship/books/add/ - Add book (requires create permission)

Testing
Create test users and assign them to different groups:

Viewer User: Can only view books

Editor User: Can view, create, and edit books

Admin User: Has full access to all book operations

Verify that each user can only perform actions allowed by their group's permissions.
