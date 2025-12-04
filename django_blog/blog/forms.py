from django import forms
from .models import Post, Comment
from taggit.utils import parse_tags
from taggit.forms import TagWidget  # Import TagWidget from django-taggit

# Custom TagWidget for better tag input
class CustomTagWidget(TagWidget):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas (e.g., django, python, web)',
            'data-role': 'tagsinput'
        })
        super().__init__(*args, **kwargs)

class PostForm(forms.ModelForm):
    # Use the CustomTagWidget for tags field
    tags = forms.CharField(
        required=False,
        widget=CustomTagWidget(),
        help_text='Separate tags with commas. Tags will be created automatically.'
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Write your post content here...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # For existing posts, populate tags field with current tags
            tags = self.instance.tags.all()
            self.fields['tags'].initial = ', '.join([tag.name for tag in tags])
    
    def clean_tags(self):
        tags_input = self.cleaned_data.get('tags', '')
        if tags_input:
            # Parse tags using django-taggit's utility
            tag_names = parse_tags(tags_input)
            return tag_names
        return []
    
    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
            # Save tags using django-taggit
            tag_names = self.cleaned_data.get('tags', [])
            if tag_names:
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