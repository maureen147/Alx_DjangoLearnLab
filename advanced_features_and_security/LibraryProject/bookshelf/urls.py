from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('books/list/', views.list_books, name='list_books'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-view/', views.admin_view, name='admin_view'),
]
from . import views_example

urlpatterns += [
    path('example-form/', views_example.example_form_view, name='example_form'),
    path('example-form/success/', views_example.example_form_success, name='example_form_success'),
    path('secure-search/', views_example.secure_search_view, name='secure_search'),
    path('user-registration/', views_example.user_registration_view, name='user_registration'),
    path('registration/success/', views_example.registration_success, name='registration_success'),
]
