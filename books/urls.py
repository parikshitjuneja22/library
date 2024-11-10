from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('books/', views.list_books, name='list_books'),
    path('borrow/', views.borrow_book, name='borrow_book'),
    path('return/', views.return_book, name='return_book'),
    path('borrowed/<int:borrower_id>/', views.list_borrowed_books, name='list_borrowed_books'),
    path('history/<int:borrower_id>/', views.borrower_history, name='borrower_history'),
    path('add_books/', views.add_book, name='add_book'),
    path('borrowers/', views.create_borrower, name='create_borrower'),
    path('borrowers/list/', views.list_borrowers, name='list_borrowers'),
]
