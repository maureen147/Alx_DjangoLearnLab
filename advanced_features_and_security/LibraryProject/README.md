# LibraryProject - Django Application

## Project Overview
This is a Django project that implements a library management system with custom user models, permissions, and groups for access control.

## Project Structure
LibraryProject/
├── LibraryProject/ # Main project directory
│ ├── settings.py # Project settings with AUTH_USER_MODEL configured
│ ├── urls.py # Main URL configuration
│ ├── wsgi.py # WSGI configuration
│ └── asgi.py # ASGI configuration
├── bookshelf/ # Main app with custom user model and book management
│ ├── models.py # CustomUser model and Book model with permissions
│ ├── views.py # Views with permission decorators
│ ├── urls.py # App URL configuration
│ ├── admin.py # Admin configuration
│ ├── management/commands/ # Custom management commands
│ └── templates/ # HTML templates
└── relationship_app/ # Additional app for relationships
├── models.py # Additional models
├── views.py # Additional views
└── urls.py # App URL configuration

text

## Features Implemented

### 1. Custom User Model
- **File**: `bookshelf/models.py`
- **Model**: `CustomUser` extending `AbstractUser`
- **Additional Fields**:
  - `date_of_birth` (DateField)
  - `profile_photo` (ImageField)
- **Custom Manager**: `CustomUserManager` with proper `create_user` and `create_superuser` methods

### 2. Permissions and Groups System
- **File**: `bookshelf/models.py`
- **Book Model Permissions**:
  - `can_view` - Permission to view books
  - `can_create` - Permission to create books
  - `can_edit` - Permission to edit books
  - `can_delete` - Permission to delete books

### 3. User Groups
- **Viewers Group**: Can only view books (`can_view` permission)
- **Editors Group**: Can view, create, and edit books (`can_view`, `can_create`, `can_edit` permissions)
- **Admins Group**: Full access to all book operations (all permissions)

### 4. Protected Views
- **File**: `bookshelf/views.py`
- All views are protected with `@permission_required` decorators:
  - `book_list()` - Requires `can_view` permission
  - `add_book()` - Requires `can_create` permission
  - `edit_book()` - Requires `can_edit` permission
  - `delete_book()` - Requires `can_delete` permission


  cat >> LibraryProject/README.md << 'EOF'

## Setup Instructions

### 1. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate



## Step 6: Add access points and testing

```bash
cat >> LibraryProject/README.md << 'EOF'

## Access Points

- **Admin Interface**: `http://127.0.0.1:8000/admin/`
- **Bookshelf Dashboard**: `http://127.0.0.1:8000/bookshelf/dashboard/`
- **Book List**: `http://127.0.0.1:8000/bookshelf/books/`

## Testing Permissions

1. **Create test users** in Django admin
2. **Assign users to different groups** (Viewers, Editors, Admins)
3. **Login as each user** and verify they can only perform actions allowed by their group's permissions
EOF

## Configuration

### Custom User Model
The project uses a custom user model configured in `settings.py`:
```python
AUTH_USER_MODEL = 'bookshelf.CustomUser'

Media Files
Profile photos are stored in the media/profile_photos/ directory.

Management Commands
setup_groups - Creates default groups and assigns permissions automatically

Dependencies
Django

Pillow (for ImageField support)

For detailed permissions documentation, see PERMISSIONS_README.md in the project root.
EOF


## Step 8: Verify the README was created

```bash
# Check the file was created
ls -la LibraryProject/README.md

# Check the content
echo "=== README Content Preview ==="
head -5 LibraryProject/README.md
echo "..."
tail -5 LibraryProject/README.md
echo "=== Total lines ==="
wc -l LibraryProject/README.md
