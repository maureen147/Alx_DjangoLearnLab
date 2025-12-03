from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from taggit.models import Tag  # Import Tag from django-taggit
from .models import Post, Comment
from .forms import PostForm, CommentForm, SearchForm

def home(request):
    recent_posts = Post.objects.order_by('-published_date')[:5]
    
    # Get popular tags from django-taggit
    from taggit.models import Tag
    popular_tags = Tag.objects.annotate(
        num_times=models.Count('taggit_taggeditem_items')
    ).order_by('-num_times')[:10]
    
    return render(request, 'blog/home.html', {
        'recent_posts': recent_posts,
        'popular_tags': popular_tags,
        'search_form': SearchForm()
    })

def register_view(request):
    # Your registration logic
    return render(request, 'blog/register.html')

def login_view(request):
    # Your login logic
    return render(request, 'blog/login.html')

def logout_view(request):
    # Your logout logic
    pass

def profile_view(request):
    # Your profile logic
    return render(request, 'blog/profile.html')

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['form'] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Your post has been updated successfully!')
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

# Comment views (keep your existing ones)
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        form.instance.author = self.request.user
        form.instance.post = post
        messages.success(self.request, 'Your comment has been added!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.kwargs.get('pk')})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Your comment has been updated!')
        return super().form_valid(form)
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        comment = self.get_object()
        return reverse('post-detail', kwargs={'pk': comment.post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your comment has been deleted!')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        comment = self.get_object()
        return reverse('post-detail', kwargs={'pk': comment.post.pk})

# Search and Tag views
def search_posts(request):
    form = SearchForm(request.GET or None)
    posts = Post.objects.all()
    query = ''
    
    if form.is_valid() and form.cleaned_data.get('query'):
        query = form.cleaned_data['query']
        search_in = form.cleaned_data.get('search_in', 'all')
        
        # Build Q objects for search
        q_objects = Q()
        
        if search_in in ['all', 'title']:
            q_objects |= Q(title__icontains=query)
        
        if search_in in ['all', 'content']:
            q_objects |= Q(content__icontains=query)
        
        if search_in in ['all', 'tags']:
            q_objects |= Q(tags__name__icontains=query)
        
        posts = posts.filter(q_objects).distinct()
    
    return render(request, 'blog/search_results.html', {
        'form': form,
        'posts': posts,
        'query': query
    })

class PostsByTagView(ListView):
    model = Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        # Get tag from django-taggit
        from taggit.models import Tag
        self.tag = get_object_or_404(Tag, slug=self.kwargs.get('tag_slug'))
        return Post.objects.filter(tags=self.tag).order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context