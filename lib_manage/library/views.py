from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Book, Borrowing, User
from .services.google_books_service import GoogleBooksService
from django.contrib import messages

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        if request.user.role == User.Role.MEMBER:
            # Show member's recent borrowings and available books
            recent_borrowings = Borrowing.objects.filter(member=request.user, is_returned=False)
            available_books = Book.objects.filter(available__gt=0)
            return render(request, 'library/home.html', {
                'recent_borrowings': recent_borrowings,
                'available_books': available_books
            })
        else:
            # Show staff dashboard with recent borrowings and low stock books
            recent_borrowings = Borrowing.objects.filter(is_returned=False).order_by('-borrow_date')[:5]
            low_stock_books = Book.objects.filter(available__lt=3)
            return render(request, 'library/staff_home.html', {
                'recent_borrowings': recent_borrowings,
                'low_stock_books': low_stock_books
            })
    return render(request, 'library/home.html')

@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

@login_required
def borrowing_list(request):
    if request.user.role in [User.Role.LIBRARIAN, User.Role.MANAGER]:
        borrowings = Borrowing.objects.all()
    else:
        # Members can only see their own borrowings
        borrowings = Borrowing.objects.filter(member=request.user)
    return render(request, 'library/borrowing_list.html', {'borrowings': borrowings})

@login_required
def search_books(request):
    query = request.GET.get('q', '')
    books = []
    
    if query:
        try:
            books_service = GoogleBooksService()
            books = books_service.search_books(query)
        except ValueError as e:
            messages.error(request, "Google Books API is not properly configured. Please contact the administrator.")
            print(f"Google Books API Error: {str(e)}")
        except Exception as e:
            messages.error(request, "An error occurred while searching for books. Please try again later.")
            print(f"Search Error: {str(e)}")
    
    return render(request, 'library/search_results.html', {
        'books': books,
        'query': query
    })
