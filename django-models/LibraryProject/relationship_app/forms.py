from django import forms
from .models import Book, Author

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'libraries']
        widgets = {
            'libraries': forms.CheckboxSelectMultiple(),
        }
