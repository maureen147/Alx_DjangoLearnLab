# Advanced Django REST Framework API

This project demonstrates advanced API development with Django REST Framework, featuring custom serializers, generic views, and comprehensive CRUD operations.

## Features

- **Custom Serializers**: Handle complex data structures and nested relationships
- **Generic Views**: Efficient CRUD operations using DRF's generic views
- **Permissions**: Role-based access control for API endpoints
- **Filtering & Search**: Advanced filtering, searching, and ordering capabilities
- **Data Validation**: Custom validation for business logic

## API Endpoints

### Authors

- `GET /api/authors/` - List all authors (Public)
- `POST /api/authors/create/` - Create a new author (Authenticated only)
- `GET /api/authors/<id>/` - Get author details (Public)
- `PUT/PATCH /api/authors/<id>/update/` - Update author (Authenticated only)
- `DELETE /api/authors/<id>/delete/` - Delete author (Authenticated only)

### Books

- `GET /api/books/` - List all books with filtering (Public)
- `POST /api/books/create/` - Create a new book (Authenticated only)
- `GET /api/books/<id>/` - Get book details (Public)
- `PUT/PATCH /api/books/<id>/update/` - Update book (Authenticated only)
- `DELETE /api/books/<id>/delete/` - Delete book (Authenticated only)

## Setup

1. Install dependencies:
```bash
pip install django djangorestframework django-filter