from rest_framework import serializers
from .models import Book, Borrower, Loan

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'isbn', 'available', 'borrow_count']

class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = ['id', 'name', 'email', 'membership_date', 'is_active']

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'book', 'borrower', 'borrowed_date', 'return_date', 'is_returned']
