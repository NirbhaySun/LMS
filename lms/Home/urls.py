from django.urls import path
from .views import home, book_detail, librarian_dashboard, add_book, edit_book, delete_book, return_book, notifications

urlpatterns = [
    path('', home, name='home'),
    path('book/<int:book_id>/', book_detail, name='book_detail'),
    path('librarian/', librarian_dashboard, name='librarian_dashboard'),
    path('librarian/add/', add_book, name='add_book'),
    path('librarian/edit/<int:book_id>/', edit_book, name='edit_book'),
    path('librarian/delete/<int:book_id>/', delete_book, name='delete_book'),
    path('librarian/return/<int:book_id>/<int:user_id>/', return_book, name='return_book'),
    path('librarian/notifications/', notifications, name='librarian_notifications'),
] 