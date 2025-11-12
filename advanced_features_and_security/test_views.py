#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.LibraryProject.settings')
django.setup()

from bookshelf.views import book_list, add_book, edit_book, delete_book
import inspect

def test_views():
    print("Testing Views and Permission Decorators...")
    
    # Check if book_list view exists and has permission decorator
    book_list_func = book_list
    print(f"book_list function: {book_list_func}")
    
    # Check decorators on book_list
    source = inspect.getsource(book_list)
    print("book_list source code:")
    print(source)
    
    # Check all views for permission decorators
    views_to_check = [
        ('book_list', book_list),
        ('add_book', add_book),
        ('edit_book', edit_book),
        ('delete_book', delete_book),
    ]
    
    for view_name, view_func in views_to_check:
        source = inspect.getsource(view_func)
        print(f"\n{view_name} permission checks:")
        if '@permission_required' in source:
            print(f"  ✅ {view_name} has @permission_required decorator")
        else:
            print(f"  ❌ {view_name} missing @permission_required decorator")
    
    print("\n✅ Views testing completed!")

if __name__ == '__main__':
    test_views()
