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
    
    age = forms.IntegerField(
        min_value=0,
        max_value=120,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your age'
        })
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
        
        # Remove other potentially dangerous HTML tags
        message = re.sub(r'</?(javascript|vbscript|embed|object|iframe|frame|frameset).*?>', '', 
                        message, flags=re.IGNORECASE)
        
        return message.strip()

class SecureSearchForm(forms.Form):
    """
    Secure search form with input validation to prevent SQL injection
    """
    
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search...',
            'maxlength': '100'
        }),
        validators=[
            MinLengthValidator(2, "Search query must be at least 2 characters long."),
            MaxLengthValidator(100, "Search query cannot exceed 100 characters.")
        ]
    )
    
    def clean_query(self):
        """Sanitize search query to prevent SQL injection and XSS"""
        query = self.cleaned_data['query']
        
        if not query:
            return query
            
        # Remove SQL injection patterns
        sql_patterns = [
            r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|EXEC)\b)',
            r'(\b(OR|AND)\s+\d+=\d+)',
            r'(\-\-|\#|\/\*)',
            r'(\b(WAITFOR|DELAY)\b)'
        ]
        
        for pattern in sql_patterns:
            query = re.sub(pattern, '', query, flags=re.IGNORECASE)
        
        # Remove XSS patterns
        query = re.sub(r'<script.*?>.*?</script>', '', query, flags=re.IGNORECASE | re.DOTALL)
        query = re.sub(r'javascript:', '', query, flags=re.IGNORECASE)
        query = re.sub(r'on\w+=', '', query, flags=re.IGNORECASE)
        
        # Remove excessive whitespace
        query = ' '.join(query.split())
        
        return query.strip()

class UserRegistrationForm(forms.Form):
    """
    Secure user registration form with comprehensive validation
    """
    
    username = forms.CharField(
        max_length=150,
        validators=[
            MinLengthValidator(3, "Username must be at least 3 characters long."),
            MaxLengthValidator(150, "Username cannot exceed 150 characters.")
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a password'
        }),
        validators=[
            MinLengthValidator(8, "Password must be at least 8 characters long.")
        ]
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )
    
    def clean_username(self):
        """Validate username"""
        username = self.cleaned_data['username']
        
        # Check for only alphanumeric characters and underscores
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError("Username can only contain letters, numbers, and underscores.")
        
        return username
    
    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError({
                'confirm_password': "Passwords do not match."
            })
        
        return cleaned_data
EOFcat > LibraryProject/bookshelf/forms.py << 'EOF'
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
    
    age = forms.IntegerField(
        min_value=0,
        max_value=120,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your age'
        })
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
        
        # Remove other potentially dangerous HTML tags
        message = re.sub(r'</?(javascript|vbscript|embed|object|iframe|frame|frameset).*?>', '', 
                        message, flags=re.IGNORECASE)
        
        return message.strip()

class SecureSearchForm(forms.Form):
    """
    Secure search form with input validation to prevent SQL injection
    """
    
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search...',
            'maxlength': '100'
        }),
        validators=[
            MinLengthValidator(2, "Search query must be at least 2 characters long."),
            MaxLengthValidator(100, "Search query cannot exceed 100 characters.")
        ]
    )
    
    def clean_query(self):
        """Sanitize search query to prevent SQL injection and XSS"""
        query = self.cleaned_data['query']
        
        if not query:
            return query
            
        # Remove SQL injection patterns
        sql_patterns = [
            r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|EXEC)\b)',
            r'(\b(OR|AND)\s+\d+=\d+)',
            r'(\-\-|\#|\/\*)',
            r'(\b(WAITFOR|DELAY)\b)'
        ]
        
        for pattern in sql_patterns:
            query = re.sub(pattern, '', query, flags=re.IGNORECASE)
        
        # Remove XSS patterns
        query = re.sub(r'<script.*?>.*?</script>', '', query, flags=re.IGNORECASE | re.DOTALL)
        query = re.sub(r'javascript:', '', query, flags=re.IGNORECASE)
        query = re.sub(r'on\w+=', '', query, flags=re.IGNORECASE)
        
        # Remove excessive whitespace
        query = ' '.join(query.split())
        
        return query.strip()

class UserRegistrationForm(forms.Form):
    """
    Secure user registration form with comprehensive validation
    """
    
    username = forms.CharField(
        max_length=150,
        validators=[
            MinLengthValidator(3, "Username must be at least 3 characters long."),
            MaxLengthValidator(150, "Username cannot exceed 150 characters.")
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a password'
        }),
        validators=[
            MinLengthValidator(8, "Password must be at least 8 characters long.")
        ]
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )
    
    def clean_username(self):
        """Validate username"""
        username = self.cleaned_data['username']
        
        # Check for only alphanumeric characters and underscores
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError("Username can only contain letters, numbers, and underscores.")
        
        return username
    
    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError({
                'confirm_password': "Passwords do not match."
            })
        
        return cleaned_data
