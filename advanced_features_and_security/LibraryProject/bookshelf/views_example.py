from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import ExampleForm, SecureSearchForm, UserRegistrationForm

def example_form_view(request):
    """
    View demonstrating secure form handling with ExampleForm
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process secure data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            age = form.cleaned_data['age']
            
            # In a real application, you would save to database here
            # For demonstration, we'll just show a success message
            
            messages.success(request, 
                f"Thank you {name}! Your message has been securely processed.")
            return HttpResponseRedirect('/bookshelf/example-form/success/')
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/example_form.html', {'form': form})

def secure_search_view(request):
    """
    View demonstrating secure search functionality
    """
    results = []
    query = ""
    
    if request.method == 'GET':
        form = SecureSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            
            # Safe search using Django ORM (example)
            if query:
                from .models import Book
                results = Book.objects.filter(title__icontains=query)[:10]
    else:
        form = SecureSearchForm()
    
    return render(request, 'bookshelf/secure_search.html', {
        'form': form,
        'results': results,
        'query': query
    })

def user_registration_view(request):
    """
    View demonstrating secure user registration
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Process registration data
            username = form.cleaned_data['username']
            
            messages.success(request, 
                f"Account created successfully for {username}!")
            return HttpResponseRedirect('/bookshelf/registration/success/')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'bookshelf/user_registration.html', {'form': form})

def example_form_success(request):
    """Success page for example form submission"""
    return render(request, 'bookshelf/example_form_success.html')

def registration_success(request):
    """Success page for registration"""
    return render(request, 'bookshelf/registration_success.html')
