from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from bookshelf.models import Book, Author
from django import forms

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

# Book list view - requires can_view permission
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

# View to list books (alternative name) - requires can_view permission
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def list_books(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/list_books.html', {'books': books})

# View to create a new book - requires can_create permission
@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book created successfully!')
            return redirect('bookshelf:book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/add_book.html', {'form': form})

# View to edit a book - requires can_edit permission
@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('bookshelf:book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/edit_book.html', {'form': form, 'book': book})

# View to delete a book - requires can_delete permission
@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('bookshelf:book_list')
    return render(request, 'bookshelf/delete_book.html', {'book': book})

# Public view that doesn't require special permissions
def book_detail(request, book_id):
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
    books = Book.objects.all()
    return render(request, 'bookshelf/admin_view.html', {'books': books})
