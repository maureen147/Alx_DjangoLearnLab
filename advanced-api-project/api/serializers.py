from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    BookSerializer handles serialization and deserialization of Book instances.
    
    This serializer includes custom validation to ensure that the publication_year
    is not in the future. It serializes all fields from the Book model and
    provides validation for the publication_year field.
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        
        Ensures that the publication year is not in the future.
        Raises a validation error if the year is greater than the current year.
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    AuthorSerializer handles serialization and deserialization of Author instances.
    
    This serializer includes a nested BookSerializer to handle the one-to-many
    relationship between Author and Book. The 'books' field uses the BookSerializer
    to serialize all books related to the author, providing a nested representation
    of the relationship.
    """
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
