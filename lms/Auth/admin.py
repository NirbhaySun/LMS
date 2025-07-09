from django.contrib import admin
from .models import User
from django.utils.html import format_html
from django.db.models import Count

# Register the custom User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_role', 'books_borrowed', 'is_active']
    list_filter = ['is_admin', 'is_librarian', 'is_active']
    search_fields = ['username', 'email']
    readonly_fields = ['last_login']
    list_per_page = 25
    
    def user_role(self, obj):
        """Display user role with color coding"""
        if obj.is_admin:
            return format_html('<span style="color: red; font-weight: bold;">Admin</span>')
        elif obj.is_librarian:
            return format_html('<span style="color: blue; font-weight: bold;">Librarian</span>')
        else:
            return format_html('<span style="color: green;">Regular User</span>')
    
    user_role.short_description = 'Role'
    
    def books_borrowed(self, obj):
        """Show number of books currently borrowed"""
        count = obj.userbooklist.count()
        if count > 0:
            return format_html('<span style="color: orange; font-weight: bold;">{} books</span>', count)
        return format_html('<span style="color: green;">0 books</span>')
    
    books_borrowed.short_description = 'Books Borrowed'
    
    def get_queryset(self, request):
        """Optimize queries with prefetch_related"""
        return super().get_queryset(request).prefetch_related('userbooklist')
    
    
    # 3 fieldsets for admin panel i.e. info,perms and dates
    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'email', 'userdob', 'profile_pic')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_admin', 'is_librarian')
        }),
        ('Important Dates', {
            'fields': ('last_login',),
            'classes': ('collapse',)
        }),
    )
