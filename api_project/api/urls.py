from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Author URLs
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('authors/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),
    
    # Book URLs using the exact generic view names
    path('books/', views.ListView.as_view(), name='book-list'),
    path('books/create/', views.CreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', views.DetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/update/', views.UpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.DeleteView.as_view(), name='book-delete'),
]