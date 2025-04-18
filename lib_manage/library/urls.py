from django.urls import path
from .views import home, book_list, borrowing_list

urlpatterns = [
    path('', home, name='home'),
    path('books/', book_list, name='book_list'),
    path('borrowings/', borrowing_list, name='borrowing_list'),
] 