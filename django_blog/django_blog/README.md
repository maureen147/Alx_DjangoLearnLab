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
# Django Blog - Comment System

## Features Implemented
- Comment model with ForeignKey relationships to Post and User
- CommentForm for creating/editing comments
- Generic views for CRUD operations:
  - CommentCreateView
  - CommentUpdateView  
  - CommentDeleteView
- Permission enforcement (only authors can edit/delete)
- Templates for all comment operations
- Integration with existing blog post system

## How to Use
1. Navigate to a blog post
2. Login to add comments
3. Comment authors can edit/delete their comments
4. All users can read comments

## URLs
- Add comment: `/post/<pk>/comment/`
- Edit comment: `/comment/<pk>/edit/`
- Delete comment: `/comment/<pk>/delete/`