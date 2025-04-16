from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Book, Borrowing
from django.core.exceptions import PermissionDenied

class StaffOnlyAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.role in [User.Role.LIBRARIAN, User.Role.MANAGER]

    def has_view_permission(self, request, obj=None):
        return request.user.role in [User.Role.LIBRARIAN, User.Role.MANAGER]

    def has_add_permission(self, request):
        return request.user.role in [User.Role.LIBRARIAN, User.Role.MANAGER]

    def has_change_permission(self, request, obj=None):
        return request.user.role in [User.Role.LIBRARIAN, User.Role.MANAGER]

    def has_delete_permission(self, request, obj=None):
        return request.user.role == User.Role.MANAGER  # Only managers can delete

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Book)
class BookAdmin(StaffOnlyAdmin):
    list_display = ('title', 'author', 'isbn', 'quantity', 'available')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('author',)

@admin.register(Borrowing)
class BorrowingAdmin(StaffOnlyAdmin):
    list_display = ('book', 'member', 'borrow_date', 'return_date', 'is_returned', 'processed_by')
    list_filter = ('is_returned', 'borrow_date')
    search_fields = ('book__title', 'member__username')
