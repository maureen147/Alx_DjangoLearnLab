# DELETE Operation

## Command:
\`\`\`python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print(f"Books remaining: {Book.objects.count()}")
\`\`\`

## Expected Output:
Books remaining: 0
