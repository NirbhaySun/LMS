from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import api_views

router = DefaultRouter()
router.register(r'books', api_views.BookViewSet, basename='book')
router.register(r'users', api_views.UserViewSet, basename='user')
router.register(r'logs', api_views.BookLogViewSet, basename='booklog')

urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:pk>/wishlist/', api_views.WishlistView.as_view(), name='user-wishlist'),
    path('users/<int:pk>/profile/', api_views.UserProfileView.as_view(), name='user-profile'),
    path('users/<int:pk>/borrowed/', api_views.UserBorrowedBooksView.as_view(), name='user-borrowed-books'),
    path('users/<int:pk>/logs/', api_views.UserLogsView.as_view(), name='user-logs'),
    path('users/<int:pk>/change_password/', api_views.UserChangePasswordView.as_view(), name='user-change-password'),
    path('books/<int:pk>/photo/', api_views.BookPhotoUploadView.as_view(), name='book-photo-upload'),
    path('librarian/assign/', api_views.AssignBookView.as_view(), name='assign-book'),
    path('librarian/return/', api_views.ReturnBookView.as_view(), name='return-book'),
    path('librarian/users_borrowed/', api_views.LibrarianUsersBorrowedView.as_view(), name='librarian-users-borrowed'),
] 