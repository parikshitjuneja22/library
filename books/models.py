from django.db import models
from django.utils import timezone

class Book(models.Model):
    """Represents a book in the library."""
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    available = models.BooleanField(default=True)
    borrow_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} by {self.author}"

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"

class Borrower(models.Model):
    """Represents a borrower in the library system."""
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    membership_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Borrower"
        verbose_name_plural = "Borrowers"

class Loan(models.Model):
    """Represents a book loan between a borrower and a book."""
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    borrowed_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} loaned to {self.borrower.name}"

    class Meta:
        verbose_name = "Loan"
        verbose_name_plural = "Loans"
