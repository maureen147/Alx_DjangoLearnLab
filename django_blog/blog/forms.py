from django import forms
from .models import Post, Comment
from taggit.utils import parse_tags  # Import from django-taggit

class PostForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter tags separated by commas (e.g., django, python, web)',
            'class': 'form-control'
        }),
        help_text='Separate tags with commas. Tags will be created automatically.'
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter post title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Write your post content here...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # For existing posts, populate tags_input with current tags
            tags = self.instance.tags.all()
            self.fields['tags_input'].initial = ', '.join([tag.name for tag in tags])
    
    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
            # Save tags using django-taggit
            tags_input = self.cleaned_data.get('tags_input', '')
            if tags_input:
                tag_names = parse_tags(tags_input)
                post.tags.set(*tag_names)
            self.save_m2m()
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            })
        }
        labels = {
            'content': 'Your Comment'
        }

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search posts by title, content, or tags...',
            'class': 'form-control'
        })
    )
    search_in = forms.ChoiceField(
        choices=[
            ('all', 'All Fields'),
            ('title', 'Title Only'),
            ('content', 'Content Only'),
            ('tags', 'Tags Only')
        ],
        required=False,
        initial='all',
        widget=forms.Select(attrs={'class': 'form-control'})
    )