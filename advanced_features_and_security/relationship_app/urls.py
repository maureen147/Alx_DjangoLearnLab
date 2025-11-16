from django.urls import path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import views



@login_required
def permission_test(request):
    return render(request, 'relationship_app/permission_test.html')

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-view/', views.admin_view, name='admin_view'),
    path('permission-test/', permission_test, name='permission_test'),
    # ADD THIS LINE for the library detail view:
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]