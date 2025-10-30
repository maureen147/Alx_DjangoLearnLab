# UPDATE Operation

## Command:
\`\`\`python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated title: {book.title}")
\`\`\`

## Expected Output:
Updated title: Nineteen Eighty-Four
