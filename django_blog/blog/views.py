from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import CommentForm

# Your existing views
def home(request):
    return render(request, 'blog/home.html')

def register_view(request):
    # Your register view
    pass

def login_view(request):
    # Your login view
    pass

def logout_view(request):
    # Your logout view
    pass

def profile_view(request):
    # Your profile view
    pass

# Your existing Post views
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_date']
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comment_set.all().order_by('-created_at')
        context['form'] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
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

# NEW: Comment Generic Views
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        # Get the post from URL parameter
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

# Keep your existing function-based views or remove them if using generic views
@login_required
def add_comment(request, pk):
    # You can keep this or use CommentCreateView instead
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('post-detail', pk=post.pk)
    return redirect('post-detail', pk=post.pk)

@login_required
def edit_comment(request, pk):
    # You can keep this or use CommentUpdateView instead
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        messages.error(request, 'You are not authorized to edit this comment.')
        return redirect('post-detail', pk=comment.post.pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your comment has been updated!')
            return redirect('post-detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'blog/comment_form.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, pk):
    # You can keep this or use CommentDeleteView instead
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        messages.error(request, 'You are not authorized to delete this comment.')
        return redirect('post-detail', pk=comment.post.pk)
    
    if request.method == 'POST':
        post_pk = comment.post.pk
        comment.delete()
        messages.success(request, 'Your comment has been deleted!')
        return redirect('post-detail', pk=post_pk)
    
    return render(request, 'blog/comment_confirm_delete.html', {'comment': comment})