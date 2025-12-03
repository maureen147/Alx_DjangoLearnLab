from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post, Profile
from .forms import UserRegisterForm, PostForm

def home(request):
    return render(request, 'blog/home.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        errors = []
        
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters long.')
        
        if User.objects.filter(username=username).exists():
            errors.append('This username is already taken.')
        
        try:
            validate_email(email)
        except ValidationError:
            errors.append('Please enter a valid email address.')
        
        if User.objects.filter(email=email).exists():
            errors.append('This email is already in use.')
        
        if not password1 or len(password1) < 8:
            errors.append('Password must be at least 8 characters long.')
        
        if password1 != password2:
            errors.append('Passwords do not match.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            context = {
                'username': username,
                'email': email,
            }
            return render(request, 'blog/register.html', context)
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    
    return render(request, 'blog/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'blog/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        bio = request.POST.get('bio', '')
        profile_pic = request.FILES.get('profile_pic')
        
        errors = []
        
        if username != request.user.username:
            if User.objects.filter(username=username).exclude(pk=request.user.pk).exists():
                errors.append('This username is already taken.')
        
        if email != request.user.email:
            if User.objects.filter(email=email).exclude(pk=request.user.pk).exists():
                errors.append('This email is already in use.')
        
        try:
            validate_email(email)
        except ValidationError:
            errors.append('Please enter a valid email address.')
        
        if profile_pic and profile_pic.size > 5 * 1024 * 1024:
            errors.append('Image file too large (maximum 5MB)')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            user = request.user
            user.username = username
            user.email = email
            user.save()
            
            profile = user.profile
            profile.bio = bio
            if profile_pic:
                profile.profile_pic = profile_pic
            profile.save()
            
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    
    context = {
        'user': request.user,
    }
    return render(request, 'blog/profile.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created!')
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been updated!')
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Your post has been deleted!')
        return super().delete(request, *args, **kwargs)
