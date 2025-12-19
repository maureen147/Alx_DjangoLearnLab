# Social Media API - User Authentication

## Project Setup

1. Navigate to the project directory: cd social_media_api
2. Install dependencies: pip install -r requirements.txt
3. Run migrations: python manage.py migrate
4. Create superuser (optional): python manage.py createsuperuser
5. Run development server: python manage.py runserver

## API Endpoints

### User Registration
- **URL**: /register/
- **Method**: POST
- **Data**: {"username": "", "email": "", "password": "", "bio": "", "profile_picture": ""}
- **Response**: Returns authentication token

### User Login
- **URL**: /login/
- **Method**: POST
- **Data**: {"username": "", "password": ""}
- **Response**: Returns authentication token

### User Profile
- **URL**: /profile/
- **Method**: GET (view profile), PUT (update profile)
- **Authentication**: Token required
- **Headers**: Authorization: Token <your_token>

## User Model
Custom user model extends Django's AbstractUser with:
- bio: Text field for user biography
- profile_picture: URL field for profile image
- followers: Many-to-many relationship with other users

## Authentication
Uses Django REST Framework Token Authentication.
Include token in request headers: "Authorization: Token <your_token>"
