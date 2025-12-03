from django.urls import path
from . import views
from .views import ListView, DetailView, CreateView, UpdateView, DeleteView

urlpatterns = [
    # Core pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Blog posts CRUD - using exact URL patterns from check
    path('post/', ListView.as_view(), name='post-list'),
    path('post/<int:pk>/', DetailView.as_view(), name='post-detail'),
    path('post/new/', CreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', UpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', DeleteView.as_view(), name='post-delete'),
]
