from django.contrib import admin
from .models import Book, BookLog
from django.utils.html import format_html
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['book_name', 'book_author', 'book_genre', 'isAvailable', 'borrowed_by_users', 'created_at']
    list_filter = ['book_genre', 'isAvailable', 'created_at']
    search_fields = ['book_name', 'book_author', 'book_genre']
    readonly_fields = ['created_at']
    list_per_page = 20
    
    def borrowed_by_users(self, obj):
        """Show who has borrowed this book"""
        borrowers = obj.borrowed_by.all()
        if borrowers:
            return format_html('<span style="color: red;">Borrowed by: {}</span>', 
                             ', '.join([user.username for user in borrowers]))
        return format_html('<span style="color: green;">Available</span>')
    
    borrowed_by_users.short_description = 'Borrowing Status'

@admin.register(BookLog)
class BookLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'action', 'timestamp', 'days_since_action']
    list_filter = ['action', 'timestamp', 'user__username', 'book__book_genre']
    search_fields = ['user__username', 'user__email', 'book__book_name', 'book__book_author']
    readonly_fields = ['timestamp']
    list_per_page = 50
    date_hierarchy = 'timestamp'
    actions = ['mark_as_returned', 'send_overdue_notification']
    
    def days_since_action(self, obj):
        """Calculate days since the action"""
        from django.utils import timezone
        from datetime import datetime
        
        now = timezone.now()
        days = (now - obj.timestamp).days
        
        if obj.action == 'borrow':
            if days > 14:  # Overdue (assuming 14-day loan period)
                return format_html('<span style="color: red; font-weight: bold;">{} days (OVERDUE)</span>', days)
            else:
                return format_html('<span style="color: orange;">{} days</span>', days)
        else:  # return
            return format_html('<span style="color: green;">{} days ago</span>', days)
    
    days_since_action.short_description = 'Days Since Action'
    
    def get_queryset(self, request):
        """Optimize queries with select_related"""
        return super().get_queryset(request).select_related('user', 'book')
    
    def get_search_results(self, request, queryset, search_term):
        """Enhanced search functionality"""
        if search_term:
            queryset = queryset.filter(
                Q(user__username__icontains=search_term) |
                Q(user__email__icontains=search_term) |
                Q(book__book_name__icontains=search_term) |
                Q(book__book_author__icontains=search_term)
            )
        return queryset, True
    
    @admin.action(description="Mark selected books as returned")
    def mark_as_returned(self, request, queryset):
        """Admin action to mark books as returned"""
        updated = 0
        for log in queryset.filter(action='borrow'):
            # Remove book from user's borrowed list
            log.user.userbooklist.remove(log.book)
            # Mark book as available
            log.book.isAvailable = True
            log.book.save()
            # Create return log
            BookLog.objects.create(
                user=log.user,
                book=log.book,
                action='return'
            )
            updated += 1
        
        if updated == 1:
            message = "1 book was marked as returned."
        else:
            message = f"{updated} books were marked as returned."
        
        self.message_user(request, message, messages.SUCCESS)
    
    @admin.action(description="Send overdue notification")
    def send_overdue_notification(self, request, queryset):
        """Admin action to send overdue notifications"""
        overdue_books = queryset.filter(
            action='borrow',
            timestamp__lt=timezone.now() - timedelta(days=14)
        )
        
        if overdue_books:
            message = f"Overdue notification would be sent for {overdue_books.count()} books."
            self.message_user(request, message, messages.WARNING)
        else:
            self.message_user(request, "No overdue books found in selection.", messages.INFO)
