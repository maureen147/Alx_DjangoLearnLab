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
## Filtering, Searching and Ordering

The Book ListView supports advanced query capabilities:

### Filtering
- Filter by publication_year: `?publication_year=2020`
- Filter by author: `?author=1`

### Searching  
- Search in title and author name: `?search=harry`

### Ordering
- Order by title: `?ordering=title`
- Order by publication_year: `?ordering=-publication_year`
- Order by author name: `?ordering=author__name`

### Examples:
- Search and filter: `/api/books/?search=potter&publication_year=1997`
- Filter and order: `/api/books/?author=1&ordering=-publication_year`
- All features: `/api/books/?search=rowling&publication_year=1997&ordering=title`

## Testing

### Running Tests

To run the test suite:

\`\`\`bash
python manage.py test api
\`\`\`

### Test Coverage

The test suite covers:

**Book API Tests:**
- List books (unauthorized access)
- Create book (authorized/unauthorized)
- Retrieve book details  
- Update book (authorized/unauthorized)
- Delete book (authorized/unauthorized)
- Filter by publication_year and author
- Search by title and author name
- Order by title and publication_year
- Combined filtering, searching, ordering
- Validation for publication_year

**Author API Tests:**
- List authors
- Create author (authorized/unauthorized)

### Test Structure

- Uses Django's TestCase and APIClient
- Sets up test database automatically
- Tests both authenticated and unauthenticated access
- Verifies status codes and response data
- Tests all CRUD operations
- Tests filtering, searching, and ordering features

### Example Test Run

\`\`\`bash
python manage.py test api -v 2
\`\`\`

This will show detailed test output including all test methods and their results.
