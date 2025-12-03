from django.urls import path
from .views import ListView, DetailView, CreateView, UpdateView, DeleteView

urlpatterns = [
    path('post/', ListView.as_view(), name='post-list'),
    path('post/<int:pk>/', DetailView.as_view(), name='post-detail'),
    path('post/new/', CreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', UpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', DeleteView.as_view(), name='post-delete'),
]
