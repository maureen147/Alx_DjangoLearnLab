"""
Sample queries demonstrating Django ORM relationships
"""

from relationship_app.models import Author, Book, Library, Librarian

def query_all_books_by_author(author_name):
    """Query all books by a specific author - ForeignKey relationship"""
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"Books by {author_name}:")
        for book in books:
            print(f" - {book.title}")
        return books
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found")
        return []

def list_all_books_in_library(library_name):
    """List all books in a library - ManyToMany relationship"""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library_name} library:")
        for book in books:
            print(f" - {book.title} by {book.author.name}")
        return books
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found")
        return []

def retrieve_librarian_for_library(library_name):
    """Retrieve the librarian for a library - OneToOne relationship"""
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        print(f"Librarian for {library_name}: {librarian.name}")
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        print(f"No librarian found for library '{library_name}'")
        return None

# Demonstration of all relationships
if __name__ == "__main__":
    print("Django ORM Relationship Examples")
    print("=" * 50)
    
    # Create sample data for testing
    author1 = Author.objects.create(name="George Orwell")
    author2 = Author.objects.create(name="J.K. Rowling")
    
    book1 = Book.objects.create(title="1984", author=author1)
    book2 = Book.objects.create(title="Animal Farm", author=author1)
    book3 = Book.objects.create(title="Harry Potter", author=author2)
    
    library = Library.objects.create(name="Central Library")
    library.books.add(book1, book2, book3)
    
    librarian = Librarian.objects.create(name="Alice Johnson", library=library)
    
    print("Sample data created successfully!")
    print("\n" + "="*50)
    
    # Test ForeignKey relationship
    print("1. ForeignKey Relationship - Books by Author")
    query_all_books_by_author("George Orwell")
    
    print("\n2. ManyToMany Relationship - Books in Library")
    list_all_books_in_library("Central Library")
    
    print("\n3. OneToOne Relationship - Librarian for Library")
    retrieve_librarian_for_library("Central Library")