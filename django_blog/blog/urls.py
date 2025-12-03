from django.urls import path
from .views import ListView, DetailView, CreateView, UpdateView, DeleteView

urlpatterns = [
    path('posts/', ListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', DetailView.as_view(), name='post-detail'),
    path('posts/new/', CreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/edit/', UpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', DeleteView.as_view(), name='post-delete'),
]
