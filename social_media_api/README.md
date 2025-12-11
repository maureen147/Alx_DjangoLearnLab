# Social Media API

A Django REST Framework based Social Media API with user authentication and profile management.

## Features

- Custom user model with bio, profile picture, and followers system
- Token-based authentication
- User registration, login, and logout
- User profile management
- Follow/unfollow functionality
- RESTful API endpoints

## Setup Instructions

### 1. Clone and Install Dependencies

```bash
# Clone the repository
git clone <your-repo-url>
cd social_media_api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt