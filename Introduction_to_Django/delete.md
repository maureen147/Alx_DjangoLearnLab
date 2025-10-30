# DELETE Operation

## Command:
\`\`\`python
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print(f"Books remaining: {Book.objects.count()}")
\`\`\`

## Expected Output:
Books remaining: 0
