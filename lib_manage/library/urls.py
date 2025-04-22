from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('borrowings/', views.borrowing_list, name='borrowing_list'),
    path('search/', views.search_books, name='search_books'),
] 