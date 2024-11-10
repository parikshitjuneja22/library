from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, Borrower, Loan
from .serializers import BookSerializer, BorrowerSerializer, LoanSerializer
from django.http import JsonResponse
from django.utils import timezone

@api_view(['POST'])
def add_book(request):
    """Add a new book to the library."""
    if request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_books(request):
    """List all books in the library, optionally filter by availability."""
    available = request.GET.get('available', None)
    if available:
        books = Book.objects.filter(available=(available.lower() == 'true'))
    else:
        books = Book.objects.all()
    
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def borrow_book(request):
    """Borrow a book from the library."""
    book_id = request.data.get('book_id')
    borrower_id = request.data.get('borrower_id')

    try:
        book = Book.objects.get(id=book_id)
        borrower = Borrower.objects.get(id=borrower_id)
    except (Book.DoesNotExist, Borrower.DoesNotExist):
        return Response({"error": "Invalid book or borrower ID"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if borrower is active and has not exceeded borrowing limit
    if not borrower.is_active:
        return Response({"error": "Borrower is not active."}, status=status.HTTP_400_BAD_REQUEST)
    
    active_loans = Loan.objects.filter(borrower=borrower, is_returned=False)
    if active_loans.count() >= 3:
        return Response({"error": "Borrower has exceeded the borrowing limit of 3 books."}, status=status.HTTP_400_BAD_REQUEST)

    if not book.available:
        return Response({"error": "The book is currently unavailable."}, status=status.HTTP_400_BAD_REQUEST)

    # Borrow the book
    loan = Loan.objects.create(book=book, borrower=borrower)
    book.available = False
    book.borrow_count += 1
    book.save()

    return Response({"message": "Book borrowed successfully."}, status=status.HTTP_200_OK)

@api_view(['POST'])
def return_book(request):
    """Return a borrowed book."""
    book_id = request.data.get('book_id')
    borrower_id = request.data.get('borrower_id')

    try:
        book = Book.objects.get(id=book_id)
        borrower = Borrower.objects.get(id=borrower_id)
        loan = Loan.objects.filter(book=book, borrower=borrower, is_returned=False).first()
    except (Book.DoesNotExist, Borrower.DoesNotExist, Loan.DoesNotExist):
        return Response({"error": "Invalid data or no active loan found."}, status=status.HTTP_400_BAD_REQUEST)

    loan.is_returned = True
    loan.return_date = timezone.now()
    loan.save()

    # Update book availability
    book.available = True
    book.save()

    return Response({"message": "Book returned successfully."}, status=status.HTTP_200_OK)

@api_view(['GET'])
def list_borrowed_books(request, borrower_id):
    """List all active (unreturned) books for a borrower."""
    borrower = Borrower.objects.get(id=borrower_id)
    loans = Loan.objects.filter(borrower=borrower, is_returned=False)
    books = [loan.book for loan in loans]

    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def borrower_history(request, borrower_id):
    """List all books ever borrowed by a borrower."""
    borrower = Borrower.objects.get(id=borrower_id)
    loans = Loan.objects.filter(borrower=borrower)
    books = [loan.book for loan in loans]

    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_borrower(request):
    """Create a new borrower."""
    if request.method == 'POST':
        serializer = BorrowerSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the new borrower to the database
            borrower = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def list_borrowers(request):
    """List all borrowers."""
    if request.method == 'GET':
        borrowers = Borrower.objects.all()  # Get all borrowers
        serializer = BorrowerSerializer(borrowers, many=True)  # Serialize the borrowers
        return Response(serializer.data)

def health_check(request):
    """Health check endpoint to verify if the API is running."""
    return JsonResponse({"status": "ok"})