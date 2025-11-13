from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from bookshelf.models import Book, Author
from django import forms
from .forms import ExampleForm, SecureSearchForm  # Import ExampleForm
import logging

logger = logging.getLogger(__name__)

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
    
    def clean_title(self):
        """Sanitize and validate title input"""
        title = self.cleaned_data['title']
        # Remove potentially dangerous characters
        title = ''.join(char for char in title if char.isalnum() or char in ' .,!?-')
        if len(title) < 2:
            raise forms.ValidationError("Title must be at least 2 characters long.")
        return title.strip()
    
    def clean_publication_year(self):
        """Validate publication year"""
        year = self.cleaned_data['publication_year']
        if year < 1000 or year > 2030:
            raise forms.ValidationError("Please enter a valid publication year.")
        return year

# View that uses ExampleForm for security demonstration
@login_required
def example_form_demo(request):
    """View demonstrating ExampleForm with security features"""
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process the secure form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Log the secure form submission
            logger.info(f"User {request.user.username} submitted ExampleForm securely")
            
            messages.success(request, 
                f"Thank you {name}! Your form has been processed securely.")
            return redirect('bookshelf:dashboard')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/example_form_demo.html', {'form': form})

# Book list view - requires can_view permission with secure search
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    # Secure search functionality - using Django ORM to prevent SQL injection
    search_query = request.GET.get('q', '').strip()
    
    if search_query:
        # Use SecureSearchForm for additional validation
        search_form = SecureSearchForm({'query': search_query})
        if search_form.is_valid():
            search_query = search_form.cleaned_data['query']
            # Safe ORM query with parameterized filtering
            books = Book.objects.filter(
                Q(title__icontains=search_query) | 
                Q(author__name__icontains=search_query)
            ).select_related('author')
            
            # Log search activity for security monitoring
            logger.info(f"User {request.user.username} searched for: {search_query}")
        else:
            books = Book.objects.none()
            messages.warning(request, "Invalid search query.")
    else:
        books = Book.objects.all().select_related('author')
        search_form = SecureSearchForm()
    
    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'search_query': search_query,
        'search_form': search_form
    })

# View to create a new book - requires can_create permission
@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            # Safe save using Django ORM
            book = form.save()
            messages.success(request, 'Book created successfully!')
            logger.info(f"User {request.user.username} created book: {book.title}")
            return redirect('bookshelf:book_list')
        else:
            # Form validation failed - potential security issue detected
            logger.warning(f"User {request.user.username} submitted invalid book form")
    else:
        form = BookForm()
    return render(request, 'bookshelf/add_book.html', {'form': form})

# View to edit a book - requires can_edit permission
@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    # Safe object retrieval - prevents unauthorized access
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            logger.info(f"User {request.user.username} updated book: {book.title}")
            return redirect('bookshelf:book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/edit_book.html', {'form': form, 'book': book})

# View to delete a book - requires can_delete permission
@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    # Safe object retrieval
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        logger.info(f"User {request.user.username} deleted book: {book_title}")
        return redirect('bookshelf:book_list')
    return render(request, 'bookshelf/delete_book.html', {'book': book})

# Public view that doesn't require special permissions
def book_detail(request, book_id):
    # Safe object retrieval for public access
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

# Dashboard view that shows different content based on permissions
@login_required
def dashboard(request):
    user = request.user
    context = {
        'can_view': user.has_perm('bookshelf.can_view'),
        'can_create': user.has_perm('bookshelf.can_create'),
        'can_edit': user.has_perm('bookshelf.can_edit'),
        'can_delete': user.has_perm('bookshelf.can_delete'),
    }
    return render(request, 'bookshelf/dashboard.html', context)

# Admin view for managing books (requires all permissions)
@login_required
@permission_required([
    'bookshelf.can_view',
    'bookshelf.can_create', 
    'bookshelf.can_edit',
    'bookshelf.can_delete'
], raise_exception=True)
def admin_view(request):
    books = Book.objects.all().select_related('author')
    return render(request, 'bookshelf/admin_view.html', {'books': books})

# Secure form example view using ExampleForm
@login_required
def form_example(request):
    """Example view demonstrating secure form handling with ExampleForm"""
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Example of secure input handling
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Log the secure form submission
            logger.info(f"Secure form submitted by {request.user.username}: {name}, {email}")
            
            messages.success(request, f'Thank you {name}! Form submitted securely.')
            return redirect('bookshelf:dashboard')
        else:
            messages.error(request, 'Please correct the form errors.')
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})

# Secure search view using SecureSearchForm
@login_required
def secure_search(request):
    """Secure search view using SecureSearchForm"""
    results = []
    query = ""
    
    if request.method == 'GET':
        form = SecureSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            
            # Safe search using Django ORM
            if query:
                results = Book.objects.filter(
                    Q(title__icontains=query) | 
                    Q(author__name__icontains=query)
                )[:10]
                
                logger.info(f"Secure search by {request.user.username}: {query}")
    else:
        form = SecureSearchForm()
    
    return render(request, 'bookshelf/secure_search.html', {
        'form': form,
        'results': results,
        'query': query
    })
EOFcat > LibraryProject/bookshelf/views.py << 'EOF'
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from bookshelf.models import Book, Author
from django import forms
from .forms import ExampleForm, SecureSearchForm  # Import ExampleForm
import logging

logger = logging.getLogger(__name__)

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
    
    def clean_title(self):
        """Sanitize and validate title input"""
        title = self.cleaned_data['title']
        # Remove potentially dangerous characters
        title = ''.join(char for char in title if char.isalnum() or char in ' .,!?-')
        if len(title) < 2:
            raise forms.ValidationError("Title must be at least 2 characters long.")
        return title.strip()
    
    def clean_publication_year(self):
        """Validate publication year"""
        year = self.cleaned_data['publication_year']
        if year < 1000 or year > 2030:
            raise forms.ValidationError("Please enter a valid publication year.")
        return year

# View that uses ExampleForm for security demonstration
@login_required
def example_form_demo(request):
    """View demonstrating ExampleForm with security features"""
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process the secure form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Log the secure form submission
            logger.info(f"User {request.user.username} submitted ExampleForm securely")
            
            messages.success(request, 
                f"Thank you {name}! Your form has been processed securely.")
            return redirect('bookshelf:dashboard')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/example_form_demo.html', {'form': form})

# Book list view - requires can_view permission with secure search
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    # Secure search functionality - using Django ORM to prevent SQL injection
    search_query = request.GET.get('q', '').strip()
    
    if search_query:
        # Use SecureSearchForm for additional validation
        search_form = SecureSearchForm({'query': search_query})
        if search_form.is_valid():
            search_query = search_form.cleaned_data['query']
            # Safe ORM query with parameterized filtering
            books = Book.objects.filter(
                Q(title__icontains=search_query) | 
                Q(author__name__icontains=search_query)
            ).select_related('author')
            
            # Log search activity for security monitoring
            logger.info(f"User {request.user.username} searched for: {search_query}")
        else:
            books = Book.objects.none()
            messages.warning(request, "Invalid search query.")
    else:
        books = Book.objects.all().select_related('author')
        search_form = SecureSearchForm()
    
    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'search_query': search_query,
        'search_form': search_form
    })

# View to create a new book - requires can_create permission
@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            # Safe save using Django ORM
            book = form.save()
            messages.success(request, 'Book created successfully!')
            logger.info(f"User {request.user.username} created book: {book.title}")
            return redirect('bookshelf:book_list')
        else:
            # Form validation failed - potential security issue detected
            logger.warning(f"User {request.user.username} submitted invalid book form")
    else:
        form = BookForm()
    return render(request, 'bookshelf/add_book.html', {'form': form})

# View to edit a book - requires can_edit permission
@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    # Safe object retrieval - prevents unauthorized access
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            logger.info(f"User {request.user.username} updated book: {book.title}")
            return redirect('bookshelf:book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/edit_book.html', {'form': form, 'book': book})

# View to delete a book - requires can_delete permission
@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    # Safe object retrieval
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        logger.info(f"User {request.user.username} deleted book: {book_title}")
        return redirect('bookshelf:book_list')
    return render(request, 'bookshelf/delete_book.html', {'book': book})

# Public view that doesn't require special permissions
def book_detail(request, book_id):
    # Safe object retrieval for public access
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

# Dashboard view that shows different content based on permissions
@login_required
def dashboard(request):
    user = request.user
    context = {
        'can_view': user.has_perm('bookshelf.can_view'),
        'can_create': user.has_perm('bookshelf.can_create'),
        'can_edit': user.has_perm('bookshelf.can_edit'),
        'can_delete': user.has_perm('bookshelf.can_delete'),
    }
    return render(request, 'bookshelf/dashboard.html', context)

# Admin view for managing books (requires all permissions)
@login_required
@permission_required([
    'bookshelf.can_view',
    'bookshelf.can_create', 
    'bookshelf.can_edit',
    'bookshelf.can_delete'
], raise_exception=True)
def admin_view(request):
    books = Book.objects.all().select_related('author')
    return render(request, 'bookshelf/admin_view.html', {'books': books})

# Secure form example view using ExampleForm
@login_required
def form_example(request):
    """Example view demonstrating secure form handling with ExampleForm"""
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Example of secure input handling
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Log the secure form submission
            logger.info(f"Secure form submitted by {request.user.username}: {name}, {email}")
            
            messages.success(request, f'Thank you {name}! Form submitted securely.')
            return redirect('bookshelf:dashboard')
        else:
            messages.error(request, 'Please correct the form errors.')
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})

# Secure search view using SecureSearchForm
@login_required
def secure_search(request):
    """Secure search view using SecureSearchForm"""
    results = []
    query = ""
    
    if request.method == 'GET':
        form = SecureSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            
            # Safe search using Django ORM
            if query:
                results = Book.objects.filter(
                    Q(title__icontains=query) | 
                    Q(author__name__icontains=query)
                )[:10]
                
                logger.info(f"Secure search by {request.user.username}: {query}")
    else:
        form = SecureSearchForm()
    
    return render(request, 'bookshelf/secure_search.html', {
        'form': form,
        'results': results,
        'query': query
    })
