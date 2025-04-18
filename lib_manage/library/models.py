from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Role(models.TextChoices):
        MEMBER = 'MEMBER', _('Member')
        LIBRARIAN = 'LIBRARIAN', _('Librarian')
        MANAGER = 'MANAGER', _('Manager')
    
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    quantity = models.PositiveIntegerField(default=1)
    available = models.PositiveIntegerField(default=1)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='added_books')
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.title} by {self.author}"

class Borrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': User.Role.MEMBER}, related_name='borrowed_books')
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                   limit_choices_to={'role__in': [User.Role.LIBRARIAN, User.Role.MANAGER]},
                                   related_name='processed_borrowings')
    
    def __str__(self):
        return f"{self.member} borrowed {self.book}"
