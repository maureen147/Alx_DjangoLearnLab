from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book

class BookAPITestCase(TestCase):
    """
    Test case for Book API endpoints including CRUD operations,
    filtering, searching, ordering, and permissions.
    """
    
    def setUp(self):
        """
        Set up test data and client for all test cases.
        """
        self.client = APIClient()
        
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpassword123',
            email='admin@test.com'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George Orwell')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author2
        )
        self.book4 = Book.objects.create(
            title='Animal Farm',
            publication_year=1945,
            author=self.author2
        )
    
    def test_list_books_unauthorized(self):
        """
        Test that unauthenticated users can list books (read-only access).
        """
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
    
    def test_create_book_unauthorized(self):
        """
        Test that unauthenticated users cannot create books.
        """
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_book_authorized(self):
        """
        Test that authenticated users can create books.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 5)
        self.assertEqual(response.data['title'], 'New Book')
    
    def test_retrieve_book_detail(self):
        """
        Test retrieving a single book detail.
        """
        response = self.client.get(f'/api/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
    
    def test_update_book_unauthorized(self):
        """
        Test that unauthenticated users cannot update books.
        """
        data = {'title': 'Updated Title'}
        response = self.client.patch(f'/api/books/update/{self.book1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_book_authorized(self):
        """
        Test that authenticated users can update books.
        """
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Title'}
        response = self.client.patch(f'/api/books/update/{self.book1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')
    
    def test_delete_book_unauthorized(self):
        """
        Test that unauthenticated users cannot delete books.
        """
        response = self.client.delete(f'/api/books/delete/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_book_authorized(self):
        """
        Test that authenticated users can delete books.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/books/delete/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 3)
    
    def test_filter_books_by_publication_year(self):
        """
        Test filtering books by publication year.
        """
        response = self.client.get('/api/books/?publication_year=1997')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter and the Philosopher\'s Stone')
    
    def test_filter_books_by_author(self):
        """
        Test filtering books by author.
        """
        response = self.client.get(f'/api/books/?author={self.author2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_search_books_by_title(self):
        """
        Test searching books by title.
        """
        response = self.client.get('/api/books/?search=Harry')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_search_books_by_author_name(self):
        """
        Test searching books by author name.
        """
        response = self.client.get('/api/books/?search=Orwell')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_order_books_by_title(self):
        """
        Test ordering books by title.
        """
        response = self.client.get('/api/books/?ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))
    
    def test_order_books_by_publication_year_desc(self):
        """
        Test ordering books by publication year descending.
        """
        response = self.client.get('/api/books/?ordering=-publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
    
    def test_combined_filter_search_order(self):
        """
        Test combining filtering, searching, and ordering.
        """
        response = self.client.get('/api/books/?author=1&search=Harry&ordering=-publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Should be ordered by publication year descending
        self.assertEqual(response.data[0]['publication_year'], 1998)
        self.assertEqual(response.data[1]['publication_year'], 1997)
    
    def test_create_book_validation(self):
        """
        Test that book creation validates publication_year (cannot be in future).
        """
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Future Book',
            'publication_year': 2030,  # Future year
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)


class AuthorAPITestCase(TestCase):
    """
    Test case for Author API endpoints.
    """
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.author = Author.objects.create(name='Test Author')
    
    def test_list_authors(self):
        """
        Test listing all authors.
        """
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_author_unauthorized(self):
        """
        Test that unauthenticated users cannot create authors.
        """
        data = {'name': 'New Author'}
        response = self.client.post('/api/authors/create/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_author_authorized(self):
        """
        Test that authenticated users can create authors.
        """
        self.client.force_authenticate(user=self.user)
        data = {'name': 'New Author'}
        response = self.client.post('/api/authors/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)
