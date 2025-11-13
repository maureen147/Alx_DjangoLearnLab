from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
import re

class ExampleForm(forms.Form):
    """
    Example form demonstrating secure form practices including:
    - CSRF protection (handled by template)
    - Input validation
    - Data sanitization
    - Security best practices
    """
    
    name = forms.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2, "Name must be at least 2 characters long."),
            MaxLengthValidator(100, "Name cannot exceed 100 characters.")
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name'
        })
    )
    
    email = forms.EmailField(
        max_length=150,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your message',
            'rows': 4
        }),
        validators=[
            MinLengthValidator(10, "Message must be at least 10 characters long."),
            MaxLengthValidator(1000, "Message cannot exceed 1000 characters.")
        ]
    )
    
    def clean_name(self):
        """Sanitize and validate name field"""
        name = self.cleaned_data['name']
        
        # Remove potentially dangerous characters
        name = re.sub(r'[<>{}]', '', name)
        
        # Check for only allowed characters
        if not re.match(r'^[a-zA-Z\s\-\'\.]+$', name):
            raise ValidationError("Name can only contain letters, spaces, hyphens, apostrophes, and periods.")
        
        return name.strip()
    
    def clean_message(self):
        """Sanitize and validate message field"""
        message = self.cleaned_data['message']
        
        # Basic XSS prevention - remove script tags
        message = re.sub(r'<script.*?>.*?</script>', '', message, flags=re.IGNORECASE | re.DOTALL)
        
        return message.strip()
