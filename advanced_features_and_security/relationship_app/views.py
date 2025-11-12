from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Book, Author, Library
from .forms import BookForm

# View to list books - requires can_view_book permission
@login_required
@permission_required('relationship_app.can_view_book', raise_exception=True)
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# View to create a new book - requires can_create_book permission
@login_required
@permission_required('relationship_app.can_create_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book created successfully!')
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})

# View to edit a book - requires can_edit_book permission
@login_required
@permission_required('relationship_app.can_edit_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})

# View to delete a book - requires can_delete_book permission
@login_required
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})

# Public view that doesn't require special permissions
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'relationship_app/book_detail.html', {'book': book})

# Dashboard view that shows different content based on permissions
@login_required
def dashboard(request):
    user = request.user
    context = {
        'can_view': user.has_perm('relationship_app.can_view_book'),
        'can_create': user.has_perm('relationship_app.can_create_book'),
        'can_edit': user.has_perm('relationship_app.can_edit_book'),
        'can_delete': user.has_perm('relationship_app.can_delete_book'),
    }
    return render(request, 'relationship_app/dashboard.html', context)

# Admin view for managing books (requires all permissions)
@login_required
@permission_required([
    'relationship_app.can_view_book',
    'relationship_app.can_create_book', 
    'relationship_app.can_edit_book',
    'relationship_app.can_delete_book'
], raise_exception=True)
def admin_view(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/admin_view.html', {'books': books})
