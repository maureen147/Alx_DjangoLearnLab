# Django Blog Project

A simple blogging platform built with Django.

## Features

- User authentication and authorization
- Create, read, update, and delete blog posts
- Responsive design
- Admin interface for content management

## Setup Instructions

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install django`
5. Run migrations: `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Run development server: `python manage.py runserver`

## Project Structure

- `django_blog/` - Main project directory
- `blog/` - Blog application
  - `models.py` - Database models
  - `views.py` - View functions
  - `urls.py` - URL routing
  - `templates/` - HTML templates
  - `static/` - Static files (CSS, JS, images)

## Access Points

- Home page: http://127.0.0.1:8000/
- Blog posts: http://127.0.0.1:8000/posts/
- Admin panel: http://127.0.0.1:8000/admin/
